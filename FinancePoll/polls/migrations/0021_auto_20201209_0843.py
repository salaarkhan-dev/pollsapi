# Generated by Django 3.1.3 on 2020-12-09 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0020_auto_20201209_0727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order', 'id'], 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=1),
        ),
    ]
