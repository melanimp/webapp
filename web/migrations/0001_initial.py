# Generated by Django 5.0.3 on 2024-03-11 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=30)),
                ('ulname', models.EmailField(max_length=30)),
                ('passwd', models.CharField(max_length=65)),
                ('email', models.BooleanField(default=True)),
                ('rol', models.CharField(max_length=30)),
            ],
        ),
    ]
