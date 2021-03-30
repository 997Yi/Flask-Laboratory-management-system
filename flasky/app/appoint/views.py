# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from . import appoint
from flask_login import login_required, current_user
from ..models import Permission, LabAppoint, StuLabAppoint, StuLab
from .forms import Stu_CheckAppointmentForm, Teacher_CheckAppointmentForm, \
                        Stu_AppointForm,Teacher_AppointForm

@appoint.route('/appoint', methods=['GET', 'POST'])
@login_required
def appointOld():
    checkStuForm = Stu_CheckAppointmentForm()
    checkTeaForm = Teacher_CheckAppointmentForm()
    appStuForm = Stu_AppointForm()
    appTeaForm = Teacher_AppointForm()
    if request.method == 'POST':
        if checkStuForm.validate_on_submit:        
            stuAppList = StuLabAppoint.query.all()
            for stuApp in stuAppList:
                if not stuApp.isNotAppointed(checkStuForm.startTime.data, checkStuForm.endTime.data, 
                                                 checkStuForm.labNo.data, checkStuForm.comNo.data):
                    flash('该实验室已被预约')
                    return redirect(url_for('appoint.appoint'))
            flash('该实验室未被预约')
            return redirect(url_for('appoint.appoint'))
        if checkTeaForm.validate_on_submit:
            teaAppList = LabAppoint.query.all()
            for teaApp in teaAppList:
                if not teaApp.isNotAppointed(checkTeaForm.date.data, checkTeaForm.howClass.data, checkTeaForm.labNo.data):
                    flash('该实验室已被预约')
                    return redirect(url_for('appoint.appoint'))
            flash('该实验室未被预约')
            return redirect(url_for('appoint.appoint'))
        
        if appStuForm.validate_on_submit:
            stuAppList = StuLabAppoint.query.all()
            for stuApp in stuAppList:
                if not stuApp.isNotAppointed(checkStuForm.startTime.data, checkStuForm.endTime.data, 
                                                 checkStuForm.labNo.data, checkStuForm.comNo.data):
                    flash('该实验室已被预约')
                    return redirect(url_for('appoint.appoint'))
            StuLabAppoint.addApp(checkStuForm.startTime.data, checkStuForm.endTime.data, 
                                                 checkStuForm.labNo.data, checkStuForm.comNo.data, current_user.id)
            flash('预约成功')
            return redirect(url_for('appoint.appoint'))
        if appTeaForm.validate_on_submit:
            teaAppList = LabAppoint.query.all()
            for teaApp in teaAppList:
                if not teaApp.isNotAppointed(checkTeaForm.date.data, checkTeaForm.howClass.data, checkTeaForm.labNo.data):
                    flash('该实验室已被预约')
                    return redirect(url_for('appoint.appoint'))
            LabAppoint.addApp(checkTeaForm.date.data, checkTeaForm.howClass.data, checkTeaForm.labNo.data, current_user.id)
            flash('预约成功')
            return redirect(url_for('appoint.appoint'))
    return render_template('appoint/appoint.html', page=4, perm=Permission, 
                           checkStuForm=checkStuForm, checkTeaForm=checkTeaForm,
                           appStuForm=appStuForm, appTeaForm=appTeaForm)
  
@appoint.route('/appointNew', methods=['GET', 'POST'])
@login_required
def appointNew():
    labNo = 1
    stuLabList = StuLab.query.filter_by(labNo=labNo).all()
    return render_template('appoint/appointNew.html', page=4, stuLabList=stuLabList, labNo=labNo)