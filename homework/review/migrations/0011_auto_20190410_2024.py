# Generated by Django 2.2 on 2019-04-10 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_auto_20190410_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='score',
            field=models.CharField(choices=[('low', '1'), ('low', '2'), ('low', '3'), ('middle', '4'), ('middle', '5'), ('middle', '6'), ('middle', '7'), ('high', '8'), ('high', '9'), ('high', '10')], default='5', max_length=5),
        ),
    ]
