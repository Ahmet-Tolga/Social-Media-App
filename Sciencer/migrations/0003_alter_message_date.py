# Generated by Django 4.0.3 on 2023-03-27 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sciencer', '0002_alter_message_date_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.CharField(max_length=200),
        ),
    ]