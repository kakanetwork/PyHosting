# Generated by Django 2.0.13 on 2023-12-22 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apphosting', '0002_auto_20231219_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario_bd',
            name='senha',
            field=models.CharField(max_length=255),
        ),
    ]
