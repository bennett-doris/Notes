# import  pymysql
#
# #  连接数据库
# db = pymysql.Connect('localhost','root','123456','Notes')
# # 创建游标对象
# cursorr = db.cursor()
# # 编写SQL语句
# SQL = ''
# # 执行sql语句
# res = cursorr.execute(sql)
# # 提交
# db.commit()
# # 关闭游标对象
# cursorr.close()
# # 关闭数据库对象
# db.close()

from . import *
from datetime import datetime


class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

class Artciles(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    author = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow())


db.drop_all()
db.create_all()