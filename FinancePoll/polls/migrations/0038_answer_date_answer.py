# Generated by Django 3.1.4 on 2020-12-10 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0037_auto_20201210_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='date_answer',
            field=models.DateField(blank=True, null=True),
        ),
    ]
