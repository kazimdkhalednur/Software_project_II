# Generated by Django 5.0.4 on 2024-05-24 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0005_cart_total_price_alter_cart_product_alter_cart_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="sold",
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="Discount Price",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="products/thhumbnails/"
            ),
        ),
    ]