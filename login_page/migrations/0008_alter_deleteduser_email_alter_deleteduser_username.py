# Generated by Django 5.0.6 on 2024-05-28 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_page', '0007_alter_updateduser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deleteduser',
            name='email',
            field=models.EmailField(max_length=100),
        ),
        migrations.AlterField(
            model_name='deleteduser',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
