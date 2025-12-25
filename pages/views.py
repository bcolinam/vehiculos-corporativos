from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Page


class PageListView(ListView):
    model = Page
    template_name = "pages/page_list.html"
    context_object_name = "pages"


class PageDetailView(DetailView):
    model = Page
    template_name = "pages/page_detail.html"


class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    template_name = "pages/page_form.html"
    fields = ["titulo", "subtitulo", "contenido", "imagen"]
    success_url = reverse_lazy("pages:list")

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Page
    template_name = "pages/page_form.html"
    fields = ["titulo", "subtitulo", "contenido", "imagen"]
    success_url = reverse_lazy("pages:list")


class PageDeleteView(LoginRequiredMixin, DeleteView):
    model = Page
    template_name = "pages/page_confirm_delete.html"
    success_url = reverse_lazy("pages:list")

