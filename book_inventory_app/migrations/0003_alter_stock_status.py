# Generated by Django 3.2 on 2022-10-11 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_inventory_app', '0002_auto_20221011_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='status',
            field=models.CharField(blank=True, choices=[('Good', 'Good'), ('Bad', 'Bad'), ('Critical', 'Critical'), ('OS', 'out of stock')], default='Good', max_length=23, null=True),
        ),
    ]