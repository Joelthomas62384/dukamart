# Generated by Django 5.0 on 2023-12-29 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_product_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
