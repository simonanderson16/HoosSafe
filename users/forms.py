from django.utils import timezone
from django import forms
from .models import Report
from django.forms.widgets import FileInput, TextInput, DateInput, TimeInput, Textarea


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ReportForm(forms.ModelForm):
    files = MultipleFileField(widget=MultipleFileInput(attrs={'class': 'custom-file-input'}), label='File(s):')
    location = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'custom-text-input',
        'placeholder': 'Enter Location'
    }), max_length=100)
    
    date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'custom-date-input'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        present_day = timezone.localdate()
        self.fields['date'].widget.attrs['max'] = present_day.isoformat()
    
    time = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'class': 'custom-time-input'}))
    
    CHOICES = (
        ("1", "Harassment"),
        ("2", "Bullying"),
        ("3", "Hazing"),
        ("4", "Discrimination/Racial Bias"),
        ("5", "Accessibility Issues"),
        ("6", "Food Quality or Sanitation"),
        ("7", "Unsafe Behavior at Social Gatherings"),
        ("8", "Poorly Lit Areas"),
        ("9", "Other: Please Specify when Explaining")
    )
    type_of_violation = forms.ChoiceField(choices=CHOICES, widget=forms.Select(), label='Type')
    explain = forms.CharField(widget=Textarea(attrs={
        'class': 'custom-textarea',
        'rows': 4}))
    
    class Meta:
        model = Report
        fields = ['title', 'location', 'date', 'time', 'type_of_violation', 'explain', 'files']


# class ReportForm(forms.ModelForm):
#     file = forms.FileField(widget=FileInput(attrs={'class': 'custom-file-input'}), label='File:')
#     location = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'custom-text-input',
#         'placeholder': 'Enter Location'
#     }), max_length=100)
    
#     date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'custom-date-input'}))
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         present_day = timezone.localdate()
#         self.fields['date'].widget.attrs['max'] = present_day.isoformat()
    
#     time = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'class': 'custom-time-input'}))
    
#     CHOICES = (
#         ("1", "Harassment"),
#         ("2", "Bullying"),
#         ("3", "Hazing"),
#         ("4", "Discrimination/Racial Bias"),
#         ("5", "Accessibility Issues"),
#         ("6", "Food Quality or Sanitation"),
#         ("7", "Unsafe Behavior at Social Gatherings"),
#         ("8", "Poorly Lit Areas"),
#         ("9", "Other: Please Specify when Explaining")
#     )
#     type_of_violation = forms.ChoiceField(choices=CHOICES, widget=forms.Select(), label='Type')
#     explain = forms.CharField(widget=Textarea(attrs={
#         'class': 'custom-textarea',
#         'rows': 4}))
    
#     class Meta:
#         model = Report
#         fields = ['file', 'location', 'date', 'time', 'type_of_violation', 'explain']

class AdminForm(forms.Form):
    note = forms.CharField(widget=Textarea(attrs={
        'class': 'custom-textarea',
        'rows': 4}))