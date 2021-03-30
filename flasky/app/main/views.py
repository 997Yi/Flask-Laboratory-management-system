from flask import render_template, redirect
from . import main
from flask_login import login_required
from ..models import LabAppoint, StuLabAppoint, Notice
from ..decorators import admin_required

@main.route('/', methods=['GET', 'POST'])
def index():
    noticeList = Notice.query.all()
    return render_template('index.html',page=1, noticeList=noticeList)

@main.route('/sysinfo')
def sysInfo():
    return render_template('sysInfo.html', page=2)

#添加
@main.route('/appointList')
@login_required
@admin_required
def appointList():
    appStuList = StuLabAppoint.query.all()
    appTeaList = LabAppoint.query.all()
    return render_template('appointList.html', page=3, 
                           appStuList=appStuList, appTeaList=appTeaList)