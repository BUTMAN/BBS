from models.topic import Topic
from routes import *
from models.user import User


def current_user():
    uid = session.get('uid')
    if uid is not None:
        u = User.query.get(uid)
        return u

main = Blueprint('topic', __name__)

Model = Topic


# @main.route('/')
# def index():
#     ms = Model.query.all()
#     return render_template('topic_index.html', node_list=ms)


@main.route('/new/<int:id>')
def new(id):
    u = current_user()
    return render_template('topic_new.html', node_id=id, user=u)


@main.route('/<int:id>')
def show(id):
    u = current_user()
    m = Model.query.get(id)
    print('topic show', m)
    return render_template('topic.html', topic=m, user=u)


@main.route('/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form
    m = Model(form)
    m.node_id = int(form.get('node_id'))
    m.user_id = u.id
    m.save()
    return redirect(url_for('node.show', id=m.node_id))
