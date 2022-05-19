# Generated by Django 3.0 on 2022-05-18 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('author', models.CharField(max_length=140)),
                ('year', models.IntegerField()),
                ('finished', models.BooleanField()),
                ('users', models.ManyToManyField(related_name='books', to='users.Profile', verbose_name='Пользователи')),
            ],
        ),
    ]
