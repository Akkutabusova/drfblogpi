# Generated by Django 3.2.9 on 2021-12-26 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_postarray_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='premium',
            field=models.BooleanField(default=False),
        ),
    ]