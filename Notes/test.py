import  pymysql
#
# #  连接数据库
db = pymysql.Connect(host='192.168.1.116',port=8306,user = 'root',password = '123456',database = 'Notes')
# # 创建游标对象
cursorr = db.cursor()
# # 编写SQL语句
SQL = 'create table t2 (id int)'
# # 执行sql语句
res = cursorr.execute(SQL)
# # 提交
db.commit()
# # 关闭游标对象
cursorr.close()
# # 关闭数据库对象
db.close()