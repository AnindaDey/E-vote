from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView
from ..models import Employee, OTP, Vote, Ballot,Position
from ..forms import PhoneForm, OTPForm
from django.shortcuts import redirect

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

def logout_view(request):
    # Clear only the session data related to OTP login
    request.session.flush()
    return redirect('login_phone')  # Or wherever your login starts


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

        # All positions that the employee hasn't voted for
        voted_positions = Vote.objects.filter(voter=employee).values_list("position_id", flat=True)
        available_positions = Position.objects.exclude(id__in=voted_positions)

        context["employee"] = employee
        context["positions"] = available_positions
        return context


class PositionBallotsView(TemplateView):
    template_name = "position_ballots.html"

    def dispatch(self, request, *args, **kwargs):
        if "employee_id" not in request.session:
            return redirect("login_phone")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = get_object_or_404(Employee, id=self.request.session["employee_id"])
        position_id = self.kwargs["position_id"]
        position = get_object_or_404(Position, id=position_id)

        # Check if already voted for this position
        if Vote.objects.filter(voter=employee, position=position).exists():
            messages.info(self.request, "You have already voted for this position.")
            return redirect("vote_page")

        ballots = Ballot.objects.filter(position=position)

        context["employee"] = employee
        context["position"] = position
        context["ballots"] = ballots
        return context



class VoteBallotView(View):
    template_name = "vote_ballot.html"

    def get(self, request, ballot_id):
        employee = self._get_employee(request)
        if not employee:
            return redirect("login_phone")

        ballot = get_object_or_404(Ballot, id=ballot_id)

        # Check if this employee has already voted for this position
        if Vote.objects.filter(voter=employee, position=ballot.position).exists():
            messages.info(
                request,
                f"You have already voted for the position '{ballot.position.title}'."
            )
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

        # Check if already voted for this position
        if Vote.objects.filter(voter=employee, position=ballot.position).exists():
            messages.info(
                request,
                f"You have already voted for the position '{ballot.position.title}'."
            )
            return redirect("vote_page")

        # Create the vote
        Vote.objects.create(
            voter=employee,
            ballot=ballot,
            election=ballot.election,
            position=ballot.position
        )

        messages.success(
            request,
            f"Your vote for {ballot.candidate.employee.name} ({ballot.symbol}) in {ballot.position.title} has been recorded."
        )
        return redirect("vote_page")

    def _get_employee(self, request):
        employee_id = request.session.get("employee_id")
        if not employee_id:
            return None
        return get_object_or_404(Employee, id=employee_id)
