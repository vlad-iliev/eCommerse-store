# Generated by Django 3.2.21 on 2023-09-23 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='first_name',
            new_name='forename',
        ),
    ]