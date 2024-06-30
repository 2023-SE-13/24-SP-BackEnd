# Generated by Django 4.2.4 on 2024-06-30 04:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CompanyManagement', '0008_remove_position_company_delete_application_and_more'),
        ('UserManagement', '0009_user_avatar'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PositionTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('specialization', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'PositionTags',
                'unique_together': {('category', 'specialization')},
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('position_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('position_name', models.CharField(max_length=255)),
                ('position_description', models.CharField(max_length=255)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('education_requirement', models.CharField(blank=True, max_length=255, null=True)),
                ('salary_min', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_max', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('posted_at', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CompanyManagement.company')),
                ('position_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='PositionManagement.positiontag')),
                ('skill_required', models.ManyToManyField(blank=True, to='UserManagement.skill')),
            ],
            options={
                'db_table': 'Positions',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('application_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('applied_at', models.DateTimeField()),
                ('result', models.CharField(blank=True, max_length=255, null=True)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PositionManagement.position')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'applications',
            },
        ),
    ]
