# Generated by Django 3.2.9 on 2021-12-03 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20211203_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_posts', to='blog.postarray'),
        ),
    ]
