# Generated by Django 3.0.3 on 2020-02-11 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapp', '0007_auto_20200211_0817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='Owners',
        ),
        migrations.AddField(
            model_name='application',
            name='Owners',
            field=models.ManyToManyField(to='restapp.Owner'),
        ),
    ]
