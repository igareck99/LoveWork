# Generated by Django 3.2.5 on 2021-08-01 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caljan', '0009_workshop'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='parent_id',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
