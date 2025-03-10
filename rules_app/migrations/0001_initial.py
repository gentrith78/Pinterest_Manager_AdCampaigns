# Generated by Django 4.2 on 2023-04-26 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('api_token', models.CharField(max_length=255)),
                ('ad_account_id', models.IntegerField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator_choice', models.CharField(choices=[('D', 'Choose Operator'), ('A', 'All'), ('O', 'At Least One')], default='D', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_type', models.CharField(choices=[('D', 'Initial'), ('S', 'By Status'), ('I', 'By Id')], default='D', max_length=1)),
                ('operator_choice', models.CharField(choices=[('D', 'Choose Operator'), ('A', 'All'), ('O', 'At Least One')], default='D', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Rule_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Enter Name', max_length=255)),
                ('description', models.TextField(default='Enter Description', max_length=255)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'Inactive')], default='A', max_length=1)),
                ('ad_acc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='strategy', to='rules_app.adaccount')),
            ],
        ),
        migrations.CreateModel(
            name='Interval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.CharField(choices=[('DEF', 'Select Interval'), ('E10', 'Every 10 Min'), ('E30', 'Every 30 Min'), ('EH', 'Every Hour'), ('ETH', 'Every Two Hours'), ('ED', 'Every Day'), ('EW', 'Every Week')], default='ED', max_length=3)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('rule_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rules_app.rule_item')),
            ],
        ),
        migrations.CreateModel(
            name='FilterStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_choice', models.CharField(choices=[('IS', 'Is'), ('IN', 'Is Not')], default='IS', max_length=2)),
                ('status', models.CharField(choices=[('D', 'Select Status'), ('A', 'Active'), ('I', 'Inactive')], default='D', max_length=1)),
                ('confirmed', models.BooleanField(default=False)),
                ('filter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rules_app.filter')),
            ],
        ),
        migrations.CreateModel(
            name='FilterId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_choice', models.CharField(choices=[('IS', 'Is'), ('IN', 'Is Not')], default='IS', max_length=2)),
                ('value', models.IntegerField(default=0)),
                ('confirmed', models.BooleanField(default=False)),
                ('filter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rules_app.filter')),
            ],
        ),
        migrations.AddField(
            model_name='filter',
            name='rule_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter', to='rules_app.rule_item'),
        ),
        migrations.CreateModel(
            name='ConditionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variable', models.CharField(choices=[('DEF', 'Select Variable'), ('TCPCH', 'Total CPA Checkout'), ('TCOCH', 'Total Conversions Checkout'), ('ROASC', 'ROAS Checkout'), ('ROASA', 'Total ROAS Add to cart'), ('TCAC', 'Total Conversions Add to cart'), ('CTR', 'CTR'), ('SP', 'Spendings'), ('LSC', 'Lifetime Spend Cap'), ('DSC', 'Daily Spend Cap')], default='DEF', max_length=255)),
                ('granularity', models.CharField(choices=[('DEF', 'Select Granularity'), ('T', 'Today'), ('TY', 'Today and Yesterday'), ('Y', 'Yesterday'), ('LTDT', 'Last Three Days INC. Today'), ('LTD', 'Last Three Days'), ('LWD', 'Last Week Inc. Today'), ('LW', 'Last Week')], default='DEF', max_length=255)),
                ('condition_op', models.CharField(choices=[('DEF', 'Select Condition'), ('E', 'Equal'), ('NE', 'Not Equal'), ('GT', 'Greater Than'), ('GTE', 'Greater Than or Equal'), ('LT', 'Less Than'), ('LTE', 'Less Than or Equal')], default='DEF', max_length=255)),
                ('value', models.CharField(default=0, max_length=255)),
                ('confirmed', models.BooleanField(default=False)),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rules_app.condition')),
            ],
        ),
        migrations.AddField(
            model_name='condition',
            name='rule_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='rules_app.rule_item'),
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('IN', 'Increase Budget'), ('SB', 'Set Budget'), ('De', 'Decrease Budget')], default='IN', max_length=2)),
                ('value', models.IntegerField(default=0)),
                ('confirmed', models.BooleanField(default=False)),
                ('rule_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action', to='rules_app.rule_item')),
            ],
        ),
    ]
