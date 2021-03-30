# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length
#from wtforms import ValidationError#自定义检测

class Stu_CheckAppointmentForm(FlaskForm):
    startTime = DateTimeField('开始时间', validators=[DataRequired()])
    endTime = DateTimeField('结束时间',  validators=[DataRequired()])
    labNo = IntegerField('实验室号', validators=[DataRequired(), Length(12)])
    comNo = IntegerField('计算机号', validators=[DataRequired(), Length(12)])
    submit = SubmitField('查询')

class Teacher_CheckAppointmentForm(FlaskForm):
    date = DateTimeField('预约日期', validators=[DataRequired()])
    howClass = IntegerField('课程选择', validators=[DataRequired(), Length(12)])
    labNo = IntegerField('实验室号', validators=[DataRequired(), Length(12)])
    submit = SubmitField('查询')
    
class Stu_AppointForm(FlaskForm):
    startTime = DateTimeField('开始时间', validators=[DataRequired()])
    endTime = DateTimeField('结束时间',  validators=[DataRequired()])
    labNo = IntegerField('实验室号', validators=[DataRequired(), Length(12)])
    comNo = IntegerField('计算机号', validators=[DataRequired(), Length(12)])
    submit = SubmitField('预约')
    
class Teacher_AppointForm(FlaskForm):
    date = DateTimeField('预约日期', validators=[DataRequired()])
    howClass = IntegerField('课程选择', validators=[DataRequired(), Length(12)])
    labNo = IntegerField('实验室号', validators=[DataRequired(), Length(12)])
    submit = SubmitField('预约')