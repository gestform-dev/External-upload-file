from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate


class DocumentsConfig(AppConfig):
    name = "documents"

    verbose_name = _("Documents")

    def ready(self):
        from .signals import document_consumption_finished
        from .signals.handlers import add_inbox_tags
        from .signals.handlers import add_to_index
        from .signals.handlers import set_correspondent
        from .signals.handlers import set_document_type
        from .signals.handlers import set_log_entry
        from .signals.handlers import set_storage_path
        from .signals.handlers import set_tags
        from .signals.handlers import create_advance_ui_permission
        from .signals.handlers import create_account_settings_permission
        from paperless.handlers import add_user
        from paperless.handlers import handle_basic_employee_group_init
        from django.db.models.signals import post_migrate

        document_consumption_finished.connect(add_inbox_tags)
        document_consumption_finished.connect(set_correspondent)
        document_consumption_finished.connect(set_document_type)
        document_consumption_finished.connect(set_tags)
        document_consumption_finished.connect(set_storage_path)
        document_consumption_finished.connect(set_log_entry)
        document_consumption_finished.connect(add_to_index)

        post_migrate.connect(add_user)

        post_migrate.connect(create_advance_ui_permission)
        post_migrate.connect(create_account_settings_permission)

        post_migrate.connect(handle_basic_employee_group_init, sender=self)

        AppConfig.ready(self)
