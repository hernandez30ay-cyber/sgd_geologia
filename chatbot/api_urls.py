from django.urls import path
from .views_api import chatbot_api
from .views_docs import chatbot_doc_api
from .views_search import chatbot_search_api
from .views_report import chatbot_doc_report

urlpatterns = [
    path("", chatbot_api, name="chatbot_api"),
    path("documents/", chatbot_doc_api, name="chatbot_doc_api"),
    path("search/", chatbot_search_api, name="chatbot_search_api"),
    path("documents/report/", chatbot_doc_report, name="chatbot_doc_report"),
]
