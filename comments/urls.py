from django.urls import path
from comments.views import Confirmacion,Formulario, Lista_comentarios, DetalleComentario, EditarComentario,BorrarComentario


urlpatterns = [
    path('',Lista_comentarios.as_view(), name='lista_comentarios'),
    path('detalleComentario/<int:pk>', DetalleComentario.as_view(), name='detalleComentario'),
    path('editarComentario/<int:pk>', EditarComentario.as_view(), name='editarComentario'),
    path('borrarComentario/<int:pk>/', BorrarComentario.as_view(), name = 'borrarComentario'),
    path('formulario/', Formulario.as_view(), name='formulario'),
    path('confirmacion/', Confirmacion.as_view(), name='confirmacion'),
]
