# Generated by Django 2.2.16 on 2022-04-11 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0013_auto_20220411_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.TextField(verbose_name=posts.models.Post)),
                ('text', models.CharField(help_text='Введите текст коментария', max_length=400, verbose_name='Текст коментария')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время публикации комментария')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор коментария')),
            ],
        ),
    ]