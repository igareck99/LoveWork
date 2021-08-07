# Generated by Django 3.2.5 on 2021-08-01 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caljan', '0006_remove_tables_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tables',
            name='number',
        ),
        migrations.AddField(
            model_name='tables',
            name='person_amount',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='tables',
            name='table_num',
            field=models.CharField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='tables',
            name='table_title',
            field=models.CharField(default='Стол', max_length=100),
        ),
        migrations.AlterField(
            model_name='tables',
            name='info',
            field=models.CharField(default='', max_length=200),
        ),
    ]