# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from captcha.fields import CaptchaField
from ..models import User


class Login(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"用户名",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
            }
        ),
    )
    captcha = CaptchaField()

    def get(self, request):
        return render(request, 'anime/login.html', {'form': self})

    def post(self, request):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
            if user is not None and not user.is_active:
                return render(request, 'anime/login.html', {'form': self, 'loginError': True})
            request.session['user'] = username
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'anime/index.html', {'invalidForm': True})

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"登录错误")
        clean_data = super(Login, self).clean()
        username = clean_data.get('username')
        password = clean_data.get('password')
        try:
            staff = User.objects.get(username__exact=username)
        except:
            raise forms.ValidationError(u"用户不存在或密码错误")
        if not check_password(password, staff.password):
            raise forms.ValidationError(u"密码错误")
        return clean_data
