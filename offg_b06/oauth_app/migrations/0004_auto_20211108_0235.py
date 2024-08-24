# Generated by Django 3.2.5 on 2021-11-08 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_app', '0003_housing_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='housing',
            name='popularity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='housing',
            name='description',
            field=models.CharField(default='description of housing option', max_length=1000),
        ),
    ]
