from django import forms


class SearchForm(forms.Form):
    search_words = forms.CharField(label="Search", max_length=100)
    search_words.widget.attrs.update({'class':'form-control', 'placeholder':'Search' })

class ContactForm(forms.Form):
    subject = forms.CharField(label="Subject", max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    subject.widget.attrs.update({'class':'form-control'})
    message.widget.attrs.update({'class':'form-control'})

class SubscribeForm(forms.Form):
    email_address = forms.EmailField(label="", max_length=100)
    email_address.widget.attrs.update({'class':'form-control', 'placeholder':'Email' })