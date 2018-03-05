#coding:utf-8
import re
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
    email = forms.EmailField(
        max_length=32,
        min_length=6,
        label='邮箱',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'邮箱'})
    )
    phone = forms.CharField(
        max_length=11,
        min_length=11,
        label='电话',
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'电话'})
    )
    photo = forms.ImageField(label='用户头像')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        try:
            user = CMDBUser.objects.get(phone=phone)
        except:
            return phone  #不存在返回手机号
        else:
            raise ValidationError('手机号已存在')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password.isdigit():
            raise ValidationError('密码不可以完全由数字组成')
        elif password.isalnum():
            raise ValidationError('密码不可以完全由数字字母组成')
        else:
            return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        res = re.match(r'\w+@\w+\.\w+]',email)
        if res:
            return email
        else:
            raise ValidationError('邮箱格式错误')
