from django.contrib import admin
from .models import Employee, Position, Candidate, Vote, Ballot,Election

admin.site.register(Employee)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register(Ballot)
admin.site.register(Election)