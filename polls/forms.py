from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Poll, Choice, User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'is_public']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']

ChoiceFormSet = inlineformset_factory(Poll, Choice, form=ChoiceForm, extra=2, can_delete=True)