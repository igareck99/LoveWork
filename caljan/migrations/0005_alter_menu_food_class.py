# Generated by Django 3.2.5 on 2021-08-01 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caljan', '0004_alter_menu_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='food_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='caljan.food_class'),
        ),
    ]
