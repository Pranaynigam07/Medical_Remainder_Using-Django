# Generated by Django 3.1.5 on 2021-04-18 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='appointments',
            fields=[
                ('case_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('mob', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('dept', models.CharField(max_length=200)),
                ('doc_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='doctors_information',
            fields=[
                ('doctor_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.department')),
            ],
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=500)),
                ('key', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='patient_table',
            fields=[
                ('case_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('file_presciption', models.FileField(upload_to='prescription')),
                ('next_date', models.DateField()),
                ('status', models.CharField(max_length=20)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.department')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.doctors_information')),
                ('patient_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.login')),
            ],
        ),
        migrations.CreateModel(
            name='qnty',
            fields=[
                ('quantity', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='slots',
            fields=[
                ('slot_name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tablets',
            fields=[
                ('tablet_name', models.CharField(max_length=1000, primary_key=True, serialize=False)),
                ('Comments', models.CharField(max_length=500)),
                ('case_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.patient_table')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.department')),
                ('patient_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.login')),
                ('prescribed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.doctors_information')),
                ('quantity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.qnty')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.slots')),
            ],
        ),
    ]