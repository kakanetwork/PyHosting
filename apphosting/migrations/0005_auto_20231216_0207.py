# Generated by Django 2.0.13 on 2023-12-16 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apphosting', '0004_auto_20231216_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario_bd',
            name='id_user',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]