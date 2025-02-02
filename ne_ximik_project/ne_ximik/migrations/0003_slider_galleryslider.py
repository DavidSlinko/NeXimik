# Generated by Django 5.0.1 on 2024-02-06 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ne_ximik', '0002_product_brand_taste_product_taste'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='Краткоео описание к слайдеру')),
                ('description', models.CharField(max_length=400, verbose_name='Под описание')),
            ],
        ),
        migrations.CreateModel(
            name='GallerySlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images_slider/', verbose_name='Картинка для слайдера')),
                ('slider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ne_ximik.slider', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Картинка для слайдэра',
                'verbose_name_plural': 'Картинки для слайдэра',
            },
        ),
    ]
