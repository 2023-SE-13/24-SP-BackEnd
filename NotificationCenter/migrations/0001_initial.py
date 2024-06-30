# Generated by Django 4.2.4 on 2024-06-30 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CompanyManagement', '0008_remove_position_company_delete_application_and_more'),
        ('TweetManagement', '0003_rename_content_tweet_text_content_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserManagement', '0016_user_desired_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('notification_type', models.CharField(choices=[('message', 'Message Mention'), ('subscribe', 'Subscribe Mention'), ('system', 'System Notification')], max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.CharField(max_length=255)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='CompanyManagement.company')),
                ('message', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='UserManagement.message')),
                ('tweet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='TweetManagement.tweet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
