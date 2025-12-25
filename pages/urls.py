from django.urls import path
from .views import (
    PageListView,
    PageDetailView,
    PageCreateView,
    PageUpdateView,
    PageDeleteView
)

app_name = "pages"

urlpatterns = [
    # Cambiado 'list' por 'page_list' para que coincida con el Navbar
    path("", PageListView.as_view(), name="page_list"),
    
    # Cambiado 'detail' por 'page_detail' para ser más descriptivo
    path("<int:pk>/", PageDetailView.as_view(), name="page_detail"),
    
    path("create/", PageCreateView.as_view(), name="page_create"),
    path("<int:pk>/update/", PageUpdateView.as_view(), name="page_update"),
    path("<int:pk>/delete/", PageDeleteView.as_view(), name="page_delete"),
]