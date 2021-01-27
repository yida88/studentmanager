import pymysql
from django.shortcuts import render,redirect,HttpResponse
from utils import sqlheper
import json
def classes(request):
    conn = pymysql.connect(host='127.0.0.1', user ='root', password ='080851', database ='Studentdb', charset ='utf8')
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list=cursor.fetchall()
    print(class_list)
    cursor.close()
    conn.close()
    return render(request,'classes.html',{'class_list':class_list})
def add_class(request):
    if request.method=="GET":
        return render(request ,'add_class.html')
    else:
        v=request.POST.get("title")
        if len(v)>0:

            conn = pymysql.connect(host='127.0.0.1', user='root', password='080851', database='Studentdb', charset='utf8')
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            print(cursor)
            cursor.execute("insert into class(title) values(%s)",[v,])
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/classes')
        else:
            return render(request,'add_class.html',{"msg":'班级名称不能为空'})
def del_class(request):
    nid=request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', user='root', password='080851', database='Studentdb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print(cursor)
    cursor.execute("delete from class where id=%s", [nid, ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes')
def edit_class(request):
    if request.method=="GET":
        nid=request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', user='root', password='080851', database='Studentdb', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class where id=%s",[nid,])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request, 'edit_class.html', {'result': result})

    else:
        title=request.POST.get("title")
        nid=request.GET.get('nid')

        conn = pymysql.connect(host='127.0.0.1', user='root', password='080851', database='Studentdb', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        print(cursor)
        cursor.execute("update class set title=%s where id=%s",[title,nid])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes')
def students(request):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='080851', database='Studentdb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select student.id,student.name,class.title,student.class_id from student LEFT JOIN class ON class.id=student.class_id")
    students_list = cursor.fetchall()
    cursor.close()
    conn.close()
    class_list=sqlheper.get_list("select id,title from class",[])
    print(class_list)
    return render(request, 'students.html', {'students_list':students_list,'class_list':class_list})
def add_student(request):
    if request.method == "GET":
        conn = pymysql.connect(host='127.0.0.1', user='root', password='080851', database='Studentdb', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class")
        class_list = cursor.fetchall()
        print(class_list)
        cursor.close()
        conn.close()
        return render(request, 'add_student.html',{'class_list':class_list})
    else:
        name = request.POST.get("name")
        class_id=request.POST.get('class_id')

        conn = pymysql.connect(host='127.0.0.1', user='root', password='080851', database='Studentdb', charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        print(cursor)
        cursor.execute("insert into student (name,class_id) values(%s,%s)", [name,class_id])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/students')
def del_student(request):
    nid=request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', user='root', password='080851', database='Studentdb', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    print(cursor)
    cursor.execute("delete from student where id=%s", [nid, ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/students')
def edit_student(request):
    from utils import sqlheper
    if request.method=="GET":
        nid=request.GET.get('nid')
        class_list=sqlheper.get_list("select id,title from class",[])
        student_list=sqlheper.get_one("select id,name,class_id from student where id=%s",[nid,])
        return render(request, 'edit_student.html', {'class_list': class_list,'student_list':student_list})
    else:
        name=request.POST.get("name")
        nid=request.GET.get('nid')
        cid=request.POST.get('class_id')

        sqlheper.modify("update student set name=%s,class_id=%s where id=%s",[name,cid,nid])
        return redirect('/students')
def teachers(request):
    teacher_list=sqlheper.get_list("""SELECT teacher.id as tid, teacher.name, class.title from teacher LEFT JOIN teacher2class ON teacher.id=teacher2class.teacher_id
LEFT JOIN class ON class.id=teacher2class.class_id""",[])
    print(teacher_list)
    result={}
    for row in teacher_list:
        tid=row['tid']
        if tid in result:
            result[tid]['titles'].append(row['title'])
        else:
            result[tid]={'tid':row['tid'],'name':row['name'],'titles':[row['title']]}
    print(result)
    class_list = sqlheper.get_list("select id,title from class", [])
    # for row in result.values():
    #     row['titles']=','.join(row['titles'])
    return render(request,'teachers.html',{'teachers_list':result.values(),'class_list':class_list})
def modal_add_class(request):
    from utils import sqlheper
    title = request.POST.get("title")
    print(title)
    if len(title)>0:

        sqlheper.modify("insert into class(title) values(%s)", [title, ])
        return HttpResponse('ok')
    else:
        return HttpResponse('班级名称不能为空')
def modal_del_class(request):
    from utils import sqlheper
    nid = request.POST.get("nid")
    print(nid)
    if len(nid)>0:

        sqlheper.modify("delete from class where id=%s", [nid, ])
        return HttpResponse('ok')
    else:
        return HttpResponse('班级名称不能为空')
def modal_edit_class(request):
    from utils import sqlheper
    title = request.POST.get("title")
    nid = request.POST.get("nid")
    print(nid)
    print(title)
    if len(title) > 0:
        sqlheper.modify("update class set title=%s where id=%s", [title,nid])
        return HttpResponse('ok')
    else:
        return HttpResponse('班级名称不能为空')
def modal_add_student(request):
    ret={"statues":True,'message':None}
    try:

        name=request.POST.get('name')
        classid=request.POST.get('class_id')
        print(name,classid)
        if len(name)>0:


            sqlheper.modify("insert into student(name,class_id) value(%s,%s)",[name,classid])
        else:
            ret['statues'] = False
            ret['message'] = "姓名不能为空"
    except Exception as e:
        ret['statues']=False
        ret['message']=str(e)
    return HttpResponse(json.dumps(ret))
def modal_del_student(request):
    ret={'status':True,'message':None}
    try:
        student_id=request.POST.get('student_id')
        sqlheper.modify("delete from student where id=%s",[student_id,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))
def modal_edit_student(request):
    ret={'status':True,'message':None}
    try:
        student_id=request.POST.get('student_id')
        student_name=request.POST.get('student_name')
        class_id=request.POST.get('class_id')
        if len(student_name)>0:
            sqlheper.modify("update student set name=%s,class_id=%s where id=%s",[student_name,class_id,student_id])
        else:
            ret['status'] = False
            ret['message'] ="学生姓名不能为空"
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))
def modal_add_teacher(request):
    ret={'status':True,'message':None}
    try:
        name=request.POST.get('teacher_name')
        class_id=request.POST.get('class_id')
        cid=class_id.split(',')
        print(cid)
        print(class_id)
        if len(name)>0:
            sqlheper.modify("insert into teacher(name) value(%s)",[name,])
            teacher_id=sqlheper.get_one("select id from teacher where name=%s",[name],)
            tid=teacher_id['id']
            print(teacher_id['id'])
            for i in cid:
                sqlheper.modify("insert into teacher2class(teacher_id,class_id) value(%s,%s)",[tid,i])
        else:
            ret['status'] = False
            ret['message'] = "老师姓名不能为空"
    except Exception as e:
        ret['status']=False
        ret['message']=str(e)
    return HttpResponse(json.dumps(ret))
def login(request):
    return render(request,'login.html')
def welcome(request):
    return  render(request,'welcome.html')






