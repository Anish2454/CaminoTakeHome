# Generated by Django 3.0.3 on 2020-02-11 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0006_auto_20200211_0804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestheader',
            name='CFApiPassword',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='requestheader',
            name='CFApiUserId',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
