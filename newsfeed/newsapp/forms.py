from django import forms


class SearchForm(forms.Form):
    search_words = forms.CharField(label="Search", max_length=100)
    search_words.widget.attrs.update({'class':'form-control'})