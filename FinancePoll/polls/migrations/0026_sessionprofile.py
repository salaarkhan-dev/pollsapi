# Generated by Django 3.1.4 on 2020-12-09 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0025_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=200)),
                ('user_rating', models.IntegerField(blank=True, default=0)),
                ('profile_calc', models.FloatField(blank=True, default=0)),
                ('potential_investment', models.FloatField(blank=True, default=0)),
                ('horizon', models.FloatField(blank=True, default=0)),
                ('liquidity_needs', models.FloatField(blank=True, default=0)),
                ('investment_experience_years', models.FloatField(blank=True, default=0)),
                ('investment_previous', models.FloatField(blank=True, default=0)),
                ('accepts_profile', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='profiles', to='polls.poll')),
                ('profile_text', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='polls.bit')),
            ],
        ),
    ]