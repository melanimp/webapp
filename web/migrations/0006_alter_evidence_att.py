# Generated by Django 5.0.3 on 2024-03-11 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_evidence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidence',
            name='att',
            field=models.BooleanField(default=True),
        ),
    ]