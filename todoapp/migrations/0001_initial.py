# Generated by Django 4.0.4 on 2022-06-09 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import todoapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('firstname', models.CharField(max_length=100, null=True, validators=[todoapp.models.only_char])),
                ('lastname', models.CharField(max_length=100, null=True, validators=[todoapp.models.only_char])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('todo_task_id', models.CharField(blank=True, max_length=200)),
                ('task', models.JSONField(default=list, null=True)),
                ('wbs_id', models.CharField(default='WBSID', max_length=50, null=True)),
                ('status', models.CharField(choices=[('1', 'selected'), ('2', 'notStarted'), ('3', 'inProgress'), ('4', 'completed')], default='2', max_length=50)),
                ('exported', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('due_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('createdAt', models.DateField(auto_now_add=True)),
                ('updatedAt', models.DateField(auto_now=True)),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plan_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
