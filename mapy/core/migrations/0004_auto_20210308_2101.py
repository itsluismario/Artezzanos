# Generated by Django 3.1.7 on 2021-03-08 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210308_2053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippingaddress',
            options={},
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='apartment_address',
            new_name='instructions',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='default',
            new_name='is_delivered',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='street_address',
            new_name='shipping_address',
        ),
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zip',
            new_name='shipping_zip',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='address_type',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]