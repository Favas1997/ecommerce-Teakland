# Generated by Django 3.1.6 on 2021-03-24 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210324_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
