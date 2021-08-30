from django.urls import path
from .views import (
    CuestListView,
    cuest_view,
    cuest_data_view,
    save_cuest_view,
)

app_name = 'quizes'

urlpatterns = [
    path('', CuestListView.as_view(), name='main-view'),
    path('<pk>/', cuest_view, name='quiz-view'),
    path('<pk>/save/', save_cuest_view, name='save-view'),
    path('<pk>/data/', cuest_data_view, name='cuest-data-view'),
]