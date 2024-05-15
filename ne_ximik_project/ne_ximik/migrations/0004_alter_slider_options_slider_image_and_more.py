# Generated by Django 5.0.1 on 2024-02-06 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ne_ximik', '0003_slider_galleryslider'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slider',
            options={'verbose_name': 'Слайдер', 'verbose_name_plural': 'Слайдер'},
        ),
        migrations.AddField(
            model_name='slider',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images_slider/', verbose_name='Картинка для слайдера'),
        ),
        migrations.DeleteModel(
            name='GallerySlider',
        ),
    ]
