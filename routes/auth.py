from models.user import User
# from models.topic import Topic
from routes import *

# for decorators
from functools import wraps


main = Blueprint('auth', __name__)

Model = User


def current_user():
    uid = session.get('uid')
    if uid is not None:
        u = Model.query.get(uid)
        return u


@main.route('/')
def index():
    return render_template('auth_index.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = Model(form)
    user = Model.query.filter_by(username=u.username).first()
    if u.valid_login(user):
        session.permanent = True
        session['uid'] = user.id
        return redirect(url_for('node.index'))
    else:
        return redirect(url_for('.index'))


@main.route('/logout', methods=['GET'])
def logout():
    session['uid'] = ''
    return redirect(url_for('.index'))


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = Model(form)
    x, y = u.valid()
    if x:
        print('auth register\n', u, '111')
        u.save()
        session.permanent = True
        session['uid'] = u.id
        return redirect(url_for('node.index'))
    else:
        return render_template('auth_index.html', msgs=y)


@main.route('/profile', methods=['GET'])
def profile():
    u = current_user()
    if u is not None:
        print('profile', u.id, u.username, u.password)
        return render_template('profile.html', user=u)
    else:
        return redirect(url_for('.index'))


@main.route('/update_password', methods=['POST'])
def update_password():
    u = current_user()
    password = request.form.get('password', '')
    print('password', password)
    if u.change_password(password):
        print('修改成功')
    else:
        print('用户密码修改失败')
    return render_template('profile.html', user=u)


@main.route('/update_avatar', methods=['POST'])
def update_avatar():
    u = current_user()
    avatar = request.form.get('avatar', '')
    print('password', avatar)
    if u.change_avatar(avatar):
        print('修改成功')
    else:
        print('用户密码修改失败')
    return render_template('profile.html', user=u)

