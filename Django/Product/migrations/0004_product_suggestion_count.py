# Generated by Django 3.2 on 2021-04-22 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_auto_20210419_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='suggestion_count',
            field=models.IntegerField(default=0, verbose_name='تعداد پیشنهاد خرید'),
        ),
    ]
