# Generated by Django 3.0.5 on 2020-07-04 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20200704_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='store.MinCategory'),
        ),
    ]