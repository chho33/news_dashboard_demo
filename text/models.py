from django.db import models

class Content(models.Model):
    url = models.CharField(max_length=1000)
    title = models.CharField(max_length=500)
    content = models.TextField()
    type = models.CharField(max_length=10,null=True)
    source = models.CharField(max_length=20,null=True)
    date = models.DateTimeField(null=True)
    author = models.CharField(max_length=30,null=True)
    discussion_count = models.IntegerField(null=True)
    share_count = models.IntegerField(null=True)
    comment_count = models.IntegerField(null=True)
    like_count = models.IntegerField(null=True)
    dislike_count = models.IntegerField(null=True)

    def __str__(self):
        return self.title
