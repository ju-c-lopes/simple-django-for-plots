# Generated by Django 5.0.3 on 2024-03-31 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_alter_aluno_notas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='aprovado',
        ),
        migrations.AddField(
            model_name='prova',
            name='aprovado',
            field=models.BooleanField(default=False),
        ),
    ]
