# Generated by Django 5.0.3 on 2024-03-11 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_actividad_type_alter_evidence_uname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidence',
            name='uname',
            field=models.ForeignKey(limit_choices_to={'rol__name': 'Estudiante'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.usuario'),
        ),
    ]
