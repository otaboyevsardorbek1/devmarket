from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo, Optional

class LoginForm(FlaskForm):
    email = StringField('Elektron Pochta', validators=[DataRequired(), Email()])
    password = PasswordField('Parol', validators=[DataRequired()])
    remember_me = BooleanField('Meni eslab qol')
    submit = SubmitField('Kirish')

class RegistrationForm(FlaskForm):
    username = StringField('Foydalanuvchi nomi', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Elektron Pochta', validators=[DataRequired(), Email()])
    password = PasswordField('Parol', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Parolni Tasdiqlash', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Ro\'yxatdan o\'tish')

class ProductForm(FlaskForm):
    title = StringField('Mahsulot Nomi', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Tavsif', validators=[DataRequired()])
    price = DecimalField('Narx ($)', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Kategoriya', choices=[
        ('projects', 'Dasturiy Loyihalar'),
        ('hardware', 'Kompyuter Texnikasi'),
        ('components', 'Komponentlar'),
        ('accessories', 'Aksessuarlar')
    ], validators=[DataRequired()])
    condition = SelectField('Holati', choices=[
        ('new', 'Yangi'),
        ('used', 'Ishlatilgan'),
        ('refurbished', 'Qayta tiklanga')
    ], validators=[DataRequired()])
    image_url = StringField('Rasm URL (ixtiyoriy)', validators=[Optional()])
    submit = SubmitField('Mahsulotni qo\'shish')

class ReviewForm(FlaskForm):
    content = TextAreaField('Sharh', validators=[DataRequired()])
    rating = IntegerField('Reyting (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Sharhni joylash')