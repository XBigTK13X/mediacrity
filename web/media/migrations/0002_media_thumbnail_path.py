# Generated by Django 2.1.7 on 2019-04-03 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='thumbnail_path',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
