
from django import forms
from django.forms import ModelForm
from .models import Topic

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["name", "wid"]
    photo = forms.CharField()
