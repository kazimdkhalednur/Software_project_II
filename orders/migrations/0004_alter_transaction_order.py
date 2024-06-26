# Generated by Django 5.0.4 on 2024-05-24 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_transaction_paid_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transactions",
                to="orders.order",
            ),
        ),
    ]
