# Generated by Django 3.0.2 on 2020-01-11 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200109_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totalviews',
            name='session',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
