from django import forms
from .models import Comment, FormModel

class aboutForm(forms.ModelForm):
    # name = forms.CharField(max_length=30)
    # email = forms.EmailField()
    # enquiry = forms.CharField(required=True,
    #                         widget=forms.Textarea)
    class Meta:
        model = FormModel
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
                