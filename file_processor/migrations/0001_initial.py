# Generated by Django 5.0.2 on 2024-12-04 20:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('file_name', models.CharField(max_length=255)),
                ('file_content', models.TextField()),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('processing', 'Processing'), ('completed', 'Completed'), ('error', 'Error')], default='processing', max_length=50)),
                ('result', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
