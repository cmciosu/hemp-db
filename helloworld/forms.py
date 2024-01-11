# forms.py a Django form to handle file uploads
from django import forms
from helloworld.models import Company

class FileUploadForm(forms.ModelForm):
    # file = forms.FileField()

    class Meta:
        model = Company
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Status"].widget.attrs.update({"class": "form-control"})