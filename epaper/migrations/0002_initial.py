# Generated by Django 5.0.4 on 2024-05-09 10:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('edition', '0002_alter_edition_options_edition_is_active'),
        ('epaper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edition.edition')),
            ],
            options={
                'verbose_name': 'Paper',
                'verbose_name_plural': 'Papers',
                'db_table': 'paper',
            },
        ),
        migrations.CreateModel(
            name='PaperPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_url', models.CharField(default='', max_length=1024)),
                ('gif_url', models.CharField(default='', max_length=1024)),
                ('thumbnail_url', models.CharField(default='', max_length=1024)),
                ('page_number', models.IntegerField(default=999)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epaper.paper')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'db_table': 'paper_page',
            },
        ),
    ]
