from flask_wtf import FlaskForm
from wtforms.fields import (EmailField, PasswordField, StringField, SubmitField, SelectField, TextAreaField)


categories = [
  ('covid', 'Corona Vírus'),
  ('cinema', 'Cinema'),
  ('ciencia', 'Ciência'),
  ('saude', 'Saúde'),
  ('musica', 'Música'),
  ('seguranca_publica', 'Segurança Pública'),
  ('educacao', 'Educação'),
  ('tecnologia', 'Tecnologia'),
  ('meio_ambiente', 'Meio Ambiente'),
  ('cultura', 'Cultura'),
  ('geografia', 'Geografia'),
  ('financas', 'Finanças')
]

spheres = [
  ('Global', 'Global'),
  ('Federal', 'Federal'),
  ('Estadual', 'Estadual'),
  ('Municipal', 'Municipal'),
]


class LoginUser(FlaskForm):
  email = EmailField('E-mail')
  password = PasswordField('Senha')
  submit = SubmitField('Entrar')


class RegisterUser(FlaskForm):
  username = StringField('Nome de usuário')
  email = EmailField('E-mail')
  password = PasswordField('Senha')
  submit = SubmitField('Cadastre-se')


class DataRegister(FlaskForm):
  title = StringField('Título')
  category = SelectField('Categorias', choices=categories)
  page_link = StringField('Link da página oficial')
  description = TextAreaField('Descrição')
  sphere = SelectField('Esfera', choices=spheres)
  country = StringField('País')
  state = StringField('Estado')
  city = StringField('Cidade')
  submit = SubmitField('Registrar Fonte')