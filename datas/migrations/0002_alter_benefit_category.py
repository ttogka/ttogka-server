# Generated by Django 4.2.4 on 2023-08-17 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefit',
            name='category',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='혜택카테고리'),
        ),
    ]
