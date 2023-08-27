# Generated by Django 4.0.3 on 2023-02-15 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_alter_advertcard_a_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_message', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='offer',
            name='a_img',
            field=models.ImageField(default='book/media/photos/appartment.jpg', upload_to='book/media/photos'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_message', models.CharField(max_length=100)),
                ('a_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
