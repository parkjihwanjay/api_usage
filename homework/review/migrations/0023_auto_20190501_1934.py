# Generated by Django 2.2 on 2019-05-01 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0022_auto_20190501_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='댓글',
            field=models.CharField(max_length=150),
        ),
    ]
