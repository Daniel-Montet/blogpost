from app import create_app, db
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand
from flask_socketio import SocketIO,send

app,socketio =create_app('development')

manager = Manager(app)
migrate = Migrate(app,db)
# manager = Manager(socketio)
# migrate = Migrate(socketio,db) 

manager.add_command('server',Server)
manager.add_command('db',MigrateCommand)

# @socketio.on('message')
# def handleMessage(msg):
#     print('Message' + msg)

if __name__ == "__main__":
    manager.run()