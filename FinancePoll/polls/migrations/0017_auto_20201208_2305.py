# Generated by Django 3.1.4 on 2020-12-08 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0016_auto_20201208_2258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='answer',
            new_name='choice',
        ),
    ]
