# Generated by Django 5.1 on 2024-08-22 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.RenameField(
            model_name='fooditem',
            old_name='category_name',
            new_name='category',
        ),
    ]
