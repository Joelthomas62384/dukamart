# Generated by Django 5.0 on 2023-12-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_feature_image_feature_link_alter_slider_slider_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature',
            name='image',
            field=models.ImageField(upload_to='media/Feature'),
        ),
    ]
