# Generated by Django 5.0 on 2024-01-15 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
