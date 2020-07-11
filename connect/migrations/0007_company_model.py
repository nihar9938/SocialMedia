# Generated by Django 3.0.6 on 2020-07-01 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connect', '0006_auto_20200622_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('number', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('map_embad', models.TextField(blank=True, null=True)),
                ('usr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]