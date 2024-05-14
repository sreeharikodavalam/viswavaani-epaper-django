from django import forms
from .models import Edition


class EditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = ['name']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if Edition.objects.filter(name=name, is_main=True).exists():
            raise forms.ValidationError(
                'Main edition with this name already exists.')


class SubEditionForm(forms.ModelForm):
    class Meta:
        model = Edition
        fields = ['name', 'parent']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if Edition.objects.filter(name=name, is_main=False).exists():
            raise forms.ValidationError(
                'Sub edition with this name already exists.')
        return cleaned_data
