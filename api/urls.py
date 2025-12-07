from django.urls import path
from .views import chat, test_data_view, retrieve_answer

urlpatterns = [
    path("chat/", chat, name="chat"),
    path("test-data/", test_data_view),
    path("retrieve/", retrieve_answer),
]
