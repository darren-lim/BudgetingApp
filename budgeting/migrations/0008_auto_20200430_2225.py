# Generated by Django 3.0.4 on 2020-05-01 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgeting', '0007_auto_20200427_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='t_type',
            field=models.CharField(max_length=15, null=True),
        ),
    ]