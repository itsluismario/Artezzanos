# Generated by Django 3.1.7 on 2021-03-17 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210317_2316'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='CartHeader',
            new_name='cartheader',
        ),
    ]