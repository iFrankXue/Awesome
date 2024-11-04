# Generated by Django 5.1.2 on 2024-10-22 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0002_alter_post_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='post',
            name='artist',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
