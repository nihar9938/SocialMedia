# Generated by Django 3.0.6 on 2020-06-14 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatabase',
            name='Degree',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='company',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='experience',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='location',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='userdatabase',
            name='website',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
