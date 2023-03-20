from django import forms

class aboutForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    comment = forms.CharField(required=False,
                            widget=forms.Textarea)