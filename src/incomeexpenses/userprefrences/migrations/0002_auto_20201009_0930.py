# Generated by Django 3.0.8 on 2020-10-09 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprefrences', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userpreferences',
            old_name='catergory',
            new_name='currency',
        ),
    ]
