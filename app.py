from flask import Flask, render_template as rt, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Member.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

db = SQLAlchemy(app)
comment = "ようこそ"
joins = True
k = 0
line_member = None
group_num = 0
jmembers = []
s_jmembers = []
change = []
count_m = 1
ca = 0
exchange = []
xxx = 0
ol_info = [0,0]
l_jmembers = []
g_jmembers = []

class Post(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable = True)
    line = db.Column(db.String(50),nullable = False)
    read = db.Column(db.String(30),nullable= True )
    grade = db.Column(db.Integer,nullable= False)
    sex   = db.Column(db.String(1),nullable = False)
    belong = db.Column(db.Integer, nullable=False)
class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer,primary_key=True)
    people = db.Column(db.String(1000),nullable = False)
    when = db.Column(db.Integer, nullable = False)


@app.route('/', methods=['GET','POST'])
def index():
    global exchange, line_member
    exchange = []
    if request.method == 'GET':
        members1 = Post.query.filter(Post.grade==1).order_by(Post.read.asc()).all()
        c1 = len(members1)
        members2 = Post.query.filter(Post.grade==2).order_by(Post.read.asc()).all()
        c2 = len(members2)
        members3 = Post.query.filter(Post.grade==3).order_by(Post.read.asc()).all()
        c3 = len(members3)
        members4 = Post.query.filter(Post.grade==4).order_by(Post.read.asc()).all()
        c4 = len(members4)

        return rt('index.html', members1=members1,members2=members2,members3=members3,members4=members4,greeding=comment,c1=c1,c2=c2,c3=c3,c4=c4,line_member=line_member)
    else:
        members1 = Post.query.filter(Post.grade==1).order_by(Post.read.asc()).all()
        c1 = len(members1)
        members2 = Post.query.filter(Post.grade==2).order_by(Post.read.asc()).all()
        c2 = len(members2)
        members3 = Post.query.filter(Post.grade==3).order_by(Post.read.asc()).all()
        c3 = len(members3)
        members4 = Post.query.filter(Post.grade==4).order_by(Post.read.asc()).all()
        c4 = len(members4)

        return rt('index.html', members1=members1,members2=members2,members3=members3,members4=members4,greeding=comment,c1=c1,c2=c2,c3=c3,c4=c4,line_member=line_member)


@app.route('/search', methods=['POST','GET'])
def search():
    global line_member
    name = request.form.get('line_name')
    if name != "":
        line_member = Post.query.filter(Post.line.like( "%%%s%%" %   name ))
    else:
        line_member = None
    return redirect('/')


@app.route('/create',methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return rt('create.html')
    else:
        name = request.form.get('name')
        read = request.form.get('read')
        line = request.form.get('line')
        grade = request.form.get('grade')
        sex = request.form.get('sex')
        belong = 0


        new_member = Post(name=name,line = line ,read=read, grade=grade, sex=sex ,belong = belong)

        db.session.add(new_member)
        db.session.commit()
        return redirect('/create')
        
@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'GET':
        members1 = Post.query.filter(Post.grade==1).order_by(Post.read.asc()).all()
        members2 = Post.query.filter(Post.grade==2).order_by(Post.read.asc()).all()
        members3 = Post.query.filter(Post.grade==3).order_by(Post.read.asc()).all()
        members4 = Post.query.filter(Post.grade==4).order_by(Post.read.asc()).all()
        c1 = len(members1)
        c2 = len(members2)
        c3 = len(members3)
        c4 = len(members4)
        return rt('admin.html', members1=members1,members2=members2,members3=members3,members4=members4,greeding=comment,c1=c1,c2=c2,c3=c3,c4=c4)
    else:
        return redirect('/admin')

@app.route('/judge',methods=['GET','POST'])
def judge():
    if request.method == 'POST':
        passwrd = request.form.get('password')
        members1 = Post.query.filter(Post.grade==1).order_by(Post.read.asc()).all()
        c1 = len(members1)
        members2 = Post.query.filter(Post.grade==2).order_by(Post.read.asc()).all()
        c2 = len(members2)
        members3 = Post.query.filter(Post.grade==3).order_by(Post.read.asc()).all()
        c3 = len(members3)
        members4 = Post.query.filter(Post.grade==4).order_by(Post.read.asc()).all()
        c4 = len(members4)
        if passwrd == "aaa":
            comment ="ようこそ"
            return rt('admin.html', members1=members1,members2=members2,members3=members3,members4=members4,greeding=comment,c1=c1,c2=c2,c3=c3,c4=c4)
        else:
            comment="お前ほんまに管理者なん? "
            return rt('index.html',members1=members1,members2=members2,members3=members3,members4=members4,greeding=comment,c1=c1,c2=c2,c3=c3,c4=c4)
    else:
        members = Post.query.all()
        return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    member = Post.query.get(id)
    db.session.delete(member)
    db.session.commit()

    return redirect('/admin')

@app.route('/join',methods=['GET','POST'])
def join():
    global line_member
    line_member = None
    members = Post.query.all()
    if request.method == 'GET':
        return redirect('/')
    
    else:
        joinings_s = request.form.getlist('joining')
        joinings = list(map(int,joinings_s))

        for member in members:
            if (member.id in joinings) == False:
                member.belong = 0
                db.session.commit()
            else:
                member.belong = 1 
                db.session.commit()

    return redirect('/')

@app.route('/reset', methods = ["POST"])
def reset():
    members = Post.query.all()
    for member in members:
        member.belong = 0
        db.session.commit()

    return redirect('/')
        

@app.route('/joiner',methods=['GET'])
def joiner():
    if request.method == 'GET':
        members1 = Post.query.filter(Post.grade==1,Post.belong==1).order_by(Post.read.asc()).all()
        c1 = len(members1)
        members2 = Post.query.filter(Post.grade==2,Post.belong==1).order_by(Post.read.asc()).all()
        c2 = len(members2)
        members3 = Post.query.filter(Post.grade==3,Post.belong==1).order_by(Post.read.asc()).all()
        c3 = len(members3)
        members4 = Post.query.filter(Post.grade==4,Post.belong==1).order_by(Post.read.asc()).all()
        c4 = len(members4)
        members = Post.query.filter(Post.belong == 1).all()
        ca = len(members)

        return rt('joiner.html', members1=members1,members2=members2,members3=members3,members4=members4,greeding=comment,c1=c1,c2=c2,c3=c3,c4=c4,ca=ca,k=k)

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    member = Post.query.get(id)
    if request.method == 'GET':
        return rt('update.html', member=member)
    else:
        member.name = request.form.get('name')
        member.line = request.form.get('line')
        member.read = request.form.get('read')
        member.grade = request.form.get('grade')
        member.sex   = request.form.get('sex')
        db.session.commit()

        return redirect('/admin')

@app.route('/grouping', methods=['POST','GET'])
def grouping():
    global jmembers,group_num,ca,count_m,exchange,s_jmembers,l_jmembers,g_jmembers
    if request.method == 'POST':
        jmembers = []
        s_jmembers = []
        l_jmembers = []
        g_jmembers = []

        join_freshers = Post.query.filter(Post.belong == 1, Post.grade == 1)        #1年生のデータ
        join_second = Post.query.filter(Post.belong == 1, Post.grade == 2)          #2年生のデータ
        join_third= Post.query.filter(Post.belong == 1, Post.grade == 3)            #3年生のデータ
        join_fourth = Post.query.filter(Post.belong ==1, Post.grade == 4)           #4年生のデータ
        freshers = []                                                               #新入生
        s_freshers = []
        l_freshers = []
        g_freshers = []
        second = []                                                              
        s_second = []
        l_second = []
        g_second = []
        senior = []                                                   
        s_senior = []
        l_senior = []
        g_senior = []

        for member in join_freshers:                                            #学年ごとのlistに名前、性別を追加     
            freshers.append(member.name)
            s_freshers.append(member.sex)
            l_freshers.append(member.line)
            g_freshers.append(member.grade)
        for member in join_second:
            second.append(member.name)
            s_second.append(member.sex)
            l_second.append(member.line)
            g_second.append(member.grade)
        for member in join_third:
            senior.append(member.name)
            s_senior.append(member.sex)
            l_senior.append(member.line)
            g_senior.append(member.grade)
        for member in join_fourth:
            senior.append(member.name)      
            s_senior.append(member.sex)
            l_senior.append(member.line)
            g_senior.append(member.grade)

        count_m = int(request.form.get('group_num'))                                #グループの人数
        ca = Post.query.filter(Post.belong == 1).count()                            #参加人数
        group_num = ca // count_m  
                                             


        g =0

        for i in range(group_num):
            name = "group"+str(i)
            globals()[name] = []
            s_name = 'sex'+str(i)
            globals()[s_name] = []
            l_name = 'line'+str(i)
            globals()[l_name] = []
            g_name = 'grade'+str(i)
            globals()[g_name] = []


        def setlist(x):                                                         #list発見関数
            name = "group" + str(x)
            return globals()[name]
        def sexlist(x):
            name = "sex"+str(x)
            return globals()[name]
        def setline(x):
            name = "line"+str(x)
            return globals()[name]
        def setgrade(x):
            name = 'grade'+str(x)
            return globals()[name]
        
        def resetter(x):                                                        #追加するlist番号の指定
            if x + 1 == group_num:
                return 0
            else:
                return x + 1
                        

        r_freshers = randmaking(len(freshers))
        r_second = randmaking(len(second))
        r_senior = randmaking(len(senior))


        for num in r_senior:                                                    #グループメンバーを二次元配列に組み込む
            setlist(g).append(senior[num])
            sexlist(g).append(s_senior[num])
            setline(g).append(l_senior[num])
            setgrade(g).append(g_senior[num])
            g = resetter(g)
        for num in r_second:
            setlist(g).append(second[num])
            sexlist(g).append(s_second[num])
            setline(g).append(l_second[num])
            setgrade(g).append(g_second[num])
            g = resetter(g)
        for num in r_freshers:
            setlist(g).append(freshers[num])
            sexlist(g).append(s_freshers[num])
            setline(g).append(l_freshers[num])
            setgrade(g).append(g_freshers[num])
            g = resetter(g)


        for i in range(group_num):                                              #それぞれのグループのリストをmembersという一つのグループにぶち込む
            name = "group"+str(i)
            s_name = 'sex'+str(i)
            l_name = 'line'+str(i)
            g_name = 'grade'+str(i)
            jmembers.append(globals()[name])
            s_jmembers.append(globals()[s_name])
            l_jmembers.append(globals()[l_name])
            g_jmembers.append(globals()[g_name])

        
        exchange = np.zeros((len(jmembers),len(jmembers[0])))

        return rt('grouped_members.html',exchange = exchange,l_jmembers=l_jmembers,s_jmembers=s_jmembers, group_num = group_num, jmembers = jmembers,ca = ca,g_jmembers=g_jmembers,count_m=count_m)
    
    else:

        return rt('grouped_members.html',exchange = exchange,l_jmembers=l_jmembers , group_num = group_num, s_jmembers=s_jmembers ,jmembers = jmembers,ca = ca,count_m=count_m,g_jmembers=g_jmembers)


@app.route('/replace', methods=['POST','GET'])
def replace():
    global position,jmembers,exchange,ol_info,xxx,s_jmembers,l_jmembers,g_jmembers
    if xxx == 0:
        xxx+=1
        name = request.form.get('place')
        r=0
        l=0
        for x in range(len(jmembers)):
            if name in jmembers[x]:
                l = x
                r = jmembers[x].index(name)
        ol_info = [l,r]
        exchange[l][r] = 1
        return redirect('/grouping') 
    else:
        xxx = 0
        name = request.form.get('place')
        r=0
        l=0

        for x in range(len(jmembers)):
            if name in jmembers[x]:
                l = x
                r = jmembers[x].index(name)

        old_l = ol_info[0]
        old_r = ol_info[1]
        old_line = l_jmembers[old_l][old_r]
        old_name = jmembers[old_l][old_r]
        old_sex = s_jmembers[old_l][old_r]
        old_grade = g_jmembers[old_l][old_r]
        new_name = jmembers[l][r]
        new_sex = s_jmembers[l][r]
        new_line = l_jmembers[l][r]
        new_grade = g_jmembers[l][r]
        jmembers[l][r] = old_name
        jmembers[old_l][old_r] = new_name
        s_jmembers[l][r] = old_sex
        s_jmembers[old_l][old_r] = new_sex
        l_jmembers[l][r] = old_line
        l_jmembers[old_l][old_r] = new_line
        g_jmembers[l][r] = old_grade
        g_jmembers[old_l][old_r] = new_grade
        exchange[old_l][old_r] = 0

        return redirect('/grouping')
    

@app.route('/lastjudge', methods=['GET','POST'])
def lastjudge():
    global l_jmembers,group_num ,ca,count_m
    if request.form.get('way') == "確定する":
        w = 0
        count = len(l_jmembers)
        histories = History.query.all()
        if len(histories) != 0:
            for history in histories:
                if w < history.when:
                    w = history.when + 1
            
        for i in range(count):
            people = ""
            for member in l_jmembers[i]:
                people += member + ","
            new_his = History(people = people, when = w)
            db.session.add(new_his)
            db.session.commit()


        for history in histories:
            print(history.people)

        return redirect('/')
    else:
        return redirect('/grouping')



@app.route('/complete',methods=['GET','POST'])
def complete():
    global l_jmembers,group_num ,ca,count_m 
    return rt('complete.html',l_jmembers=l_jmembers, group_num = group_num,ca = ca,count_m=count_m)


@app.route('/seehis',methods=["GET"])
def seehis():
    histories = History.query.all()
    num = len(histories)
    his = []
    for history in histories:
        peo = history.people
        mem = peo.split(',')
        his.append(mem)

    return rt('seehis.html',his = his, num=num)

@app.route('/forget',methods=["GET","POST"])
def forget():
    db.session.query(History).delete()
    db.session.commit()

    return redirect('/')


def randmaking(x):
    ns =[]
    while len(ns) < x:
        n = random.randint(0,x-1)
        if not n in ns:
            ns.append(n)
    return ns



if __name__ == "__main__":
    app.run()





        