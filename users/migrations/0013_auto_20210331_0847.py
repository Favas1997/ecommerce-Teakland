# Generated by Django 3.1.6 on 2021-03-31 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210331_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image1',
            field=models.ImageField(null=True, upload_to='media/'),
        ),
    ]