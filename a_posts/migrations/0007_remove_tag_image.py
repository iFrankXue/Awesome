# Generated by Django 5.1.2 on 2024-10-23 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0006_alter_tag_options_tag_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='image',
        ),
    ]
