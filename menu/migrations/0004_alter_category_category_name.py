# Generated by Django 5.1 on 2024-09-09 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_fooditem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100),
        ),
    ]
