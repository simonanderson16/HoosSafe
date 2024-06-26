# Generated by Django 4.2.10 on 2024-04-04 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_rename_type_report_type_of_violation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='file',
        ),
        migrations.CreateModel(
            name='ReportFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='static')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='users.report')),
            ],
        ),
    ]
