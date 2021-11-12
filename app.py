import re
from flask import Flask, render_template, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager, login_user
from flask_login import logout_user,login_required,UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =  SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class students(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=False)
    name = db.Column(db.String(80))
    stream = db.Column(db.String(80))

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return students.get(int(user_id))

@app.route('/create',methods=['POST'])
def create():
    if(request.method == 'POST'):
        print(request.json)
        id = request.json['id']
        name = request.json['name']
        stream = request.json['stream']
        if(db.session.query(db.exists().where(students.id==id)).scalar()):
            return "id already exists"
        else:
            student=students(id=id,name=name,stream=stream)
            db.session.add(student)
            db.session.commit()
            return "added sucessfully"

@app.route('/read',methods=['GET'])
def read():
    records=students.query.all()
    if(len(records)==0):
        return "No students enrolled yet"
    for student in records:
        ans={}    
        ans[str(student.id)] = {
        "name": student.name, "stream": student.stream}
    return jsonify(ans)

@app.route('/update',methods=['PUT'])
def update():
    student = students.query.filter_by(id=request.json['id']).first()
    if(student):
        db.session.delete(student)
        db.session.commit()

        id=request.json['id']
        name=request.json['name']
        stream=request.json['stream']
        record=students(id=id,name=name,stream=stream)
        db.session.add(record)
        db.session.commit()

        return "Update success"

    else:
        return "id not found"

@app.route('/delete',methods=['DELETE'])
def delete():
    student = students.query.filter_by(id=request.json['id']).first()
    if(student):
        db.session.delete(student)
        db.session.commit()
        return "Delete success"
    else:
        return "id not found"

if(__name__=='__main__'):
    app.run(port=8000,debug=True)




