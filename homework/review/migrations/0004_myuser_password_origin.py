# Generated by Django 2.2.1 on 2019-05-19 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_find'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='password_origin',
            field=models.CharField(default='', max_length=20),
        ),
    ]
