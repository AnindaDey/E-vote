from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from ..models import Election
from ..forms import ElectionForm  # We'll create this next


# Admin mixin
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
class ElectionListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Election
    template_name = "elections/election_list.html"
    context_object_name = 'elections'


class ElectionCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Election
    form_class = ElectionForm
    template_name = 'elections/election_form.html'
    success_url = reverse_lazy('election_list')


class ElectionUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Election
    form_class = ElectionForm
    template_name = 'elections/election_form.html'
    success_url = reverse_lazy('election_list')


class ElectionDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Election
    template_name = 'elections/election_confirm_delete.html'
    success_url = reverse_lazy('election_list')