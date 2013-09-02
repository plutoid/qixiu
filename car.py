#!/usr/bin/python
#coding:utf8
# 显示表格
#coding:utf8
# 提示信息中文话
# 车牌输入唯一提示 z/
# 判断逻辑 z/
# 时间 月日选择 用下拉框
# 车牌不能修改 注意输入字母为大写,转换为大写
# update: 2012年04月 2日 21:28:29

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import flask
import time

DATABASE = 'car.db'
#DEBUG = True
SECRET_KEY = 'development key'
USERNAME = ''
PASSWORD = ''

app = Flask(__name__)
# 添加所有的大写变量
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    nowmonth = str(time.strftime("%m",time.localtime())+'%')
    if 'logged_in' in session:
        cur = g.db.execute("select carid,owner,corp, tel,fst,snd,thd,year,insurance, remarks from car where fst like  ?  or snd like ? or thd like ? or year like ? or insurance like ? order by id desc",[nowmonth,nowmonth, nowmonth, nowmonth, nowmonth  ])
        entries = [dict(carid=row[0], owner=row[1], corp=row[2], tel=row[3], fst=row[4],snd=row[5],thd=row[6],year=row[7], insurance=row[8],remarks=row[9] ) for row in cur.fetchall()]
        return render_template('index.html', entries=entries)
    return redirect(url_for('login'))

@app.route('/about')
def about():
    error = None
    return render_template('about.html', error=error)

def mon_chk(monstr):
    cur = g.db.execute("select carid,owner,corp, tel,fst,snd,thd,year,insurance, remarks from car where fst not like  ?  and   (year like ? or insurance like ? ) order by id desc",[monstr,monstr,monstr,monstr,monstr])
    mon_chk = [dict(carid=row[0], owner=row[1], corp=row[2], tel=row[3], fst=row[4],snd=row[5],thd=row[6],year=row[7], insurance=row[8],remarks=row[9] ) for row in cur.fetchall()]
    return mon_chk
    

@app.route('/all')
def all():
    nowmonth = str(time.strftime("%m",time.localtime())+'%')
    if 'logged_in' in session:
        all =[[],[],[],[],[],[],[],[],[],[],[],[]] 

        moninx = 0
        m1 = ['01%','02%','03%','04%']
        for month in m1:
            cur = g.db.execute("select carid,owner,corp, tel,fst,snd,thd,year,insurance, remarks from car where fst like  ?   or year like ? or insurance like ? order by id desc",[month,month,month])
            result = [dict(carid=row[0], owner=row[1], corp=row[2], tel=row[3], fst=row[4],snd=row[5],thd=row[6],year=row[7], insurance=row[8],remarks=row[9] ) for row in cur.fetchall()]
            all[moninx] = result
            moninx = moninx+1

        m1 = ['05%','06%','07%','08%']
        for month in m1:
            cur = g.db.execute("select carid,owner,corp, tel,fst,snd,thd,year,insurance, remarks from car where snd like  ?   or year like ? or insurance like ? order by id desc",[month,month,month])
            result = [dict(carid=row[0], owner=row[1], corp=row[2], tel=row[3], fst=row[4],snd=row[5],thd=row[6],year=row[7], insurance=row[8],remarks=row[9] ) for row in cur.fetchall()]
            all[moninx] = result
            moninx = moninx+1

        m1 = ['09%','10%','11%','12%']
        for month in m1:
            cur = g.db.execute("select carid,owner,corp, tel,fst,snd,thd,year,insurance, remarks from car where thd like  ?   or year like ? or insurance like ? order by id desc",[month,month,month])
            result = [dict(carid=row[0], owner=row[1], corp=row[2], tel=row[3], fst=row[4],snd=row[5],thd=row[6],year=row[7], insurance=row[8],remarks=row[9] ) for row in cur.fetchall()]
            all[moninx] = result
            moninx = moninx+1

        return render_template('all.html', entries= all )
    return redirect(url_for('login'))

@app.route('/modify')
def modify():
    if 'logged_in' in session:
        cur = g.db.execute("select carid,owner,corp,tel,fst,snd,thd,year,insurance, remarks from car order by fst ")
        entries = [dict(carid=row[0], owner=row[1], corp=row[2], tel=row[3], fst=row[4],snd=row[5],thd=row[6],year=row[7], insurance=row[8],remarks=row[9] ) for row in cur.fetchall()]
        return render_template('all.html', entries= all )
    return redirect(url_for('login'))

@app.route('/modify')
def modify():
    if 'logged_in' in session:
        cur = g.db.execute("select carid,owner,corp,tel,fst,snd,thd,year,insurance, remarks from car order by fst ")
        entries = [dict(carid=row[0], owner=row[1], corp=row[2], tel=row[3], fst=row[4],snd=row[5],thd=row[6],year=row[7], insurance=row[8],remarks=row[9] ) for row in cur.fetchall()]
        return render_template('modify.html', entries=entries)
    return redirect(url_for('login'))

@app.route('/update')
def update():
    cur = g.db.execute("select carid,owner,corp, tel,fst,snd,thd,year,insurance, remarks from car where carid=? ",[request.args['carid']])
    entries = [dict(carid=row[0], owner=row[1], corp=row[2], tel=row[3], fst=row[4],snd=row[5],thd=row[6],year=row[7], insurance=row[8],remarks=row[9] ) for row in cur.fetchall()]
    return render_template('update.html', entries=entries)

@app.route('/del')
def delete():
    if 'logged_in' in session:
        cur = g.db.execute("delete from car where carid =? ",[request.args['carid']] )
        g.db.commit()
        flash('Deleted')
        return redirect(url_for('modify'))
    return redirect(url_for('index'))

def carids():
    cur = g.db.execute("select carid from car")
    return [dict(carid=row[0]) for row in cur.fetchall()]

@app.route('/add', methods=['POST'])
def add_entry():
    exist = True
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    for ci in carids():
        if request.form['carid'] == ci['carid']:
            flash('chepai yijing cunzai!!!')
            exist = False
        elif request.form['carid'] == '':
            return redirect(url_for('index'))
            exist = False
    if exist :
        g.db.execute('insert into car (carid, owner, corp, tel, fst, snd,thd,year,insurance,remarks) values (?, ?, ?, ?,?, ?, ?, ?, ?, ? )', [request.form['carid'], request.form['owner'], request.form['corp'], request.form['tel'], request.form['fst'], request.form['snd'], request.form['thd'], request.form['year'], request.form['insurance'],  request.form['remarks']])
        g.db.commit()
        flash(' New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/set_update', methods=['POST'])
def set_update():
    exist = True
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    for ci in carids():
        if request.form['carid'] == '':
            return redirect(url_for('index'))
            exist = False
    if exist :
        g.db.execute('update  car set carid = ?,  owner =? ,  corp =? ,   tel =? ,  \
                                      fst =? , snd =? ,  thd =? ,  year =? ,  \
                                      insurance =? , remarks =?  where carid= ?',  \
                                     [request.form['carid'],  request.form['owner'],  \
                                      request.form['corp'],  request.form['tel'],   \
                                      request.form['fst'],   request.form['snd'],   \
                                      request.form['thd'],  request.form['year'], \
                                      request.form['insurance'],request.form['remarks'],\
                                      request.form['carid']])
        g.db.commit()
        flash('Entry updated successfully!')
    return redirect(url_for('modify'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #print request.form['username'], request.form['password'] 
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    #app.debug = False
    #app.run(host='0.0.0.0')
    app.run(debug=True)

