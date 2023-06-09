# Generated by Django 3.2 on 2023-04-03 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('colleges', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PracticeDrawingExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('task_description', models.TextField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colleges.college')),
            ],
        ),
        migrations.CreateModel(
            name='MCQExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('option1', models.CharField(max_length=100)),
                ('option2', models.CharField(max_length=100)),
                ('option3', models.CharField(max_length=100)),
                ('answer', models.CharField(max_length=100)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colleges.college')),
            ],
        ),
        migrations.CreateModel(
            name='HandDrawingExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('task_description', models.TextField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colleges.college')),
            ],
        ),
        migrations.CreateModel(
            name='DigitalDrawingExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('task_description', models.TextField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='colleges.college')),
            ],
        ),
    ]
