# Generated by Django 3.2.13 on 2022-06-16 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jp_app', '0010_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='recruiter',
            field=models.ForeignKey(default=1,on_delete=django.db.models.deletion.CASCADE, to='jp_app.recruiter'),
        ),
    ]
