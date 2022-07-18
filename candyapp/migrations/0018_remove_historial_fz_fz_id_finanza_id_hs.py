# Generated by Django 4.0.3 on 2022-07-03 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candyapp', '0017_historial_fz_id_lg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historial_fz',
            name='fz_id',
        ),
        migrations.AddField(
            model_name='finanza',
            name='id_hs',
            field=models.IntegerField(default=2, verbose_name='Historial'),
            preserve_default=False,
        ),
    ]
