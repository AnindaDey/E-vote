from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Candidate
from ..forms import CandidateForm

class CandidateListView(ListView):
    model = Candidate
    template_name = 'candidate/candidate_list.html'
    context_object_name = 'candidates'

class CandidateCreateView(CreateView):
    model = Candidate
    form_class = CandidateForm
    template_name = 'candidate/candidate_form.html'
    success_url = reverse_lazy('candidate_list')

class CandidateUpdateView(UpdateView):
    model = Candidate
    form_class = CandidateForm
    template_name = 'candidate/candidate_form.html'
    success_url = reverse_lazy('candidate_list')

class CandidateDeleteView(DeleteView):
    model = Candidate
    template_name = 'candidate/confirm_delete.html'
    success_url = reverse_lazy('candidate_list')
