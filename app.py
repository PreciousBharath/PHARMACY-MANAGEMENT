from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf import FlaskForm
import pandas as pd
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretpharmacykey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='Pharmacist')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Medicine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(400))
    uses = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(300), nullable=True, default='https://via.placeholder.com/150')
    emoji = db.Column(db.String(50), nullable=True, default='💊')


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicine.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    sold_at = db.Column(db.DateTime, default=datetime.utcnow)
    medicine = db.relationship('Medicine')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class MedicineForm(FlaskForm):
    name = StringField('Medicine Name', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=[
        ('Pain Relief', 'Pain Relief'),
        ('Cold & Flu', 'Cold & Flu'),
        ('Digestive Care', 'Digestive Care'),
        ('Supplements', 'Supplements'),
        ('Antibiotics', 'Antibiotics'),
        ('Antihistamines', 'Antihistamines'),
        ('Antacids', 'Antacids'),
        ('Cough Suppressants', 'Cough Suppressants'),
        ('Other', 'Other')
    ])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=0)])
    price = FloatField('Price (₹)', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description')
    uses = TextAreaField('What it cures / Uses')
    image_url = StringField('Image URL (Optional)')
    submit = SubmitField('Save Medicine')


class SaleForm(FlaskForm):
    medicine_id = SelectField('Medicine', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity Sold', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Record Sale')


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back, {}!'.format(user.username), 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing:
            flash('Username or email already exists.', 'warning')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration complete. Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    medicines = Medicine.query.count()
    total_stock = sum([m.quantity for m in Medicine.query.all()])
    total_sales = Sale.query.count()
    revenue = sum([sale.total for sale in Sale.query.all()])
    top_medicines = db.session.query(Medicine.name, db.func.sum(Sale.quantity).label('sold'))
    top_medicines = top_medicines.join(Sale).group_by(Medicine.id).order_by(db.desc('sold')).limit(5).all()
    all_medicines = Medicine.query.all()
    return render_template('dashboard.html', medicines=medicines, total_stock=total_stock,
                           total_sales=total_sales, revenue=revenue, top_medicines=top_medicines, all_medicines=all_medicines)


@app.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    form = MedicineForm()
    if form.validate_on_submit():
        medicine = Medicine(
            name=form.name.data,
            category=form.category.data,
            quantity=form.quantity.data,
            price=form.price.data,
            description=form.description.data,
            uses=form.uses.data,
            image_url=form.image_url.data or 'https://via.placeholder.com/150'
        )
        db.session.add(medicine)
        db.session.commit()
        flash('Medicine added successfully.', 'success')
        return redirect(url_for('inventory'))
    items = Medicine.query.order_by(Medicine.name).all()
    return render_template('inventory.html', form=form, items=items)


@app.route('/inventory/delete/<int:item_id>')
@login_required
def delete_inventory(item_id):
    item = Medicine.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Medicine removed from inventory.', 'info')
    return redirect(url_for('inventory'))


@app.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    form = SaleForm()
    medicines = Medicine.query.order_by(Medicine.name).all()
    form.medicine_id.choices = [(m.id, f'{m.name} ({m.quantity} in stock)') for m in medicines]
    if form.validate_on_submit():
        medicine = Medicine.query.get(form.medicine_id.data)
        if not medicine or form.quantity.data > medicine.quantity:
            flash('Insufficient stock or invalid medicine selection.', 'danger')
        else:
            medicine.quantity -= form.quantity.data
            sale_total = form.quantity.data * medicine.price
            sale = Sale(medicine_id=medicine.id, quantity=form.quantity.data, total=sale_total)
            db.session.add(sale)
            db.session.commit()
            flash('Sale recorded successfully.', 'success')
            return redirect(url_for('sales'))
    sales = Sale.query.order_by(Sale.sold_at.desc()).limit(20).all()
    return render_template('sales.html', form=form, sales=sales)


@app.route('/reports')
@login_required
def reports():
    sales = Sale.query.order_by(Sale.sold_at.desc()).all()
    medicines = Medicine.query.order_by(Medicine.name).all()
    return render_template('reports.html', sales=sales, medicines=medicines)


@app.route('/analytics')
@login_required
def analytics():
    top_categories = db.session.query(Medicine.category, db.func.sum(Sale.quantity).label('sold'))
    top_categories = top_categories.join(Sale).group_by(Medicine.category).order_by(db.desc('sold')).all()
    stock_composition = db.session.query(Medicine.category, db.func.sum(Medicine.quantity).label('stock'))
    stock_composition = stock_composition.group_by(Medicine.category).all()
    return render_template('analytics.html', top_categories=top_categories, stock_composition=stock_composition)


@app.route('/forecast', methods=['GET', 'POST'])
@login_required
def forecast():
    forecast_data = None
    coefficients = None
    error_message = None
    if request.method == 'POST':
        window = int(request.form.get('window', 7))
        sales = Sale.query.order_by(Sale.sold_at.asc()).all()
        if len(sales) < 5:
            error_message = 'Not enough sales data to build a forecast model.'
        else:
            data = pd.DataFrame([{'date': s.sold_at.date(), 'quantity': s.quantity} for s in sales])
            daily = data.groupby('date')['quantity'].sum().reset_index()
            daily['day_index'] = range(1, len(daily) + 1)
            X = daily[['day_index']]
            y = daily['quantity']
            model = LinearRegression()
            model.fit(X, y)
            future_days = list(range(len(daily) + 1, len(daily) + 1 + window))
            preds = model.predict(pd.DataFrame({'day_index': future_days}))
            forecast_data = [{'day': i + 1, 'predicted': max(0, round(float(pred), 2))} for i, pred in enumerate(preds)]
            coefficients = {'intercept': round(float(model.intercept_), 2), 'slope': round(float(model.coef_[0]), 2)}
    return render_template('forecast.html', forecast_data=forecast_data, coefficients=coefficients, error_message=error_message)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


def initialize_database():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@pharmacy.com', password_hash=generate_password_hash('admin123'))
            db.session.add(admin)
            db.session.commit()
        if Medicine.query.count() == 0:
            sample_data = [
                Medicine(name='Aspirin', category='Pain Relief', quantity=120, price=35, description='Fast-acting analgesic tablet.', uses='Headaches, fever, mild body pain and inflammation relief', emoji='🩹'),
                Medicine(name='Vitamin C', category='Supplements', quantity=75, price=150, description='Immune support vitamin tablets.', uses='Boosts immune system, prevents common cold and flu', emoji='🍊'),
                Medicine(name='Cough Syrup', category='Cold & Flu', quantity=50, price=125, description='Soothes sore throat and cough.', uses='Cough suppression, sore throat relief and bronchial comfort', emoji='🤧'),
                Medicine(name='Antacid', category='Digestive Care', quantity=90, price=45, description='Quick relief from heartburn and acidity.', uses='Treats acid reflux, heartburn and stomach acidity', emoji='🫀'),
                Medicine(name='Amoxicillin', category='Antibiotics', quantity=60, price=280, description='Broad-spectrum antibiotic capsule.', uses='Bacterial infections, respiratory tract infections and urinary tract infections', emoji='💉'),
                Medicine(name='Paracetamol', category='Pain Relief', quantity=100, price=25, description='Common painkiller and fever reducer.', uses='Fever reduction, headaches, body aches and mild pain relief', emoji='💊'),
                Medicine(name='Ibuprofen', category='Pain Relief', quantity=80, price=55, description='Anti-inflammatory pain reliever.', uses='Severe pain relief, inflammation reduction and arthritis pain', emoji='🧪'),
                Medicine(name='Antihistamine', category='Antihistamines', quantity=70, price=85, description='Allergy relief medication.', uses='Allergies, hay fever, urticaria and itching relief', emoji='👃'),
                Medicine(name='Multivitamin', category='Supplements', quantity=110, price=200, description='Complete daily nutrition supplement.', uses='Daily nutritional support and overall health boost', emoji='💪'),
                Medicine(name='Cough Drops', category='Cough Suppressants', quantity=95, price=50, description='Medicated throat lozenges.', uses='Sore throat relief, cough suppression and throat soothing', emoji='🍯'),
                Medicine(name='Omeprazole', category='Digestive Care', quantity=65, price=180, description='Stomach acid reducer tablet.', uses='GERD treatment, ulcer healing and acid reflux prevention', emoji='🔴'),
                Medicine(name='Cetirizine', category='Antihistamines', quantity=55, price=95, description='Non-drowsy allergy medication.', uses='Seasonal allergies, chronic urticaria and allergy symptoms', emoji='👁️'),
            ]
            db.session.add_all(sample_data)
            db.session.commit()


if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
