# Generated by Django 4.2.4 on 2023-08-17 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datas', '0004_alter_benefit_content_alter_card_link_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='카드명'),
        ),
    ]