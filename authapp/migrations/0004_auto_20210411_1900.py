# Generated by Django 3.1.7 on 2021-04-11 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20210411_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='актуальность ключа'),
        ),
        migrations.CreateModel(
            name='ShopUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_line', models.CharField(blank=True, max_length=128, verbose_name='Тэги')),
                ('about_me', models.TextField(blank=True, max_length=512, verbose_name='о себе')),
                ('gender', models.CharField(blank=True, choices=[('M', 'M'), ('W', 'Ж')], max_length=1, verbose_name='пол')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
