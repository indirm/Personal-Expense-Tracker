from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total = sum(e.amount for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
            exp = Expense(date=date, description=request.form['description'],
                          amount=float(request.form['amount']), category=request.form['category'])
            db.session.add(exp)
            db.session.commit()
        except:
            pass
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    exp = Expense.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)