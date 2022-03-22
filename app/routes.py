from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models.DataSource import DataSource
from app.models.User import User
from app.forms import DataRegister, LoginUser, RegisterUser, categories



def init_app(app):

  # index

  @app.route('/')
  def index():
    return render_template('index.html', categories=categories)

  # autenticacão

  @app.route('/register/', methods=('GET', 'POST'))
  def register():

    if current_user.is_active:
      return redirect(url_for('index'))

    form = RegisterUser()

    if form.validate_on_submit():

      username = User.query.filter_by(username=form.username.data).first()
      email = User.query.filter_by(email=form.email.data).first()

      if username:
        flash(f'@{form.username.data} já está sendo usado')
        return redirect(url_for('register'))

      if email:
        flash(f'o email {form.email.data} já está sendo usado')
        return redirect(url_for('register'))

      user = User()

      user.username = form.username.data
      user.email = form.email.data
      user.password = generate_password_hash(form.password.data)

      db.session.add(user)
      db.session.commit()

      login_user(user)
      return redirect(url_for('index'))

    return render_template('register.html', form=form)

  @app.route('/login/', methods=('GET', 'POST'))
  def login():

    if current_user.is_active:
      return redirect(url_for('index'))

    form = LoginUser()

    if form.validate_on_submit():

      user = User.query.filter_by(email=form.email.data).first()

      if not user:
        flash(f'o email {form.email.data} não foi cadastrado')
        return redirect(url_for('login'))

      if not check_password_hash(user.password, form.password.data):
        flash('Senha incorreta')
        return redirect(url_for('login'))
      
      login_user(user)
      return redirect(url_for('index'))

    return render_template('login.html', form=form)

  @app.route('/logout/')
  def logout():
    logout_user()
    return redirect(url_for('index'))


  # perfil

  @app.route('/profile/')
  def profile_view():

    form = RegisterUser()

    user = User.query.filter_by(id=current_user.id).first()

    form.username.data = user.username
    form.email.data = user.email

    return render_template('profile.html', user=user, form=form)

  @app.route('/profile/edit', methods=('GET', 'POST'))
  def profile_edit():

    form = RegisterUser()

    user = User.query.filter_by(id=current_user.id).first()

    form.username.data = user.username
    form.email.data = user.email

    return render_template('profile_edit.html', user=user, form=form)

  @app.route('/profile/edit/submit/', methods=('GET', 'POST'))
  def submit_edit_profile():

    form = RegisterUser()

    user = User.query.filter_by(id=current_user.id).first()

    if form.validate_on_submit():

      if User.query.filter_by(email=form.email.data).first():
        if form.email.data != user.email:
          flash(f'o email {form.email.data} já está sendo usado')
          return redirect(url_for('.profile.profile_edit'))

      if User.query.filter_by(username=form.username.data).first():
        if form.username.data != user.username:
          flash(f'@{form.username.data} já está sendo usado')
          return redirect(url_for('.profile.profile_edit'))

      user.username = form.username.data
      user.email = form.email.data

      db.session.commit()

      return redirect(url_for('.profile_view'))

  @app.route('/profile/delete')
  def profile_delete():

    user = User.query.filter_by(id=current_user.id).first()

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('index'))

  # data sources

  @app.route('/fontes/<category>/<id>/')
  def data_source(id, category):
    source = DataSource.query.filter_by(id=id).first()
    return render_template('fonte.html', source=source, category=category)

  @app.route('/fontes/<category>/')
  def data_category_view(category):
    
    data_sources = DataSource.query.filter_by(category=category)

    for cat in categories:
      if cat[0] == category:
        c = cat

    return render_template('fonte_categoria.html', data_sources=data_sources, category=c)

  @app.route('/fontes/registrar/', methods=('GET', 'POST'))
  def data_source_register():
    form = DataRegister()

    if form.validate_on_submit():
      
      source = DataSource()

      source.title = form.title.data
      source.description = form.description.data
      source.category = form.category.data
      source.country = form.country.data
      source.state = form.state.data
      source.city = form.city.data
      source.page_link = form.page_link.data
      source.sphere = form.sphere.data
      
      db.session.add(source)
      db.session.commit()

      return redirect(url_for('data_source', id=source.id, category=source.category))

    return render_template('registrar_fonte.html', form=form)

  @app.route('/fonte/<id>/editar/', methods=('GET', 'POST'))
  def data_source_edit(id):
    form = DataRegister()

    source = DataSource.query.filter_by(id=id).first()

    form.title.data = source.title
    form.description.data = source.description
    form.category.data = source.category
    form.country.data = source.country
    form.state.data = source.state
    form.city.data = source.city
    form.page_link.data = source.page_link
    form.sphere.data = source.sphere

    return render_template('editar_fontes.html', form=form, source=source)

  @app.route('/fonte/<id>/editar/enviar/', methods=('GET', 'POST'))
  def submit_data_source_edit(id):

    form = DataRegister()

    if form.validate_on_submit():

      source = DataSource.query.filter_by(id=id).first()

      source.title = form.title.data
      source.description = form.description.data
      source.category = form.category.data
      source.country = form.country.data
      source.state = form.state.data
      source.city = form.city.data
      source.page_link = form.page_link.data
      source.sphere = form.sphere.data

      db.session.commit()

      return redirect(url_for('data_source', id=source.id, category=source.category))

  @app.route('/fontes/delete/<id>/')
  def delete_data_source(id):
    source = DataSource.query.filter_by(id=id).first()
    db.session.delete(source)
    db.session.commit()

    return redirect(url_for('index'))
