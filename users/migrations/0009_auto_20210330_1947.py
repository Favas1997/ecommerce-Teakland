# Generated by Django 3.1.6 on 2021-03-30 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210330_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image1',
            field=models.ImageField(null=True, upload_to='media11/'),
        ),
    ]
