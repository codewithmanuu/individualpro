from django import forms


class dform(forms.Form):
    username=forms.CharField(max_length=30)
    email=forms.EmailField()
    password=forms.CharField(max_length=30)
    confirm = forms.CharField(max_length=30)

class dlogform(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

class orthoform(forms.Form):
    image = forms.FileField()
    name=forms.CharField(max_length=30)
    country=forms.CharField(max_length=30)
    state=forms.CharField(max_length=30)
    city=forms.CharField(max_length=30)
    qualification=forms.CharField(max_length=30)
    specialisation=forms.CharField(max_length=30)