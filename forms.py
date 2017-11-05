from django import forms
class RequestForm(forms.Form):
	flat=forms.CharField(required=False)

