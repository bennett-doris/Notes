from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,TextAreaField
from wtforms.validators import DataRequired,Length,equal_to

# 注册表单
class RegisterForm(FlaskForm):
   email = StringField(
      '邮箱',
      validators=[
         DataRequired(message='请输入邮箱'),
         Length(min=5,max=45,message='长度在5-45个字符之间')
      ]
   )
   username = StringField(
      '用户名',
      validators=[
         DataRequired(message='请输入用户名'),
         Length(min=2,max=25,message='长度在2-20个字符之间')
      ]
   )
   password = PasswordField(
      '密码',
      validators=[
         DataRequired(message='密码不能为空'),
         Length(min=6,max=20,message='长度在6-20个字符之间')
      ]
   )
   confirm = PasswordField(
      '确认密码',
      validators=[
         DataRequired(message='密码不能为空'),
         equal_to('password',message='两次输入不一致')
      ]
   )

# 文章
class ArticleForm(FlaskForm):
   title = StringField(
      '标题',
      validators=[
         DataRequired(message='请输入标题'),
         Length(min=1,max=20,message='长度为1-20个字符之间')
      ]
   )
   body = TextAreaField(
      '内容',
      validators=[
         DataRequired(message='不少于5个字符'),
         Length(min=5)
      ]
   )
   
