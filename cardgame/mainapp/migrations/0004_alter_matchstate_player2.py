# Generated by Django 4.1.7 on 2023-03-23 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_initialstate_farm_alter_initialstate_food_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchstate',
            name='player2',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainapp.player2state'),
        ),
    ]
