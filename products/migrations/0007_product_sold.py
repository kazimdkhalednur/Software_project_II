# Generated by Django 5.0.4 on 2024-05-24 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0006_remove_product_sold_alter_product_price_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sold",
            field=models.IntegerField(default=0),
        ),
    ]
