from flask import Flask, render_template, request, redirect, flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'kasper'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    number = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(200), nullable = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Contact %r' % self.id

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        address = request.form['address']
        new_contact = Contacts(name=name, number=number, address = address)
        if not name or not number:
            flash('Name and Number are mandatory', "error")
            return redirect('/')
        
        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Contact Added Successfully', "success")
            return redirect('/')
        except:
            return 'There was a problem adding this contact'     


    
    else:    
        contacts = Contacts.query.order_by(Contacts.date_created).all()
        return render_template('index.html', contacts = contacts)
    

@app.route('/delete/<int:id>')
def delete(id):
    contact_to_delete = Contacts.query.get_or_404(id)
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that contact'
    
@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    contact_to_update = Contacts.query.get_or_404(id)
    if request.method == 'POST':
        contact_to_update.name = request.form['name']
        contact_to_update.number = request.form['number']
        contact_to_update.address = request.form['address']

        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There was a problem updating this contact'
    else:
        return render_template('update.html', contact = contact_to_update)

if __name__ == '__main__':
    app.run(debug=True)
