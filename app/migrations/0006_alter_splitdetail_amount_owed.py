# Generated by Django 5.0.4 on 2024-10-22 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_creators_expenses_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='splitdetail',
            name='amount_owed',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
