# Generated by Django 5.0.4 on 2024-05-02 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_product_options_cart"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="is_active",
        ),
    ]
