from django import forms

class aboutForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    enquiry = forms.CharField(required=True,
                            widget=forms.Textarea)