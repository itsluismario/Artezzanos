# Generated by Django 3.1.7 on 2021-03-15 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210308_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='holder_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
