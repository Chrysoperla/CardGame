# Generated by Django 4.1.7 on 2023-03-20 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_matchstate_last_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initialstate',
            name='farm',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='initialstate',
            name='food',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='initialstate',
            name='fountain',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='initialstate',
            name='gold',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='initialstate',
            name='mana',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='initialstate',
            name='mine',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='initialstate',
            name='tower',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='initialstate',
            name='wall',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player1state',
            name='farm',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player1state',
            name='food',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player1state',
            name='fountain',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player1state',
            name='gold',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player1state',
            name='mana',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player1state',
            name='mine',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player1state',
            name='tower',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player1state',
            name='wall',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player2state',
            name='farm',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player2state',
            name='food',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player2state',
            name='fountain',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player2state',
            name='gold',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player2state',
            name='mana',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player2state',
            name='mine',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player2state',
            name='tower',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='player2state',
            name='wall',
            field=models.PositiveIntegerField(),
        ),
    ]
