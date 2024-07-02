# Generated by Django 4.2.4 on 2024-07-02 05:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('like_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'db_table': 'Likes',
            },
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('tweet_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_retweet', models.BooleanField(default=False)),
                ('text_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
                ('retweets', models.IntegerField(default=0)),
                ('comments', models.IntegerField(default=0)),
                ('retweet_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TweetManagement.tweet')),
            ],
            options={
                'db_table': 'Tweets',
            },
        ),
        migrations.CreateModel(
            name='TweetPhoto',
            fields=[
                ('photo_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='resources/tweetphotos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TweetManagement.tweet')),
            ],
            options={
                'db_table': 'TweetPhotos',
            },
        ),
    ]
