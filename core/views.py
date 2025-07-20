from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from .models import Employee, OTP, Vote, Ballot
from .forms import PhoneForm, OTPForm


# --- Helper function ---
def send_otp(phone, code):
    print(f"OTP for {phone}: {code}")


# --- OTP Login Flow ---

class LoginPhoneView(FormView):
    template_name = "login_phone.html"
    form_class = PhoneForm
    success_url = reverse_lazy("verify_otp")

    def form_valid(self, form):
        phone = form.cleaned_data["phone"]
        if not Employee.objects.filter(phone=phone).exists():
            messages.error(self.request, "Phone number not registered.")
            return self.form_invalid(form)
        code = OTP.generate_code()
        OTP.objects.create(phone=phone, code=code)
        send_otp(phone, code)
        self.request.session["phone"] = phone
        return super().form_valid(form)


class VerifyOTPView(FormView):
    template_name = "verify_otp.html"
    form_class = OTPForm
    success_url = reverse_lazy("vote_page")

    def dispatch(self, request, *args, **kwargs):
        if "phone" not in request.session:
            return redirect("login_phone")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        phone = self.request.session.get("phone")
        code = form.cleaned_data["code"]
        otp = OTP.objects.filter(phone=phone, code=code).last()
        if otp and otp.is_valid():
            employee = Employee.objects.get(phone=phone)
            self.request.session["employee_id"] = employee.id
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid or expired OTP.")
            return self.form_invalid(form)


# --- Voting Flow ---

class VotePageView(TemplateView):
    template_name = "vote.html"

    def dispatch(self, request, *args, **kwargs):
        if "employee_id" not in request.session:
            return redirect("login_phone")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = get_object_or_404(Employee, id=self.request.session["employee_id"])
        voted_ids = Vote.objects.filter(voter=employee).values_list('ballot_id', flat=True)
        available_ballots = Ballot.objects.exclude(id__in=voted_ids)
        context["employee"] = employee
        context["ballots"] = available_ballots
        return context


class VoteBallotView(View):
    template_name = "vote_ballot.html"

    def get(self, request, ballot_id):
        employee = self._get_employee(request)
        if not employee:
            return redirect("login_phone")

        ballot = get_object_or_404(Ballot, id=ballot_id)

        # Already voted check
        if Vote.objects.filter(voter=employee, ballot=ballot).exists():
            messages.info(request, f"You have already voted for {ballot.position.title} (Ballot #{ballot.ballot_no}).")
            return redirect("vote_page")

        return render(request, self.template_name, {
            "employee": employee,
            "ballot": ballot
        })

    def post(self, request, ballot_id):
        employee = self._get_employee(request)
        if not employee:
            return redirect("login_phone")

        ballot = get_object_or_404(Ballot, id=ballot_id)

        # Double vote protection
        if Vote.objects.filter(voter=employee, ballot=ballot).exists():
            messages.info(request, f"You already voted for this ballot.")
            return redirect("vote_page")

        Vote.objects.create(voter=employee, ballot=ballot)
        messages.success(request, f"Your vote for {ballot.candidate.employee.name} ({ballot.symbol}) in {ballot.position.title} has been recorded.")
        return redirect("vote_page")

    def _get_employee(self, request):
        employee_id = request.session.get("employee_id")
        if not employee_id:
            return None
        return get_object_or_404(Employee, id=employee_id)




from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Election, Position, Employee, Candidate, Ballot
from .forms import ElectionForm  # We'll create this next


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

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Employee
from .forms import EmployeeForm  # Create this form

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'employees'

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employee/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Candidate
from .forms import CandidateForm

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



from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Ballot
from .forms import BallotForm

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


from django.shortcuts import render
from .models import Employee, Candidate, Position, Election, Ballot

def admin_dashboard_view(request):
    context = {
        'employee_count': Employee.objects.count(),
        'candidate_count': Candidate.objects.count(),
        'position_count': Position.objects.count(),
        'election_count': Election.objects.count(),
        'ballot_count': Ballot.objects.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)
