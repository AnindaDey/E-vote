from django.db.models import Count
from django.shortcuts import render
from ..models import Position, Ballot, Vote, Election

def vote_result_view(request):
    elections = Election.objects.filter(is_deleted=False, is_active=True)
    result_data = []

    for election in elections:
        positions = Position.objects.filter(is_deleted=False, is_active=True)
        election_data = {'election': election, 'positions': []}

        for position in positions:
            ballots = (
                Ballot.objects.filter(position=position, election=election)
                .annotate(vote_count=Count('vote'))
                .order_by('-vote_count')
            )

            if ballots.exists():
                election_data['positions'].append({
                    'position': position,
                    'ballots': ballots
                })

        if election_data['positions']:
            result_data.append(election_data)

    return render(request, 'votes/vote_results.html', {
        'result_data': result_data
    })