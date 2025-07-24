from django import forms
from .models import Candidate, Election, Employee, Candidate, Ballot, Position

class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=15, label="Phone Number")

class OTPForm(forms.Form):
    code = forms.CharField(max_length=6, label="OTP Code")

class VoteForm(forms.Form):
    candidate = forms.ChoiceField(label="Select Candidate")

    def __init__(self, *args, **kwargs):
        position = kwargs.pop('position')
        super().__init__(*args, **kwargs)
        candidates = Candidate.objects.filter(position=position)
        self.fields['candidate'].choices = [(c.id, c.employee.name) for c in candidates]



class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'start_date', 'end_date']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['employee']



class BallotForm(forms.ModelForm):
    class Meta:
        model = Ballot
        fields = ['election', 'ballot_no', 'symbol', 'position', 'candidate']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

