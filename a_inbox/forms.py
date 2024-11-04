from django import forms
from .models import Conversation, InboxMessage

class InboxNewMessageForm(forms.ModelForm):
    class Meta:
        model = InboxMessage
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Add message ...',
            }),
        }
