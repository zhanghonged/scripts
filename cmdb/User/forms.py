#coding:utf-8
from django import forms
from django.forms import ValidationError
from models import CMDBUser


class Register(forms.Form):
    username = forms.CharField(
        max_length=32,
        min_length=6,
        label='用户名',
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'用户名'})
    )
    password = forms.CharField(
        max_length=32,
        min_length=6,
        label='密码',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'密码'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = CMDBUser.objects.get(username=username)
        except:
            return username
        else:
            raise ValidationError('用户名已存在')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password.isdigit():
            raise ValidationError('密码不可以完全由数字组成')
        elif password.isalnum():
            raise ValidationError('密码不可以完全由数字字母组成')
        else:
            return password