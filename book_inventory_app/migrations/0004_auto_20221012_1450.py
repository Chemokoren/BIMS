# Generated by Django 3.2 on 2022-10-12 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_inventory_app', '0003_alter_stock_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='book_inventory_app.author'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='book_inventory_app.book'),
        ),
    ]
