import os
from app import create_app, db
from app.models import User, Role, AnonymousUser
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

#shell上下文处理器
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


