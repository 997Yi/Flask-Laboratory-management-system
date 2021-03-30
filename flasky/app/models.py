from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
import time
import datetime
#from flask_sqlalchemy import func

class Permission:
    STUDENT_LAB = 1
    COURSE_LAB = 2
    ADMIN = 4

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)#权限
    
    users = db.relationship('User', backref='role')
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    
    #权限操作
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    #移除权限        
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm
    
    #重置权限
    def reset_permission(self):
        self.permissions = 0
    
    #检验是否有权限
    def has_permission(self, perm):
        return self.permissions & perm == perm
    
    #创建角色
    @staticmethod
    def insert_roles():
        roles = {
                'Student':[Permission.STUDENT_LAB],
                'Teacher':[Permission.COURSE_LAB, Permission.STUDENT_LAB],
                'Administrator':[Permission.ADMIN, Permission.COURSE_LAB, Permission.STUDENT_LAB]
                }
        default_role = 'Student'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
    
    def __repr__(self):
        return '<Role %r>'%self.name
    
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.String(12), unique=True, index=True)
    name = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    
    
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    administrators = db.relationship('Administrator', backref='user')
    labAppoint = db.relationship('LabAppoint', backref='user')
    stuLabAppoint = db.relationship('StuLabAppoint', backref='user')
    #赋予角色
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            
            为管理员赋予角色
            if self.id == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
     
    
    #检查用户是否有指定权限
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    
    #检查用户是否是管理员
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    #拒绝读取密码
    @property
    def password(self):
        raise AttributeError('密码不是一个可读属性')
  
    #设置密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    #检验密码    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User %r>'%self.sno

#匿名用户
class AnonymousUser(AnonymousUserMixin):
    #检查用户是否有指定权限
    def can(self, permissions):
        return False
    
    #检查用户是否是管理员
    def is_administrator(self):
        return False

#管理员表
class Administrator(db.Model):
    __tablename__ = 'administrators'   
    
    id = db.Column(db.Integer, primary_key=True)
    adminNo = db.Column(db.Integer, unique=True)
    
    userId = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    admin = db.relationship('Admin', backref='administrator')
    notice = db.relationship('Notice', backref='administrator')

#实验室表
class Laboratory(db.Model):
    __tablename__ = 'laboratories'
    id = db.Column(db.Integer, primary_key=True)
    labNo = db.Column(db.Integer, unique=True)
    isUse = db.Column(db.Boolean, default=True)
    labType = db.Column(db.String(12))

    admin = db.relationship('Admin', backref='laboratory')
    labAppoint = db.relationship('LabAppoint', backref='laboratory')
    stuLab = db.relationship('StuLab', backref='laboratory')
    stuLabAppoint = db.relationship('StuLabAppoint', backref='laboratory')
    
#管理表
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)#model必须要有主键
    
    adminNo = db.Column(db.Integer, db.ForeignKey('administrators.adminNo'))
    labNo = db.Column(db.Integer, db.ForeignKey('laboratories.labNo'))
            
#课程实验室预约表
class LabAppoint(db.Model):
    __tablename__ = 'labAppoint'
    id = db.Column(db.Integer, primary_key=True)#model必须要有主键
    date = db.Column(db.Date)
    howClass = db.Column(db.Integer)
    
    userId = db.Column(db.Integer,db.ForeignKey('users.id'))
    labNo = db.Column(db.Integer, db.ForeignKey('laboratories.labNo'))
    
    #课程实验室是否被预约
    def isNotAppointed(self, date, howClass, labNo):
        if self.date==date and self.howClass==howClass and self.labNo==labNo:
            return False
        return True
    
    @staticmethod
    def addApp(newDate, newHowClass, newLabNo, userId):
        newApp = LabAppoint(date=newDate, howClass=newHowClass, labNo=newLabNo, userId=userId)
        db.session.add(newApp)
        db.session.commit()
        
#学生实验室表
class StuLab(db.Model):
    __tablename__ = 'stuLabs'
    id = db.Column(db.Integer, primary_key=True)
    comNo = db.Column(db.Integer, unique=True)
    isUse = db.Column(db.Boolean, default=True)
    
    labNo = db.Column(db.Integer, db.ForeignKey('laboratories.labNo'))

    stuLabAppoint = db.relationship('StuLabAppoint', backref='stuLab')
        
#学生实验室预约表
class StuLabAppoint(db.Model):
    __tablename__ = 'stuLabAppoint'
    id = db.Column(db.Integer, primary_key=True)#model必须要有主键
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    useReason = db.Column(db.Text(200))
    
    userId = db.Column(db.Integer,db.ForeignKey('users.id'))
    labNo = db.Column(db.Integer, db.ForeignKey('laboratories.labNo'))
    comNo = db.Column(db.Integer, db.ForeignKey('stuLabs.comNo'))
    
    #学生实验室是否被预约
    def isNotAppointed(self, startTime, endTime, labNo, comNo):
        '''
        self.startTime = func.from_unixtime((self.startTime), "%Y-%m-%d %H:%M:%S")
        self.endTime = func.from_unixtime((self.endTime), "%Y-%m-%d %H:%M:%S")
        startTime = func.from_unixtime((startTime), "%Y-%m-%d %H:%M:%S")
        endTime = func.from_unixtime((endTime), "%Y-%m-%d %H:%i:%s")
        self.startTime = time.mktime(time.strptime(self.startTime.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
        self.endTime = time.mktime(time.strptime(self.endTime.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
        startTime = time.mktime(time.strptime(startTime.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
        endTime = time.mktime(time.strptime(endTime.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
        
        if self.labNo != labNo or self.comNo != comNo\
            or (startTime >= self.endTime and endTime >= self.endTime)\
            or (startTime <= self.startTime and endTime <= self.startTime):
            return True
        '''
        return False
    
    @staticmethod
    def addApp(newStartTime, newEndTime, newLabNo, newComNo, userId):
        newApp = StuLabAppoint(startTime=newStartTime, endTime=newEndTime, labNo=newLabNo, comNo=newComNo, userId=userId)
        db.session.add(newApp)
        db.session.commit()
#公告表
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)#model必须要有主键
    __tablename__ = 'notices'
    content = db.Column(db.Text(200))
    
    adminNo = db.Column(db.Integer, db.ForeignKey('administrators.adminNo'))
    
#加载用户的函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.anonymous_user = AnonymousUser


