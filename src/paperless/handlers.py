import logging
from . import constants
from datetime import datetime, timezone
from django.db import connection

logger = logging.getLogger("paperless.auth")


def check_and_create_group(group_name, permissions):
    from django.contrib.auth.models import Group, Permission

    group, created = Group.objects.get_or_create(name=group_name)
    if created or not set(group.permissions.all()) == set(permissions):
        group.permissions.clear()
        for permission_codename in permissions:
            permission = Permission.objects.get(codename=permission_codename)
            group.permissions.add(permission)
        group.save()
    return group


def handle_basic_employee_group_init(sender, **kwargs):
    group_name = constants.EMPLOYEE
    permissions = [
        constants.ADD_DOCUMENT_PERMISSION,
        constants.CHANGE_DOCUMENT_PERMISSION,
        constants.VIEW_DOCUMENT_PERMISSION,
        ]
    check_and_create_group(group_name, permissions)
    logger.info(constants.EMPLOYEE_GROUP_CREATED)


def add_user(sender=None, **kwargs):
    with connection.cursor() as cursor:
        # cursor.execute(
        # "ALTER TABLE paperless_customuser RENAME COLUMN prestation TO "
        # "activity;"
        # )
        # cursor.execute(
        #     "SELECT column_name "
        #     "FROM information_schema.columns "
        #     "WHERE table_name = 'paperless_customuser';"
        #     )
        # columns = cursor.fetchall()
        # print(columns)
        # import pdb
        # pdb.set_trace()
        # cursor.execute(
        #     "ALTER TABLE paperless_customuser RENAME COLUMN activity TO "
        #     "user_id;"
        #     )
        cursor.execute(
            "SELECT username FROM paperless_customuser WHERE "
            "username='user';"
            )
        exist = cursor.fetchone()
        if exist == None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                f"INSERT INTO paperless_customuser (username,is_superuser,"
                f"is_staff,is_active,date_joined,password,first_name,"
                f"last_name,email,activity,matricule,organization, "
                f"technical_client_id) values ('user', false, false, "
                f"true, '{date}','','','','','','','', '')"
                )
