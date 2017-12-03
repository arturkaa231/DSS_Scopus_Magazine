from django import forms
class ReqForm(forms.Form):
	id=forms.CharField(required=False)
	title=forms.CharField(required=False)
	ISSN=forms.CharField(required=False)
	E_ISSN=forms.CharField(required=False)
	date1=forms.CharField(required=False)
	date2=forms.CharField(required=False)
	source_type=forms.DateField(required=False)
	publisher=forms.DateField(required=False)
	country=forms.CharField(required=False)
	ASJS=forms.CharField(required=False)
	language=forms.CharField(required=False)
	Theme=forms.CharField(required=False)
class FileForm(forms.Form):
	Exc=forms.FileField(required=False)	

