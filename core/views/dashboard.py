from django.shortcuts import render
from ..models import Employee, Candidate, Position, Election, Ballot,Vote

def admin_dashboard_view(request):
    context = {
        'employee_count': Employee.objects.count(),
        'candidate_count': Candidate.objects.count(),
        'position_count': Position.objects.count(),
        'election_count': Election.objects.count(),
        'ballot_count': Ballot.objects.count(),
        "vote_count": Vote.objects.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)