# Generated by Django 4.1.7 on 2023-03-26 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userwallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='account_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
    ]
