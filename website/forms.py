from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", Widget=forms.TextInput(attrs= {'class':'form-control', 'palceholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class meta:
        model  = User
        fields = ('username','email', 'first_name', 'last_name','password1','password2')

        def __int__(self, *args,**kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
            self.fields['username'].label=''
            self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
            self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
            self.fields['password1'].label=''
            self.fields['password1'].help_text = 'Required. 8 characters or more.'
            self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
            self.fields['password2'].label=''
            self.fields['password2'].help_text = 'Enter the same password as before for verification.'