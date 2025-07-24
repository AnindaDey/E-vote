from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from ..models import Position
from ..forms import PositionForm

class PositionListView(ListView):
    model = Position
    template_name = 'positions/position_list.html'
    context_object_name = 'positions'

class PositionCreateView(CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'positions/position_form.html'
    success_url = reverse_lazy('position_list')

class PositionUpdateView(UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'positions/position_form.html'
    success_url = reverse_lazy('position_list')

class PositionDeleteView(DeleteView):
    model = Position
    template_name = 'position/sposition_confirm_delete.html'
    success_url = reverse_lazy('position_list')