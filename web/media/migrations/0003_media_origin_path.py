# Generated by Django 2.1.7 on 2019-05-16 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_seed_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='origin_path',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
