# Generated by Django 3.0.3 on 2020-06-25 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200625_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='chead0',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='chead1',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='chead2',
            field=models.CharField(default='', max_length=500),
        ),
    ]