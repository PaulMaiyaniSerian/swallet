# Generated by Django 4.1.7 on 2023-03-26 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userwallet_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='account_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
