# Generated by Django 3.2 on 2021-04-20 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Coupon', '0002_coupon_user'),
        ('Payment', '0004_auto_20210420_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Coupon.coupon', verbose_name='کد تخفیف'),
        ),
    ]
