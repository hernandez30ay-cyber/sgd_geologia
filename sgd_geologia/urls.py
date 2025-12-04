from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from sgd_geologia.views import home, login_view, logout_view, projects_view, documents_view, chatbot_ui

urlpatterns = [

    # HOME Y LOGIN
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # FRONTEND HTML
    path("projects/", projects_view, name="projects"),
    path("documents/", documents_view, name="documents"),
    path("chatbot_ui/", chatbot_ui, name="chatbot_ui"),

    # API REST
    path("api/projects/", include("projects.api_urls")),
    path("api/documents/", include("documents.urls")),
    path("api/chatbot/", include("chatbot.api_urls")),
    path("api/accounts/", include("accounts.urls")),

    # ADMIN
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
