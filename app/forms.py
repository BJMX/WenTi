# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from app.models import User

"""
登录表单：
1、用户名
2、密码
3、登录按钮
"""


class LoginForm(FlaskForm):
    name = StringField(
        label='用户名',
        validators=[
            DataRequired('用户名不能为空')
        ],
        description='用户名',
        render_kw={
            'class': 'form-control',
            'placeholder': '你的用户名'
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('密码不能为空')
        ],
        description='密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '密码'
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            'class': 'btn btn-primary btn-block'
        }
    )

    # 自定义校验函数
    def validate_password(self, field):
        pwd = field.data
        user = User.query.filter_by(username=self.name.data).first()
        if not user.check_pwd(pwd):
            raise ValidationError('密码不正确')


"""
注册表单：
1、用户名
2、邮箱
3、密码
4、确认密码
5、注册按钮
"""


class RegisterForm(FlaskForm):
    name = StringField(
        label='用户名',
        validators=[
            DataRequired('用户名不能为空')
        ],
        description='用户名',
        render_kw={
            'class': 'form-control',
            'placeholder': '用户名'
        }
    )
    email = StringField(
        label='邮箱',
        validators=[
            Email('邮箱格式不正确')
        ],
        description='邮箱',
        render_kw={
            'class': 'form-control',
            'type': 'email',
            'placeholder': '你的邮箱'
        }
    )
    password = PasswordField(
        label='密码',
        validators=[
            DataRequired('密码不能为空')
        ],
        description='密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '密码'
        }
    )
    confirmpwd = PasswordField(
        label='确认密码',
        validators=[
            EqualTo('password', '密码不一致')
        ],
        description='确认密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '确认密码'
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class': 'btn btn-success btn-block'
        }
    )


"""
提问表单：
1、标题
2、标签
3、问题描述详情
"""


class QuestionForm(FlaskForm):
    title = StringField(
        label='标题',
        validators=[
            DataRequired('标题不能为空')
        ],
        description='标题',
        render_kw={
            'class': 'form-control',
            'placeholder': '标题'
        }
    )
    cate = SelectField(
        label='标签',
        description='标签',
        choices=[(1, '生活'), (2, '影视'), (3, '技术'), (4, '文艺'), (5, '娱乐'), (6, '其他')],
        default=1,
        coerce=int,
        render_kw={
            'class': 'form-control'
        }
    )
    detail = TextAreaField(
        label='问题描述',
        validators=[
            DataRequired('详情不能为空')
        ],
        description='问题描述',
        render_kw={
            'class': 'form-control',
            'rows': '5',
            'placeholder': '详情'
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


"""
闪念标签：
1、内容
2、提交按钮
"""


class SparkForm(FlaskForm):
    spark = TextAreaField(
        label='此刻闪念',
        validators=[
            DataRequired('内容不能为空')
        ],
        description='此刻闪念',
        render_kw={
            'class': 'form-control',
            'rows': '5',
            'placeholder': '闪念'
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary'
        }
    )


"""
评论
1、内容
2、提交按钮
"""


class CommentForm(FlaskForm):
    comment = TextAreaField(
        label='评论',
        validators=[
            DataRequired('评论不能为空')
        ],
        description='评论',
        render_kw={
            'class': 'form-control',
            'rows': '2',
            'placeholder': '评论'
        }
    )
    submit = SubmitField(
        '提交',
        render_kw={
            'class': 'btn btn-primary'
        }
    )
