# Generated by Django 2.0.13 on 2023-12-16 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apphosting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario_bd',
            name='senhavoip',
            field=models.CharField(default=None, max_length=5),
        ),
    ]