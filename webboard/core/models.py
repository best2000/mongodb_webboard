from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Topic (models.Model):
    topicid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=150)
    like = models.IntegerField(null=True)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment (models.Model):
    commentid = models.AutoField(primary_key=True)
    content = models.CharField(max_length=150)
    like = models.IntegerField()
    date = models.DateTimeField(null=True)
    comuserid = models.ForeignKey(User, on_delete=models.CASCADE)
    comtopicid = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.commentid)

class Create (models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    topicid = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.date.strftime("%B %d, %Y, %H:%M %p"))

class Tag (models.Model):
    topicid = models.ForeignKey(Topic, on_delete=models.CASCADE)
    tag = models.CharField(max_length=30)

    def __str__(self):
        return self.tag

class LikeTopic(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    like_topicid = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userid)

class LikeComment(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    like_commentid = models.ForeignKey(Comment, on_delete=models.CASCADE)
    topicid = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.userid)
