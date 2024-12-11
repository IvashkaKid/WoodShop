"""
Definition of forms.
"""

from cProfile import label
from dataclasses import fields
#from tkinter import Label, Widget
from urllib import request
from xml.dom.minidom import Attr
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

from django.db import models
from .models import Comment

from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=50)
    phone = forms.CharField(label='Ваш номер телефона', validators=[RegexValidator(r'^\d{11}$', message='Номер телефона должен содержать ровно 11 цифр')])
    gender = forms.ChoiceField(label='Ваш пол', choices=[('1', 'Мужской'), ('2', 'Женский')], widget= forms.RadioSelect, initial=1)
    visit = forms.ChoiceField(label='Как давно вы совершали покупки у нас?', choices=[('1', 'В течение месяца'), ('2', 'Больше месяца назад'), ('3', 'Ещё ничего не покупал')], widget= forms.RadioSelect, initial=1)
    notice = forms.BooleanField(label='Хотите получать рекламные предложения на WhatsApp?', required=False)
    message = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'rows': 12, 'cols': 20}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Комментарий"}

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {
            'title': "Заголовок",
            'description': "Краткое содержание",
            'content': "Полное содержание",
            'image': "Картинка"
        }
