from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # Example: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # Example: /pools/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # Example: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # Example: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
