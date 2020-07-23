import json
from functools import wraps

from . import *
from flask import render_template, request, flash, redirect, url_for, make_response, session,escape
from .forms import RegisterForm,ArticleForm
from passlib.hash import sha256_crypt
from .models import Users,Artciles

@app.route('/register',methods=['GET','POST'])
def  register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # 接收表单数据
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # 存入数据库
        user = Users()
        user.email =email
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()
        flash('您已注册成功，请登录','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    # 查看是否已经登录，若已登录，直接跳转
    if 'login_in' in request.cookies:
        return redirect(url_for('dashboard'))
    else:
        if 'login_in' in session:
            session['login_in'] = True
            session['username'] = request.cookies.get('username')
            return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # 获取表单数据
        username = request.form['username']
        password_candicate = request.form['password']
        res = Users.query.filter_by(username=username).first()
        if res:
            password = res.password
            if sha256_crypt.verify(password_candicate,password):
                # 调用verify方法验证如果为真，验证通过
                # 写入cookie
                response = make_response(
                    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
                    "<title>Redirecting...</title>\n"
                    "<h1>Redirecting...</h1>\n"
                    "<p>You should be redirected automatically to target URL: "
                    '<a href="%s">%s</a>.  If not click the link.'
                    % (escape(url_for('dashboard')),
                       escape(url_for('dashboard'))), 302)
                response.set_cookie('login_in','True',max_age=60*60*24*38)
                response.set_cookie('username',username,max_age=60*60*24*38)
                # 存入session
                session['login_in'] = True
                session['username']=username
                response.location = escape(url_for('dashboard'))
                return response
            else:
                error = '用户名和密码不匹配'
                return render_template('login.html',error=error)
        else:
            error = '用户名不存在'
            return render_template('login.html',error=error)
    return render_template('login.html')

def is_login_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'login_in' in session:
            return f(*args,**kwargs)
        else:
            flash('无权访问，请先登录','danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_login_in
def logout():
    if 'login_in' in request.cookies:
        response = make_response(
            '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
            "<title>Redirecting...</title>\n"
            "<h1>Redirecting...</h1>\n"
            "<p>You should be redirected automatically to target URL: "
            '<a href="%s">%s</a>.  If not click the link.'
            % (escape(url_for('index')),
               escape(url_for('index'))), 302)
        response.delete_cookie('login_in')
        response.location = escape(url_for('index'))
        return response
    else:
        session.clear()
        flash('您已成功退出', 'success')
        return redirect(url_for('index'))


@app.route('/dashboard')
@is_login_in
def dashboard():
    notes = Artciles.query.order_by(Artciles.timestamp.desc()).all()
    if notes:
        return render_template('dashboard.html',notes=notes)
    else:
        msg = '暂无笔记信息'
        return render_template('dashboard.html',msg=msg)

@app.route('/artcile/<string:id>')
@is_login_in
def artcile(id):
    note = Artciles.query.get(id)
    return render_template('article.html',note=note)

@app.route('/add_article',methods=['GET','POST'])
@is_login_in
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        note = Artciles()
        note.title = form.title.data
        note.author = session['username']
        note.body = form.body.data
        db.session.add(note)
        db.session.commit()
        flash('提交成功','success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form=form)  # 渲染模板

@app.route('/delete_article/<int:id>',methods=['POST'])
@is_login_in
def delete_article(id):
    note = Artciles.query.filter_by(id=id).first()
    print(note.body)
    db.session.delete(note)
    db.session.commit()
    flash('删除成功','success')
    return redirect(url_for('dashboard'))

@app.route('/edit_article/<int:id>',methods=['GET','POST'])
@is_login_in
def edit_article(id):
    note = Artciles.query.filter_by(id=id).first()
    if not note:
        flash('ID错误','danger')
        return redirect(url_for('dashboard'))
    form = ArticleForm(request.form)
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        db.session.add(note)
        db.session.commit()
        flash('更改成功','success')
        return redirect(url_for('dashboard'))
    form.title.data = note.title
    form.body.data = note.body
    return render_template('edit_article.html',form=form)

@app.route('/')
def index():
    return render_template('home.html')



# 如果表单提交且字段验证通过,查询数据库是否存在相同数据
# 如果存在，返回错误提示，如果不存在，则存入数据库
@app.route('/check_info')
def check_info(data):
    # 接收数据
    email = data
    if Users.object.filter(email=email):
        dic = {
            'status':0,
            'msg':'邮箱已被注册'
        }
    else:
        dic = {
            'status': 1,
            'msg': '邮箱可以使用'
        }
    return json.dumps(dic)

@app.route('/checkLogged')
def checkLogged():
    if 'login_in' in session:
        dic = {
            'loginStatus':1,
        }
    else:
        dic = {
            'loginStatus':0,
        }
    print(dic['loginStatus'])
    return json.dumps(dic)


if __name__ == '__main__':
    app.run(debug=True)
