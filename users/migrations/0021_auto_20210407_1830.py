# Generated by Django 3.1.7 on 2021-04-07 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20210407_1720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='coupon_price',
            new_name='coupon_percentage',
        ),
        migrations.RemoveField(
            model_name='coupon',
            name='user',
        ),
    ]
