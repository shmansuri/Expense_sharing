# Generated by Django 5.0.4 on 2024-10-22 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_splitdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='splitdetail',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]