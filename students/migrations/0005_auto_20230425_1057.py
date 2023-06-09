# Generated by Django 3.2 on 2023-04-25 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20230425_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='digitaldrawinganswer',
            name='answer',
            field=models.ImageField(upload_to='digital_drawing_answers/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='handdrawinganswer',
            name='answer',
            field=models.ImageField(upload_to='hand_drawing_answers/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='practicedrawinganswer',
            name='answer',
            field=models.ImageField(upload_to='practice_drawing_answers/%Y/%m/%d'),
        ),
    ]
