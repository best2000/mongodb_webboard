from django import forms
from django.forms import ModelForm
from core.models import Topic , Comment, Tag

class create_topic_form(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']

class create_comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class edit_topic_form(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']

class EditTopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content']

class create_topic_tag_form(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']

class TopicTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['tag']
