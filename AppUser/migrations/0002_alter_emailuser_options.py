# Generated by Django 4.2.7 on 2023-11-28 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppUser', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailuser',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
