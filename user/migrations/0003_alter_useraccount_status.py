# Generated by Django 3.2 on 2023-06-19 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_useraccount_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='status',
            field=models.CharField(choices=[('user', 'User'), ('student_review', 'Student Review'), ('student_rejected', 'Student Rejected'), ('student', 'Student')], default='user', max_length=20),
        ),
    ]
