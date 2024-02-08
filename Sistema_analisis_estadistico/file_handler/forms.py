import csv
import os
from django import forms

class CargaCSVForm(forms.Form):
    archivo_csv = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv'}), label='Sube tu dataset en formato CSV')

    def clean_archivo_csv(self):
        file = self.cleaned_data['archivo_csv']
        extension = os.path.splitext(file.name)[1]
        if not extension.lower() == ".csv":
            raise forms.ValidationError('Solo se admiten archivos CSV.')
        return file