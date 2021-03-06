# Generated by Django 3.1.4 on 2020-12-08 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20201208_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('multiple_choice', 'Multiple Choice'), ('numeric_input', 'Numeric Input')], default=None, max_length=50, verbose_name='Type of Question'),
            preserve_default=False,
        ),
    ]
