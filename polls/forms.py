from django import forms
from .models import Poll, Choice
from django.forms import inlineformset_factory

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'is_public']

ChoiceFormSet = inlineformset_factory(
    Poll,
    Choice,
    fields=['text'],
    extra=2,
    can_delete=False
)
