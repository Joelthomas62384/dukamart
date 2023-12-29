# Generated by Django 5.0 on 2023-12-29 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_main_category_section_alter_feature_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='product',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.sub_category'),
        ),
        migrations.DeleteModel(
            name='Addition_informations',
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
