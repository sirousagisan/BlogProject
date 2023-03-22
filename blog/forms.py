from django import forms
from .models import Comment

class aboutForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    enquiry = forms.CharField(required=True,
                            widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
                