# Generated by Django 3.1.4 on 2020-12-13 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0040_auto_20201213_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='bit',
            field=models.ManyToManyField(related_name='products', to='polls.Bit'),
        ),
    ]
