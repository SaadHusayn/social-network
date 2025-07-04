from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]  
    return f'network/users_profile_pictures/{instance.username}.{ext}'  

class User(AbstractUser):
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False, blank=True)
    profile_picture = models.ImageField(blank=True, upload_to=user_directory_path)
    bio = models.CharField(blank=True, max_length=300)

    def add_follower(self, user):   
        if user == self:
            raise ValidationError("Users cannot follow themselves")
        self.followers.add(user)

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    postContent = models.CharField(max_length=1000, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        if len(self.postContent) > 8:
            dots = '...'
        else:
            dots = ''
        return f"{self.creator.username}: {self.postContent[:8] + dots } at {self.created_at}"

class Comment(models.Model):
    content = models.CharField(max_length=120)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  
        return f"{self.writer}: {self.content}"
    
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "writer": {
                "username": self.writer.username,
                "profile_picture": self.writer.profile_picture.url if self.writer.profile_picture else None
            },
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }