# Generated by Django 5.0.4 on 2024-10-22 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_splitdetail_percentage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenses',
            old_name='creators',
            new_name='creator',
        ),
    ]
