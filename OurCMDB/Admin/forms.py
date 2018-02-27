#coding:utf-8
import re
from django import forms
from django.forms import ValidationError
from models import User

class Register(forms.Form):
    username = forms.CharField(
        max_length = 32,
        min_length = 6,
        label = '用户名',
        widget = forms.TextInput(attrs={"class" : "form-control","placeholder":"用户名"})
    )
    password = forms.CharField(
        max_length = 32,
        min_length = 6,
        label = '密码',
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"})
    )
    phone = forms.CharField(
        max_length = 11,
        min_length = 11,
        label = '手机号',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "手机号"})
    )
    photo = forms.ImageField(
        label = '用户头像'
    )
    email = forms.EmailField(
        label = '用户邮箱',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户邮箱"}),
        error_messages={
            'invalid':'请填写有效邮箱地址'
        }
    )

    def clean_username(self):
        '''
        检测用户名是否重复
        '''
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            return username
        else:
            raise ValidationError('用户名已存在')

    def clean_phone(self):
        '''
        检测手机号是否重复
        '''
        phone = self.cleaned_data.get('phone')
        try:
            user = User.objects.get(phone = phone)
        except:
            return phone
        else:
            raise ValidationError('手机号已注册')

    def clean_password(self):
        '''
        表单验证常用的方法 raise
        常用的错误类型 forms.ValidationsError
        '''
        password = self.cleaned_data.get('password') #获取要判断的值
        if password.isdigit():
            raise ValidationError('密码不可以由纯数字组成')
        elif password.isalnum():
            raise ValidationError('密码不可以由字母加数字组成')
        else:
            return password  #返回要判断的值

    def clean_email(self):
        '''
        检测email格式是否正确，及是否已注册
        '''
        email = self.cleaned_data.get('email')
        res = re.match(r"\w+@\w+\.\w+",email)
        if res:
            try:
                user = User.objects.get(email = email)
            except:
                return email
            else:
                raise ValidationError('邮箱已注册')
        else:
            raise ValidationError('请输入正确邮箱')