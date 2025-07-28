from django.urls import path

from .views.views import (
    LoginPhoneView,
    VerifyOTPView,
    VotePageView,
    VoteBallotView,
    PositionBallotsView,
    logout_view,
)
from .views.elections import (
    ElectionListView,
    ElectionCreateView,
    ElectionUpdateView,
    ElectionDeleteView,
)
from .views.employees import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
)
from .views.candidates import (
    CandidateListView,
    CandidateCreateView,
    CandidateUpdateView,
    CandidateDeleteView,
)
from .views.ballots import (
    BallotListView,
    BallotCreateView,
    BallotUpdateView,
    BallotDeleteView,
)
from .views.dashboard import admin_dashboard_view
from .views.positions import (
    PositionListView,
    PositionCreateView,
    PositionUpdateView,
    PositionDeleteView,
)
from .views.votes import vote_result_view
urlpatterns = [
    path("login/", LoginPhoneView.as_view(), name="login_phone"),
    path("verify/", VerifyOTPView.as_view(), name="verify_otp"),
    path("vote/", VotePageView.as_view(), name="vote_page"),
    path("vote/<int:ballot_id>/", VoteBallotView.as_view(), name="vote_ballot"),
    path('manage/elections/', ElectionListView.as_view(), name='election_list'),
    path(
        'manage/elections/add/',
        ElectionCreateView.as_view(),
        name='election_add'
    ),
    path(
        'manage/elections/<int:pk>/edit/',
        ElectionUpdateView.as_view(),
        name='election_edit'
    ),
    path(
        'manage/elections/<int:pk>/delete/',
        ElectionDeleteView.as_view(),
        name='election_delete'
    ),
    path(
        'manage/employees/',
        EmployeeListView.as_view(),
        name='employee_list'
    ),
    path(
        'manage/employees/add/',
        EmployeeCreateView.as_view(),
        name='employee_add'
    ),
    path(
        'manage/employees/<int:pk>/edit/',
        EmployeeUpdateView.as_view(),
        name='employee_edit'),
    path(
        'manage/employees/<int:pk>/delete/',
        EmployeeDeleteView.as_view(),
        name='employee_delete'
    ),
    path(
        'manage/candidates/',
        CandidateListView.as_view(),
        name='candidate_list'
    ),
    path(
        'manage/candidates/add/',
        CandidateCreateView.as_view(),
        name='candidate_add'
    ),
    path(
        'manage/candidates/<int:pk>/edit/',
        CandidateUpdateView.as_view(),
        name='candidate_edit'
    ),
    path(
        'manage/candidates/<int:pk>/delete/',
        CandidateDeleteView.as_view(),
        name='candidate_delete'
    ),
    path(
        'manage/ballots/',
        BallotListView.as_view(),
        name='ballot_list'
    ),
    path(
        'manage/ballots/add/',
        BallotCreateView.as_view(),
        name='ballot_add'),
    path(
        'manage/ballots/<int:pk>/edit/',
        BallotUpdateView.as_view(),
        name='ballot_edit'
    ),
    path('manage/ballots/<int:pk>/delete/',
         BallotDeleteView.as_view(),
         name='ballot_delete'
         ),
    path('manage/dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('manage/positions/', PositionListView.as_view(), name='position_list'),
    path('manage/positions/add/', PositionCreateView.as_view(), name='position_add'),
    path('manage/positions/edit/<int:pk>/', PositionUpdateView.as_view(), name='position_edit'),
    path('manage/positions/delete/<int:pk>/', PositionDeleteView.as_view(), name='position_delete'),
    path('manage/results/', vote_result_view, name='vote_results'),
    path("vote/position/<int:position_id>/", PositionBallotsView.as_view(), name="position_ballots"),
    path("vote/ballot/<int:ballot_id>/", VoteBallotView.as_view(), name="vote_ballot"),
    path('logout/', logout_view, name='logout_view'),


]
