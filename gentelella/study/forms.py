from django import forms



class StudyForm(forms.Form):
    matrixFile = forms.FileField(label='Upload targets file', required=False)