# Generated by Django 5.1.1 on 2024-10-18 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0017_contactsubmission_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='call_to_action',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='main_title',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='sub_title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
