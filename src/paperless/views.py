import os

from collections import OrderedDict

from django.contrib.auth.models import Group
from django.contrib.auth.views import INTERNAL_RESET_SESSION_TOKEN
from django.contrib.auth.views import LoginView
from django.db.models.functions import Lower
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, \
    BasicAuthentication, TokenAuthentication
from django.utils.translation import gettext as _

from documents.permissions import PaperlessObjectPermissions
from paperless.filters import GroupFilterSet
from paperless.filters import UserFilterSet
from paperless.serialisers import GroupSerializer
from paperless.serialisers import UserSerializer
from django.contrib.auth import password_validation

from django.shortcuts import render, redirect, reverse
from .forms import (CustomUserCreationForm,
                    UserForgotPasswordForm,
                    CustomSetPasswordForm)
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth.views import PasswordResetConfirmView
from paperless_management.account_service import get_valid_users
from paperless_management.account_management import (
    create_account_success_management,
    modify_account_success_management,
    modify_account_password_success_management,
    log_in_account_success_management,
    create_account_failure_management,
    modify_account_failure_management,
    modify_account_password_failure_management, RequiredFieldException,
    CreationException, MissingEmployeeInPersonDbException
    )
from paperless_management.state_enum import StateEnum
from paperless_management.error_enum import AccountErrorLabelEnum
from paperless_management.config_management import ConfigManagement
from . import constants
from paperless.validators import FrenchPhoneNumberValidator
from phonenumber_field.phonenumber import to_python
import logging

logger = logging.getLogger("paperless")

from django.contrib.auth import get_user_model

User = get_user_model()


class UserResetPassword():
    def userResetPassword(request):
        if request.user.is_authenticated:
            return redirect(constants.BASE_LABEL)
        if request.method == "POST":
            form = UserForgotPasswordForm(request.POST)
            if form.is_valid():
                opts = {
                    "request": request,
                    }
                form.save(**opts)
                return redirect(reverse(constants.LOGIN_LABEL)
                                +
                                constants.RESET_PASSWORD_EMAIL_TOASTER_SEARCH_PARAM)
            messages.error(
                request, "Unsuccessful registration. Invalid information.")
        else:
            form = UserForgotPasswordForm()
        return render(
            request=request,
            template_name="registration/forgot_password.html",
            context={"forgotpassword_form": form}
            )


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        user = form.save()
        config = ConfigManagement()
        send_sms_enabled = (
            config
            .is_sms_enabled_for_action(
                user.activity,
                StateEnum.RESET_PASSWORD_SUCCESS)
        )
        modify_account_password_success_management(
            user, constants.RESET_PASSWORD_LABEL, send_sms_enabled)
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        return redirect(reverse(constants.LOGIN_LABEL)
                        +
                        constants.RESET_PASSWORD_SUCCESS_TOASTER_SEARCH_PARAM)

    def form_invalid(self, form):
        user = form.save(commit=False)
        modify_account_password_failure_management(
            user,
            AccountErrorLabelEnum.PASSWORD_MODIFICATION.value,
            constants.RESET_PASSWORD_ERROR_STATUS)
        del user
        return self.render_to_response(self.get_context_data(form=form))


class EditProfileView(APIView):
    def patch(self, request):
        _new_data = {}
        _is_valid_french_number = (FrenchPhoneNumberValidator()
        .is_valid_french_number(
            str(request.data[constants.PHONE_NUMBER])))
        _new_data[constants.USERNAME] = request.data[constants.USERNAME]
        _new_data[constants.EMAIL] = request.data[constants.USERNAME]
        _new_data[constants.PHONE_NUMBER] = ''

        if request.data[constants.PHONE_NUMBER] != '':
            _new_data[constants.PHONE_NUMBER] = to_python(
                request.data[constants.PHONE_NUMBER], constants.FR).as_e164
        serializer = UserSerializer(request.user, data=_new_data, partial=True)

        if serializer.is_valid() and (_is_valid_french_number
                                      or _new_data[constants.PHONE_NUMBER]
                                      == ''):
            serializer.save()
            modify_account_success_management(request.user)
            return Response(status=status.HTTP_200_OK)
        else:
            modify_account_failure_management(
                request.user,
                (AccountErrorLabelEnum
                 .MODIFICATION.value))
            error = self._format_error(_is_valid_french_number, serializer)
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    def _format_error(self, _is_valid_french_number, serializer):
        error = {}
        if (constants.USERNAME in serializer.errors
            or constants.EMAIL in serializer.errors):
            error = self._create_usnername_error(serializer.errors)
        if (constants.PHONE_NUMBER in serializer.errors
            or not _is_valid_french_number):
            error[constants.PHONE_NUMBER] = _(
                constants.PHONE_NUMBER_ERROR_MESSAGE)
        return error

    def _create_usnername_error(self, serializer_error: list):
        error = {}
        error[constants.USERNAME] = []
        try:
            error[constants.USERNAME].append(
                serializer_error[constants.USERNAME])
        except Exception as e:
            logger.debug(e)
        try:
            error[constants.USERNAME].append(serializer_error[constants.EMAIL])
        except Exception as e:
            logger.debug(e)
        return error


class EditPasswordView(APIView):
    def patch(self, request, format=None):
        returnedError = None
        new_password = request.data[constants.NEW_PASSWORD]
        old_password = request.data[constants.PASSWORD]
        user = request.user
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)

        if not user.check_password(old_password):
            returnedError = {
                constants.PASSWORD: _(constants.INVALID_PASWWORD_ERROR_MESSAGE)
                }
            modify_account_password_failure_management(
                user,
                AccountErrorLabelEnum.PASSWORD_MODIFICATION.value,
                constants.UPDATE_PASSWORD_ERROR_STATUS)
            return Response(returnedError, status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            try:
                password_validation.validate_password(new_password)
            except password_validation.ValidationError as error:
                returnedError = {
                    constants.NEW_PASSWORD: error,
                    constants.CONFIRM_PASSWORD: error,
                    }
                modify_account_password_failure_management(
                    user,
                    AccountErrorLabelEnum.PASSWORD_MODIFICATION.value,
                    constants.UPDATE_PASSWORD_ERROR_STATUS)
                return Response(returnedError,
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(new_password)
                user.save()
                modify_account_password_success_management(request.user)
                return Response(status=status.HTTP_200_OK)
        else:
            modify_account_password_failure_management(
                user,
                AccountErrorLabelEnum.PASSWORD_MODIFICATION.value,
                constants.UPDATE_PASSWORD_ERROR_STATUS)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        log_in_account_success_management(form.get_user())
        return HttpResponseRedirect(self.get_success_url())


def _handle_creation_exceptions(user, exception):
    if isinstance(exception, (RequiredFieldException,
                              MissingEmployeeInPersonDbException,
                              CreationException)):
        create_account_failure_management(
            user,
            AccountErrorLabelEnum.CREATION.value
            )
    else:
        raise exception


class SignUpRequest:
    def signUp_request(self, request):
        if request.user.is_authenticated:
            return redirect(constants.BASE_LABEL)
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(False)
                valid_users_found_in_configs_list = []
                try:
                    valid_users_found_in_configs_list = get_valid_users(user)
                except (RequiredFieldException,
                        MissingEmployeeInPersonDbException,
                        CreationException) as exception:
                    _handle_creation_exceptions(user, exception)
                if len(valid_users_found_in_configs_list) > 0:
                    # SUCCESS ROUTE
                    valid_users_in_first_activity = \
                        valid_users_found_in_configs_list[0]
                    form.try_define_additionals_fields(
                        user, valid_users_in_first_activity)
                    user = form.save()
                    config = ConfigManagement()
                    send_sms_enabled = (
                        config
                        .is_sms_enabled_for_action(
                            user.activity,
                            StateEnum.ACCOUNT_CREATION_SUCCESS)
                    )
                    basic_employee_group = Group.objects.get(
                        name=constants.EMPLOYEE)
                    basic_employee_group.user_set.add(user)
                    create_account_success_management(
                        user,
                        send_sms=send_sms_enabled)
                    messages.success(request,
                                     constants.REGISTRATION_SUCCESS_MESSAGE)
                    return redirect(constants.LOGIN_LABEL)
                else:
                    return redirect(reverse(constants.LOGIN_LABEL)
                                    +
                                    constants.SIGN_UP_FAILED_TOASTER_SEARCH_PARAM)
            user_instance = form.create_invalid_user()
            messages.error(
                request, constants.REGISTRATION_FAILURE_MESSAGE)
            fields_in_error = {
                constants.FIELDS_IN_ERROR: list(form.errors.keys())}
            create_account_failure_management(
                user_instance, AccountErrorLabelEnum.CREATION.value,
                error_description=fields_in_error
                )
        else:
            form = CustomUserCreationForm()
        return render(
            request=request,
            template_name="registration/signUp.html",
            context={"signUp_form": form},
            )


class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100000

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("all", self.get_all_result_ids()),
                    ("results", data),
                    ],
                ),
            )

    def get_all_result_ids(self):
        ids = []
        if hasattr(self.page.paginator.object_list, "saved_results"):
            results_page = self.page.paginator.object_list.saved_results[0]
            if results_page is not None:
                for i in range(0, len(results_page.results.docs())):
                    try:
                        fields = results_page.results.fields(i)
                        if "id" in fields:
                            ids.append(fields["id"])
                    except Exception:
                        pass
        else:
            for obj in self.page.paginator.object_list:
                if hasattr(obj, "id"):
                    ids.append(obj.id)
                elif hasattr(obj, "fields"):
                    ids.append(obj.fields()["id"])
        return ids

    def get_paginated_response_schema(self, schema):
        response_schema = super().get_paginated_response_schema(schema)
        response_schema["properties"]["all"] = {
            "type": "array",
            "example": "[1, 2, 3]",
            }
        return response_schema


class FaviconView(View):
    def get(self, request, *args, **kwargs):  # pragma: nocover
        favicon = os.path.join(
            os.path.dirname(__file__),
            "static",
            "paperless",
            "img",
            "favicon.ico",
            )
        with open(favicon, "rb") as f:
            return HttpResponse(f, content_type="image/x-icon")


class UserViewSet(ModelViewSet):
    model = User

    queryset = User.objects.exclude(
        username__in=["consumer", "AnonymousUser"],
        ).order_by(Lower("username"))

    serializer_class = UserSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated, PaperlessObjectPermissions)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = UserFilterSet
    ordering_fields = ("username",)


class GroupViewSet(ModelViewSet):
    model = Group

    queryset = Group.objects.order_by(Lower("name"))

    serializer_class = GroupSerializer
    pagination_class = StandardPagination
    permission_classes = (IsAuthenticated, PaperlessObjectPermissions)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = GroupFilterSet
    ordering_fields = ("name",)


class GetMaxAllowedSizeInConfigView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication,
                              BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            activity = request.user.activity
            config = ConfigManagement()
            max_allowed_size_in_mb = config.get_max_allowed_size_in_MB(
                activity)
        except:
            raise GetMaxAllowedSizeException()
        return Response(max_allowed_size_in_mb)


class GetMaxAllowedSizeException(Exception):
    pass
