# Generated by Django 4.1.13 on 2024-08-29 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_alter_gallery_options_alter_review_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='home',
            options={'verbose_name_plural': 'Home'},
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image1',
            new_name='gallery_image1',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image10',
            new_name='gallery_image10',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image2',
            new_name='gallery_image2',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image3',
            new_name='gallery_image3',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image4',
            new_name='gallery_image4',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image5',
            new_name='gallery_image5',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image6',
            new_name='gallery_image6',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image7',
            new_name='gallery_image7',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image8',
            new_name='gallery_image8',
        ),
        migrations.RenameField(
            model_name='gallery',
            old_name='image9',
            new_name='gallery_image9',
        ),
    ]
