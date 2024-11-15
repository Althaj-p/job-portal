# Generated by Django 3.2.13 on 2022-06-28 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0012_alter_job_recruiter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.FileField(null=True, upload_to='')),
                ('applydate', models.DateField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jp_app.job')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jp_app.studentuser')),
            ],
        ),
    ]
