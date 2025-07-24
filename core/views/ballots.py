from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Ballot
from ..forms import BallotForm

class BallotListView(ListView):
    model = Ballot
    template_name = 'ballot/ballot_list.html'
    context_object_name = 'ballots'

class BallotCreateView(CreateView):
    model = Ballot
    form_class = BallotForm
    template_name = 'ballot/ballot_form.html'
    success_url = reverse_lazy('ballot_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Add'
        return context

class BallotUpdateView(UpdateView):
    model = Ballot
    form_class = BallotForm
    template_name = 'ballot/ballot_form.html'
    success_url = reverse_lazy('ballot_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit'
        return context

class BallotDeleteView(DeleteView):
    model = Ballot
    template_name = 'ballot/ballot_confirm_delete.html'
    success_url = reverse_lazy('ballot_list')
    context_object_name = 'ballot'