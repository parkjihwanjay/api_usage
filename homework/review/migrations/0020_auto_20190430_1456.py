# Generated by Django 2.2 on 2019-04-30 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0019_auto_20190430_1441'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='댓글',
        ),
    ]
