# Generated manually to fix ProductImage table structure

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_update_productimage_model'),
    ]

    operations = [
        # Remove old fields if they exist
        migrations.RemoveField(
            model_name='productimage',
            name='image_data',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='image_type',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='filename',
        ),
        
        # Add new image field
        migrations.AddField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Imagen'),
        ),
    ]
