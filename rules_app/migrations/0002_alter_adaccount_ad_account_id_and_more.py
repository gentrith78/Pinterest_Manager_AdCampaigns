# Generated by Django 4.2 on 2023-04-28 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adaccount',
            name='ad_account_id',
            field=models.IntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='adaccount',
            name='api_token',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='adaccount',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='condition',
            name='operator_choice',
            field=models.CharField(choices=[('D', 'Choose Operator'), ('A', 'All'), ('O', 'At Least One')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='rule_item',
            name='description',
            field=models.TextField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='rule_item',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
