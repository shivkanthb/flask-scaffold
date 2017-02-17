import os
from flask import Flask, render_template, request, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.inspection import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/flask_test'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<E-mail %r>' % self.email


@app.route("/")
def hello():
	return render_template('index.html')
    # return "Hello world!"

@app.route("/getall")
def getall():
    data = User.query.all()
    data_all = []
    for user in data:
        data_all.append({"id":user.id, "email":user.email}) #prepare visual data
    return jsonify(users=data_all)

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email = None
        email = request.form['email']
    return render_template('404.html')

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        email = None
        email = request.form['email']
        password = request.form['password']
        print password
        if not db.session.query(User).filter(User.email == email).count():
            import pdb
            pdb.set_trace()
            reg = User(email,password)
            db.session.add(reg)
            db.session.commit()
            usr = db.session.query(User).filter(User.email == email).all()
            return jsonify({'message' : 'cool'})
        else:
            return jsonify({'message':'user exists already'})

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    manager.run()
    app.run(host='0.0.0.0', port=port)