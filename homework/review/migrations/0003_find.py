# Generated by Django 2.2.1 on 2019-05-17 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_remove_myuser_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Find',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=20)),
            ],
        ),
    ]