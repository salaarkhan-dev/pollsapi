# Generated by Django 3.1.4 on 2020-12-09 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0027_answer_total_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]
