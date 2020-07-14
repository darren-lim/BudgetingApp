# Generated by Django 2.2.12 on 2020-07-14 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
                ('current_monthly_spent', models.IntegerField(default=0)),
                ('current_monthly_income', models.IntegerField(default=0)),
                ('monthly_goal', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12)),
                ('int_monthly_goal', models.IntegerField(default=0)),
                ('monthly_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('is_expense', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_type', models.CharField(max_length=15, null=True, verbose_name='Income/Expense')),
                ('source', models.CharField(max_length=30, verbose_name='Title')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('d_amount', models.IntegerField(default=0)),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional Information')),
                ('date_posted', models.DateField(null=True, verbose_name='Transaction\xa0Date (mm/dd/yyyy)')),
                ('in_history', models.BooleanField(default=False)),
                ('year', models.IntegerField(null=True)),
                ('month', models.IntegerField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='budgeting.Categories')),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
        migrations.CreateModel(
            name='Total',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Initial Balance')),
                ('total_amount', models.IntegerField(default=0)),
                ('total_amount_gained', models.IntegerField(default=0)),
                ('total_amount_spent', models.IntegerField(default=0)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(null=True)),
                ('month', models.IntegerField(null=True)),
                ('monthly_amount_gained', models.IntegerField(default=0)),
                ('monthly_amount_spent', models.IntegerField(default=0)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
