from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] ='secret-key'
db = SQLAlchemy(app)

#models for data
class PasswordManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(520), nullable=False)
    site_url = db.Column(db.String(520), nullable=False)
    password = db.Column(db.String(520), nullable=False)


    def __repr__(self):
        return '<PasswordManager %r>' % self.email

#routes
@app.route('/')
def index():
    passwordList = PasswordManager.query.all()
    return render_template("index.html", passwordList=passwordList)

@app.route('/add', methods=['GET', 'POST'])
def add_details():
    if request.method == 'POST':
        email = request.form['email']
        site_url = request.form['site_url']
        password = request.form['password']
        new_password_details = PasswordManager(email=email, site_url=site_url, password=password)
        db.session.add(new_password_details)
        db.session.commit()
        return redirect("/")



@app.route('/update')
def  update_details():
    return "Hello World"


@app.route('/delete')
def  delete_details():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)     # run our app in debug mode