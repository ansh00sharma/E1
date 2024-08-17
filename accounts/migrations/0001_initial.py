# Generated by Django 5.1 on 2024-08-16 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.CharField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=254)),
                ('phone_number', models.CharField(blank=True, max_length=12)),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Restaurant'), (2, 'Customer')], null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
