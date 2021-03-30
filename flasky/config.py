import os


connect = 'mysql+pymysql://root:wwq13849841939@127.0.0.1:3306/'

class Config:   
    #Flask-WTF配置
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    #SQLite数据库配置
    SQLALCHEMY_TRACK_MODIFICIATIONS = False    
    #设置下方这行code后，在每次请求结束后会自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_ADMIN = 1  
    
    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                            connect+'实验室预约管理系统-开发'
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                            connect+'实验室预约管理系统-测试'
                        
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                                            connect+'实验室预约管理系统-生产'
                        
config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        
        'default': DevelopmentConfig
        }