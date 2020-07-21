from django.forms import ModelForm

from .models import MailBox


class ContactUsForm(ModelForm):
	class Meta:
		model = MailBox
		fields = ['name', 'body', 'email']