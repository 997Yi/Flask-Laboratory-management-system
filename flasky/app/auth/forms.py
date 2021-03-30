# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import ValidationError#自定义检测
from ..models import User


class LoginForm(FlaskForm):
    sno = StringField('学号', validators=[DataRequired(), Length(12)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')