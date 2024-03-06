# Generated by Django 5.0.1 on 2024-01-25 16:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_webpost_subtheme_webpost_theme'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebPostType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WebPostCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.webpost')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.webposttype')),
            ],
        ),
    ]