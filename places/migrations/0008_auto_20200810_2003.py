# Generated by Django 3.0.7 on 2020-08-10 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_auto_20200607_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='place_id',
            field=models.SlugField(blank=True, max_length=100, verbose_name='Place ID slug field'),
        ),
    ]
