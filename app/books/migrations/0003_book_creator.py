# Generated by Django 3.0.1 on 2020-01-20 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('books', '0002_auto_20200113_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
    ]
