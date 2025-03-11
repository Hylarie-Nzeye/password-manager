from flask import Flask, render_template, request, send_file, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import csv
import time
timestr= time.strftime("%Y%m%d-%H%M%S")

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



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def  update_details(id):
    update_details = PasswordManager.query.get_or_404(id)
    if request.method == 'POST':
        update_details.email = request.form['email']
        update_details.site_url = request.form['site_url']
        update_details.password = request.form['password']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was a problem updating  Password "
    else:
        return render_template('update.html', update_details=update_details)



@app.route('/delete/<int:id>')
def  delete_details(id):
    new_details_to_delete = PasswordManager.query.get_or_404(id)
    try:
        db.session.delete(new_details_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting that task"

@app.route('/export')
def export_data():
    # Crée un fichier CSV
    with open('dump.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Écrire l'en-tête
        writer.writerow(['id', 'email', 'site_url', 'password'])
        
        # Écrire chaque ligne du modèle PasswordManager
        for item in PasswordManager.query.all():
            writer.writerow([item.id, item.email, item.site_url, item.password])
    
    # Renvoi du fichier CSV comme téléchargement
    return send_file('dump.csv',
                     mimetype='text/csv',
                     download_name=f"Export_password_{timestr}.csv",
                     as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)     # run our app in debug mode