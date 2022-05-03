import hashlib
import os
from flask import Flask, render_template, redirect, request

from data import db_session
from data.users import User
from data.jobs import Jobs
from data.registerform import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'db/mars_explorer.db')
db_session.global_init(filename)


@app.route('/')
@app.route('/index')
def index():
    param = {'data': []}
    db_sess = db_session.create_session()
    for job in db_sess.query(Jobs).all():
        if job.work_size == 1:
            ws = 'hour'
        else:
            ws = 'hours'
        if job.is_finished:
            isf = 'Is finished'
        else:
            isf = 'Is not finished'
        param['data'].append(
            {'id': job.id, 'Title of activity': job.job, 'Team leader': f'{job.user.name} {job.user.surname}',
             'Duration': f'{job.work_size} {ws}', 'List of collaborators': job.collaborators,
             'Is finished': isf})
    return render_template('index.html', title='Journal', param=param)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if request.method == 'POST' and form.validate():
            user = User()
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.position = form.position.data
            user.speciality = form.speciality.data
            user.address = form.address.data
            user.email = form.email.data
            user.hashed_password = hashlib.md5(form.password.data.encode()).hexdigest()
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Registration', form=form)


if __name__ == '__main__':
    app.run(debug=True)
