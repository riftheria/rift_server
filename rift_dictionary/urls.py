from django.urls import path, include
from rift_dictionary import views
urlpatterns = [
    path('<str:word>/', views.DictionaryView.as_view()),
]
