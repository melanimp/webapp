# Generated by Django 5.0.3 on 2024-03-25 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_evidence_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidence',
            name='doc',
            field=models.ImageField(default='/img_default', upload_to='webapp/static/public/'),
        ),
        migrations.AlterField(
            model_name='evidence',
            name='recog',
            field=models.CharField(default='', max_length=30),
        ),
    ]
