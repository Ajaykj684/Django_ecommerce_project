# Generated by Django 4.0.4 on 2022-06-18 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0006_todo_delete_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='todo_list',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
