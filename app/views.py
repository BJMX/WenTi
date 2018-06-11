# coding:utf8
from flask import Flask, render_template, redirect, session, request, url_for
import app.config as config
from app.models import db, User, Question, Spark, Comment
from app.forms import LoginForm, RegisterForm, QuestionForm, SparkForm, CommentForm
from werkzeug.security import generate_password_hash
import datetime
from functools import wraps

app = Flask(__name__)
app.config.from_object(config)


# 登录限制装饰器
def login_require(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper


@app.route('/')
@login_require
def home():
    context = {
        'questions': Question.query.all()
    }
    return render_template('home.html', title='首页', **context)


@app.route('/home_spark')
@login_require
def home_spark():
    context = {
        'sparks': Spark.query.all()
    }
    return render_template('home_spark.html', title='首页', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session['user'] = data['name']
        return redirect('/')
    return render_template('login.html', title='登录', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            username=data['name'],
            password=generate_password_hash(data['password']),
            email=data['email'],
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html', title='注册', form=form)


@app.route('/logout', methods=['GET'])
@login_require
def logout():
    session.pop('user', None)
    return redirect('/login')


@app.route('/ask', methods=['GET', 'POST'])
@login_require
def ask_question():
    form = QuestionForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=session['user']).first()
        user_id = user.id
        question = Question(
            title=data['title'],
            label=data['cate'],
            detail=data['detail'],
            author_id=user_id,
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(question)
        db.session.commit()
        return redirect('/')

    return render_template('ask.html', title='提问', form=form)


@app.route('/spark', methods=['GET', 'POST'])
@login_require
def spark():
    form = SparkForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(username=session['user']).first()
        user_id = user.id
        sparks = Spark(
            text=data['spark'],
            author_id=user_id,
            addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(sparks)
        db.session.commit()
        return redirect('/home_spark')

    return render_template('sparks.html', title='闪念', form=form)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
@login_require
def question_detail(question_id):
    question = Question.query.filter_by(id=question_id).first()
    user_name = session['user']
    return render_template('question_detail.html', question=question, user_name=user_name)


@app.route('/question_comment', methods=['POST'])
@login_require
def q_comment():
    conent = request.form.get('q_comment')
    question_id = request.form.get('question_id')
    user = User.query.filter_by(username=session['user']).first()
    user_id = user.id
    comments = Comment(
        comment=conent,
        author_id=user_id,
        question_id=question_id,
        addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    db.session.add(comments)
    db.session.commit()

    return redirect(url_for('question_detail', question_id=question_id))


@app.route('/spark/<spark_id>', methods=['GET', 'POST'])
@login_require
def spark_detail(spark_id):
    sparks = Spark.query.filter_by(id=spark_id).first()
    return render_template('spark_detail.html', id=spark_id, spark=sparks)


if __name__ == '__main__':
    app.run()
