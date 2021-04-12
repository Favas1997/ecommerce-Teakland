# Generated by Django 3.1.7 on 2021-04-09 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0021_auto_20210407_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Referal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referal_code', models.CharField(max_length=10, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('coupon_percentage', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
