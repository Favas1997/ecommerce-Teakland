# Generated by Django 3.1.6 on 2021-03-31 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20210331_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image1',
            field=models.ImageField(null=True, upload_to='usermedia/'),
        ),
    ]