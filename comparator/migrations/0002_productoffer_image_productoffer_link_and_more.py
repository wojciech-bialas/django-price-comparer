# Generated by Django 4.0.1 on 2022-03-02 11:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('comparator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productoffer',
            name='image',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productoffer',
            name='link',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productoffer',
            name='shop',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productprice',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productprice',
            name='price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
