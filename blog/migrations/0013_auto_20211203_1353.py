# Generated by Django 3.2.9 on 2021-12-03 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_rename_content_postarray_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postarray',
            name='post',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_posts', to='blog.postarray'),
        ),
    ]