import os
from app import create_app,db
from app.models import User
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand



app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    
@manager.command
def seeds():
         db.session.add(User(username='123123',password='123456'))

@manager.command
def dev():
    from livereload import Server
    app.debug = True
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)         
if __name__=='__main__':
    manager.run()
    
