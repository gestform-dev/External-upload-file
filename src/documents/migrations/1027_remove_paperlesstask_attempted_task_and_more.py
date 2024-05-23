# Generated by Django 4.1.2 on 2022-10-17 16:31

import django.utils.timezone
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "1026_transition_to_celery"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paperlesstask",
            name="attempted_task",
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="date_created",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="Datetime field when the task result was created in UTC",
                null=True,
                verbose_name="Created DateTime",
            ),
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="date_done",
            field=models.DateTimeField(
                default=None,
                help_text="Datetime field when the task was completed in UTC",
                null=True,
                verbose_name="Completed DateTime",
            ),
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="date_started",
            field=models.DateTimeField(
                default=None,
                help_text="Datetime field when the task was started in UTC",
                null=True,
                verbose_name="Started DateTime",
            ),
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="result",
            field=models.TextField(
                default=None,
                help_text="The data returned by the task",
                null=True,
                verbose_name="Result Data",
            ),
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="status",
            field=models.CharField(
                choices=[
                    ("FAILURE", "FAILURE"),
                    ("PENDING", "PENDING"),
                    ("RECEIVED", "RECEIVED"),
                    ("RETRY", "RETRY"),
                    ("REVOKED", "REVOKED"),
                    ("STARTED", "STARTED"),
                    ("SUCCESS", "SUCCESS"),
                ],
                default="PENDING",
                help_text="Current state of the task being run",
                max_length=30,
                verbose_name="Task State",
            ),
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="task_args",
            field=models.JSONField(
                help_text="JSON representation of the positional arguments used with the task",
                null=True,
                verbose_name="Task Positional Arguments",
            ),
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="task_file_name",
            field=models.CharField(
                help_text="Name of the file which the Task was run for",
                max_length=255,
                null=True,
                verbose_name="Task Name",
            ),
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="task_kwargs",
            field=models.JSONField(
                help_text="JSON representation of the named arguments used with the task",
                null=True,
                verbose_name="Task Named Arguments",
            ),
        ),
        migrations.AddField(
            model_name="paperlesstask",
            name="task_name",
            field=models.CharField(
                help_text="Name of the Task which was run",
                max_length=255,
                null=True,
                verbose_name="Task Name",
            ),
        ),
        migrations.AlterField(
            model_name="paperlesstask",
            name="acknowledged",
            field=models.BooleanField(
                default=False,
                help_text="If the task is acknowledged via the frontend or API",
                verbose_name="Acknowledged",
            ),
        ),
        migrations.AlterField(
            model_name="paperlesstask",
            name="task_id",
            field=models.CharField(
                help_text="Celery ID for the Task that was run",
                max_length=255,
                unique=True,
                verbose_name="Task ID",
            ),
        ),
    ]