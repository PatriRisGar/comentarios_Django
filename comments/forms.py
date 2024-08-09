from comments.models import Comentarios
from django import forms


class CommentForm(forms.ModelForm):

    class Meta:
        model =  Comentarios
        fields = ("nombre","email","comentario",)