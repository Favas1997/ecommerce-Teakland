# Generated by Django 3.1.6 on 2021-03-24 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.IntegerField(),
        ),
    ]
