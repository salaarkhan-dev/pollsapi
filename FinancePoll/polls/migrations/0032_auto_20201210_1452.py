# Generated by Django 3.1.4 on 2020-12-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0031_sessionprofile_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numericchoice',
            name='choice_text',
            field=models.FloatField(blank=True),
        ),
    ]