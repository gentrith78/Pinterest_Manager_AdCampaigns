# Generated by Django 4.2 on 2023-04-29 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules_app', '0003_alter_conditionitem_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditionitem',
            name='value',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
