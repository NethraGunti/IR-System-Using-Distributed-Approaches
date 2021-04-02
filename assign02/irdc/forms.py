from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control form-control-lg',
                'type' : 'search',
                'placeholder' : 'enter your query'
            }
        )
    )