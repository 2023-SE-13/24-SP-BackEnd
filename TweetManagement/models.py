import uuid

from django.db import models
import os
from UserManagement.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

class Tweet(models.Model):
    tweet_id = models.UUIDField(primary_key=True, auto_created=True, unique=True, editable=False, default=uuid.uuid4)
    is_retweet = models.BooleanField(default=False)
    retweet_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    retweets = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        db_table = 'Tweets'

    def __str__(self):
        return f"{self.user} - {self.tweet_id}"

class TweetPhoto(models.Model):
    photo_id = models.UUIDField(primary_key=True, auto_created=True, unique=True, editable=False, default=uuid.uuid4)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='resources/tweetphotos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'TweetPhotos'

    def __str__(self):
        return f"{self.tweet} - {self.photo_id}"

class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, auto_created=True, unique=True, editable=False, default=uuid.uuid4)
    target_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='received_comments')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Comments'

    def __str__(self):
        return f"{self.sender} - {self.comment_id} ({self.tweet})"

class Likes(models.Model):
    like_id = models.UUIDField(primary_key=True, auto_created=True, unique=True, editable=False, default=uuid.uuid4)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='liked_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Likes'

    def __str__(self):
        return f"{self.user} - {self.like_id} ({self.tweet})"
    
@receiver(post_delete, sender=TweetPhoto)
def delete_photo(sender, instance, **kwargs):
    if instance.photo and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)