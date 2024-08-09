from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from comments.forms import CommentForm
from django.shortcuts import redirect
from comments.models import Comentarios
from django.shortcuts import render

# Create your views here.
"""
def lista_comentarios(request):
    comentarios = Comentarios.objects.all()
    return render(request, 'comments/list.html', {'comentarios': comentarios})

def formulario(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confirmacion')
    else:
        form = CommentForm()

    return render(request, 'comments/form.html', {'form' : form})

def confirmacion (request):
    return render(request, 'comments/confirmation.html')
"""

class Lista_comentarios (ListView):
    model = Comentarios
    template_name = "comments/list.html"

class DetalleComentario (DetailView):
    model = Comentarios
    template_name = "comments/detail.html"

class EditarComentario (UpdateView):
    model = Comentarios
    fields = ["nombre","email","comentario"]
    template_name = "comments/edit.html"
    success_url = reverse_lazy("lista_comentarios")

class BorrarComentario (DeleteView):
    model = Comentarios
    template_name = "comments/comments_check_delete.html"
    success_url = reverse_lazy("lista_comentarios")

class Formulario(CreateView):
    model = Comentarios
    fields = ["nombre","email", "comentario"]
    template_name  = "comments/form.html"
    success_url = reverse_lazy("confirmacion")

class Confirmacion (View):
    def get(self,request):
        return render(request, "comments/confirmation.html")
