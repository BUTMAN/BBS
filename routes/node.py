from models.node import Node
from models.user import User
from routes import *

# for decorators
from functools import wraps


main = Blueprint('node', __name__)

Model = Node


def current_user():
    uid = session.get('uid')
    print('session uid', uid)
    if uid is not None:
        u = User.query.get(uid)
        return u


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        u = current_user()
        if u.id != 1:
            print('not admin', u)
            abort(404)
        print('admin', u)
        return f(*args, **kwargs)
    return function


@main.route('/')
def index():
    u = current_user()
    ms = Model.query.all()
    if u is None:
        return redirect(url_for('.index'))
    return render_template('bbs_index.html', node_list=ms, user=u)


@main.route('/<int:id>')
def show(id):
    print('show node, ', id, type(id))
    u = current_user()
    m = Model.query.get(id)
    print(id, m)
    return render_template('node.html', node=m, user=u)


# 以下路由需要管理员权限操作
@main.route('/admin')
@admin_required
def admin():
    ms = Model.query.all()
    return render_template('node_index.html', node_list=ms)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model(form)
    m.save()
    return redirect(url_for('.admin'))


@main.route('/edit/<id>')
def edit(id):
    n = Model.query.get(id)
    return render_template('node_edit.html', node=n)


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    t = Model.query.get(id)
    t.update(form)
    return redirect(url_for('.admin'))


@main.route('/delete/<int:id>')
def delete(id):
    t = Model.query.get(id)
    t.delete()
    return redirect(url_for('.admin'))
