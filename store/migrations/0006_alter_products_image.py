# Generated by Django 4.2.7 on 2023-11-05 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_products_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='product_images/'),
        ),
    ]
