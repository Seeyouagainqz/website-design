import pymysql
from flask import Flask,request,jsonify
from flask_cors import CORS

#数据库的连接
                    #数据库的地址，可以是localhost:8,数据库的用户名,密码,数据库的名字，
db = pymysql.connect(host="127.0.0.1", user="root", password="1938lkw7352@", database="company")
cursor = db.cursor()

 #后端服务器启动
app = Flask( __name__ )
CORS(app,resources=r'/*')

#后端代码核心部分          /url  后端接口的路径

#登陆时验证          1 可行    员工
@app.route('/login/login1', methods=['POST'])
def login_login1():
    if request.method == "POST":
        username = request.form.get("username") 
        password = request.form.get("password")
        cursor.execute("select id,username,role,ctime from login where username=\""
                       +str(username)+"\" and password=\""+str(password)+"\" ")
        data = cursor.fetchone()
        if(data!=None):
            print("result:",data)
            jsondata = {"id":str(data[0]),"username":str(data[1]),
                        "role":str(data[2]),"ctime":str(data[3])}
            return jsonify(jsondata)
        else:
            print("result: NULL") 
            jsondata = {}
            return jsonify(jsondata)

#登陆时验证    用户        2
@app.route('/login/login2', methods=['POST'])
def login_login2():
    if request.method == "POST":
        username = request.form.get("username") 
        password = request.form.get("password")
        cursor.execute("select id,username,role,ctime from login where username=\""
                       +str(username)+"\" and password=\""+str(password)+"\" and role=0")
        data = cursor.fetchone()
        if(data!=None):
            print("result:",data)
            jsondata = {"id":str(data[0]),"username":str(data[1]),
                        "role":str(data[2]),"ctime":str(data[3])}
            return jsonify(jsondata)
        else:
            print("result: NULL")
            jsondata = {}
            return jsonify(jsondata)
        

#更新员+  用户密码         3 可行
@app.route('/login/updatepassword',methods=['POST'])
def update_login():
    if request.method == "POST":    #这里的username  要与前端保持一致     username=\""+str(username)+"\"
        id = request.form.get("id")
        username = request.form.get("username")
        password = request.form.get("password")
        try:
            cursor.execute("UPDATE `login` SET password=\""+str(password)+"\" WHERE id="+str(id)+"")
            db.commit()     
            print("update a new user successfully")
            return "1"
        except Exception as e:
            print("update a new user falied:",e)
            db.rollback()
            return "-1"

#用户信息在显示屏上展示       4 可行
@app.route('/login/list', methods=['POST'])
def login_list():
    if request.method == "POST":
        cursor.execute("select id,username,role,ctime from login")
        data = cursor.fetchall()
        temp={}
        result=[]
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["role"]=i[2]
                temp["ctime"]=i[3]
                result.append(temp.copy()) #特别注意要用copy，否则只是内存的引用
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result: NULL")
            return jsonify([])


#更改用户角色        10  可行
@app.route('/login/update_role', methods=['POST'])
def login_update_role():
    if request.method == "POST":
        id = request.form.get("id")
        role = request.form.get("role")
        try:
            cursor.execute("update login set role=\""+str(role)
                            +"\" where id="+str(id))
            db.commit()
            print("update role successfully!")
            return "1"
        except Exception as e:
            print("update role failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

        
#显示用户全部信息                5   可行
@app.route('/用户表/userall',methods=['POST'])
def select_user():
    if request.method == "POST":       #这里的username  要与前端保持一致
        cursor.execute("SELECT login.id,username,uname,idcard,ucall,remark,mremark,login.ctime FROM login JOIN `用户表` on login.id=`用户表`.id")
        data = cursor.fetchall();
        temp = {}
        result = []
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["uname"]=i[2]
                temp["idcard"]=i[3]
                temp["ucall"]=i[4]
                temp["remark"]=i[5]
                temp["mremark"]=i[6]
                temp["ctime"]=i[7]
                result.append(temp.copy())
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result:NULL")
            return jsonify([])



#更新用户信息  姓名          6 可行
@app.route('/用户表/updateuname', methods=['POST'])
def login_update_uname():
    if request.method == "POST":
        id = request.form.get("id")
        uname = request.form.get("uname")
        try:
            cursor.execute("update `用户表` set uname=\""+str(uname)+"\" where id="+str(id))
            db.commit()
            print("update role successfully!")
            return "1"
        except Exception as e:
            print("update role failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

#更新用户  身份证号     7     可行
@app.route('/用户表/updateidcard', methods=['POST'])
def login_update_idcard():
    if request.method == "POST":
        id = request.form.get("id")
        idcard = request.form.get("idcard")
        try:
            cursor.execute("update `用户表` set idcard="+str(idcard)+" where id="+str(id))
            db.commit()
            print("update role successfully!")
            return "1"
        except Exception as e:
            print("update role failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

#更新用户    电话        8       可行
@app.route('/用户表/updateucall', methods=['POST'])
def login_update_ucall():
    if request.method == "POST":
        id = request.form.get("id")
        ucall = request.form.get("ucall")
        try:
            cursor.execute("update `用户表` set ucall="+str(ucall)+" where id="+str(id))
            db.commit()
            print("update ucall successfully!")
            return "1"
        except Exception as e:
            print("update ucall failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

#更新用户     备注          9.1 可行
@app.route('/用户表/updateremark', methods=['POST'])
def login_update_remark():
    if request.method == "POST":
        id = request.form.get("id")
        remark = request.form.get("remark")
        try:
            cursor.execute("update `用户表` set remark=\""+str(remark)+"\" where id="+str(id))
            db.commit()
            print("update role successfully!")
            return "1"
        except Exception as e:
            print("update role failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

#更新用户     管理员备注          9.2    可行
@app.route('/用户表/updatemremark', methods=['POST'])
def login_update_mremark():
    if request.method == "POST":
        id = request.form.get("id")
        mremark = request.form.get("mremark")
        try:
            cursor.execute("update `用户表` set mremark=\""+str(mremark)+"\" where id="+str(id))
            db.commit()
            print("update mremark successfully!")
            return "1"
        except Exception as e:
            print("update mremark failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"
        




#查询用户信息
        #查询用户   姓名的      11.1
@app.route('/用户表/selectusername',methods=['POST'])
def select_uname():
    if request.method == "POST":       #这里的username  要与前端保持一致
        uname = request.form.get("uname")
        cursor.execute("SELECT login.id,username,uname,idcard,ucall,remark,mremark,login.ctime FROM login JOIN `用户表` on login.id=`用户表`.id where uname=\""+str(uname)+"\" ")
        data = cursor.fetchall();
        temp = {}
        result = []
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["uname"]=i[2]
                temp["idcard"]=i[3]
                temp["ucall"]=i[4]
                temp["remark"]=i[5]
                temp["mremark"]=i[6]
                temp["ctime"]=i[7]
                result.append(temp.copy())
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result:NULL")
            return jsonify([])

#查询用户   id的            11.2       可行
@app.route('/用户表/selectuserid',methods=['POST'])
def select_userid():
    if request.method == "POST":       #这里的username  要与前端保持一致
        id = request.form.get("id")
        cursor.execute("SELECT login.id,username,uname,idcard,ucall,remark,mremark,login.ctime FROM login JOIN `用户表` on login.id=`用户表`.id where login.id="+str(id))
        data = cursor.fetchall();
        temp = {}
        result = []
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["uname"]=i[2]
                temp["idcard"]=i[3]
                temp["ucall"]=i[4]
                temp["remark"]=i[5]
                temp["mremark"]=i[6]
                temp["ctime"]=i[7]
                result.append(temp.copy())
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result:NULL")
            return jsonify([])

#查询用户   用户名的            11.3       可行
@app.route('/用户表/selectusername1',methods=['POST'])
def select_username():
    if request.method == "POST":       #这里的username  要与前端保持一致
        username = request.form.get("username")
        cursor.execute("SELECT login.id,username,uname,idcard,ucall,remark,mremark,login.ctime FROM login JOIN `用户表` on login.id=`用户表`.id where username=\""+str(username)+"\" ")
        data = cursor.fetchall();
        temp = {}
        result = []
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["uname"]=i[2]
                temp["idcard"]=i[3]
                temp["ucall"]=i[4]
                temp["remark"]=i[5]
                temp["mremark"]=i[6]
                temp["ctime"]=i[7]
                result.append(temp.copy())
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result:NULL")
            return jsonify([])

#查询用户   idcard的            11.4       可行
@app.route('/用户表/selectuseridcard',methods=['POST'])
def select_useridcard():
    if request.method == "POST":       #这里的username  要与前端保持一致
        idcard = request.form.get("idcard")
        cursor.execute("SELECT login.id,username,uname,idcard,ucall,remark,mremark,login.ctime FROM login JOIN `用户表` on login.id=`用户表`.id where idcard="+str(idcard))
        data = cursor.fetchall();
        temp = {}
        result = []
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["uname"]=i[2]
                temp["idcard"]=i[3]
                temp["ucall"]=i[4]
                temp["remark"]=i[5]
                temp["mremark"]=i[6]
                temp["ctime"]=i[7]
                result.append(temp.copy())
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result:NULL")
            return jsonify([])
        

#更改员工信息        名字  11 可
@app.route('/员工表/update_mname', methods=['POST'])
def login_update_mname():
    if request.method == "POST":
        id = request.form.get("id")
        mname = request.form.get("mname")
        try:
            cursor.execute("update `员工表` set mname=\""+str(mname)
                            +"\" where id="+str(id))
            db.commit()
            print("update role successfully!")
            return "1"
        except Exception as e:
            print("update role failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

#更新员工    电话           12 可
@app.route('/员工表/updatemcall', methods=['POST'])
def login_update_mcall():
    if request.method == "POST":
        id = request.form.get("id")
        mcall = request.form.get("mcall")
        try:
            cursor.execute("update `员工表` set mcall="+str(mcall)+" where id="+str(id))
            db.commit()
            print("update mcall successfully!")
            return "1"
        except Exception as e:
            print("update mcall failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

#更改员工  年龄          可         13
@app.route('/员工表/update_age', methods=['POST'])
def login_update_age():
    if request.method == "POST":
        id = request.form.get("id")
        age = request.form.get("age")
        try:
            cursor.execute("update `员工表` set age=\""+str(age)
                            +"\" where id="+str(id))
            db.commit()
            print("update age successfully!")
            return "1"
        except Exception as e:
            print("update age failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

#更改员工  工龄          可         13.2
@app.route('/员工表/update_worktime', methods=['POST'])
def login_update_worktime():
    if request.method == "POST":
        id = request.form.get("id")
        worktime = request.form.get("worktime")
        try:
            cursor.execute("update `员工表` set worktime=\""+str(worktime)
                            +"\" where id="+str(id))
            db.commit()
            print("update worktime successfully!")
            return "1"
        except Exception as e:
            print("update worktime failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"

#更改员工  职称          可          14
@app.route('/员工表/update_job', methods=['POST'])
def login_update_job():
    if request.method == "POST":
        id = request.form.get("id")
        job = request.form.get("job")
        try:
            cursor.execute("update `员工表` set job=\""+str(job)
                            +"\" where id="+str(id))
            db.commit()
            print("update age successfully!")
            return "1"
        except Exception as e:
            print("update age failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"


#更改员工  用户名                   
@app.route('/员工表/update_username', methods=['POST'])
def login_updateusername():
    if request.method == "POST":
        id = request.form.get("id")
        username = request.form.get("username")
        try:
            cursor.execute("update login set username=\""+str(username)
                            +"\" where id="+str(id))
            db.commit()
            print("update username successfully!")
            return "1"
        except Exception as e:
            print("update username failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"
        
        
#添加管理员账户      15 可行
@app.route('/login/add', methods=['POST'])
def login_add():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        try:
            cursor.execute("insert into login(username,password,role) values (\""
                            +str(username)+"\",\""+str(password)+"\",\""+
                            str(role)+"\")")
            db.commit() #提交，使操作生效
            print("add a new user successfully!")
            return "1"
        except Exception as e:
            print("add a new user failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"       



#增加用户信息           不用         
@app.route('/用户表/useradd',methods=['POST'])
def add_user():
    if request.method == "POST":#这里的username  要与前端保持一致
        id = request.form.get("id")
        uname = request.form.get("uname")
        idcard = request.form.get("idcard")
        ucall = request.form.get("ucall")
        password = request.form.get("password")
        remark = request.form.get("remark")
        #role = request.form.get("")
        try:
            cursor.execute(" INSERT INTO `用户表`(id,uname,idcard,ucall,remark)  VALUES ("+str(id)+",\""+str(uname)+"\","+str(idcard)+",\""+str(ucall)+"\",\""+str(remark)+"\")")
            db.commit()                #提交表单的操作，必须加的
            print("add a new user successfully")
            return "1"
        except Exception as e:
            print("add a new user falied:",e)
            db.rollback()
            return "-1"


#增加        员工首次添加信息               可行
@app.route('/员工表/mangeradd',methods=['POST'])
def add_mangerone():
    if request.method == "POST":#这里的username  要与前端保持一致
        id = request.form.get("id")
        mname = request.form.get("mname")
        job = request.form.get("job")
        mcall = request.form.get("mcall")
        #password = request.form.get("password")
        age = request.form.get("age")
        try:
            cursor.execute("INSERT INTO `员工表`(id,mname,age,mcall,job) VALUES ("+str(id)+",\""+str(mname)+"\","+str(age)+",\""+str(mcall)+"\",\""+str(job)+"\")")
            db.commit()                #提交表单的操作，必须加的
            print("add a new manger successfully")
            return "1"
        except Exception as e:
            print("add a new manger falied:",e)
            db.rollback()
            return "-1"
        

        
#删除 login加用户 全部信息             两个表都删除了 可行        管理第一个界面用的     16
@app.route('/用户表/userdelete',methods=['POST'])
def del_user():
    if request.method == "POST":#这里的username  要与前端保持一致
        id = request.form.get("id")
        try:
            cursor.execute("DELETE login,`用户表` FROM login JOIN `用户表` ON login .id = `用户表`.id WHERE login.id="+str(id))
            db.commit()     
            print("delete a new user successfully")
            return "1"    
        except Exception as e:
            print("delete a new user falied:",e)
            db.rollback()
            return "-1"

#删除 用户   信息             未改        光删除用户的密码和用户名     17
@app.route('/login/userdelete1',methods=['POST'])
def del_userone():
    if request.method == "POST":#这里的username  要与前端保持一致
        id = request.form.get("id")
        try:
            cursor.execute("DELETE login FROM login  WHERE id="+str(id))
            db.commit()     
            print("delete a new user successfully")
            return "1"    
        except Exception as e:
            print("delete a new user falied:",e)
            db.rollback()
            return "-1"


#删除员工信息           可       18
@app.route('/员工表/userdeleteall',methods=['POST'])
def del_user_login():
    if request.method == "POST":#这里的username  要与前端保持一致
        id = request.form.get("id")
        try:
            cursor.execute("DELETE FROM `员工表` WHERE id="+str(id))
            db.commit()     
            print("delete a new user successfully")
            return "1"    
        except Exception as e:
            print("delete a new user falied:",e)
            db.rollback()
            return "-1"

        


#显示管理者全部信息            可用      19
@app.route('/员工表/mangerall',methods=['POST'])
def select_manger():
    if request.method == "POST":       #这里的username  要与前端保持一致
        cursor.execute("SELECT login.id,mid,username,mname,age,job,worktime,mcall,`员工表`.ctime FROM login join `员工表` on login.id=`员工表`.id")
        data = cursor.fetchall();
        temp = {}
        result = []   
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["mid"]=i[1]
                temp["username"]=i[2]
                temp["mname"]=i[3]
                temp["age"]=i[4]
                temp["job"]=i[5]
                temp["worktime"]=i[6]
                temp["mcall"]=i[7]                
                temp["ctime"]=i[8]
                result.append(temp.copy())
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result:NULL")
            return jsonify([])

#查询员工个人信息
@app.route('/员工表/mangerone',methods=['POST'])
def select_mangerone():
    if request.method == "POST":       #这里的username  要与前端保持一致
        id = request.form.get("id")
        cursor.execute("SELECT mid,username,mname,job,age,mcall,worktime,`员工表`.ctime FROM login join `员工表` on login.id=`员工表`.id where login.id="+str(id))
        data = cursor.fetchall();
        temp = {}
        result = []   
        if(data!=None):
            for i in data:
                temp["mid"]=i[0]
                temp["username"]=i[1]
                temp["mname"]=i[2]
                temp["job"]=i[3]
                temp["age"]=i[4]
                temp["mcall"]=i[5]
                temp["worktime"]=i[6]               
                temp["ctime"]=i[7]
                result.append(temp.copy())
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result:NULL")
            return jsonify([])
 
#添加管理员信息               超级管理员    员工管理   可行
@app.route('/员工表/mangeradd',methods=['POST'])
def add_manger():
    if request.method == "POST"                                                     :#这里的username  要与前端保持一致
        id = request.form.get("id")
        mname = request.form.get("mname")
        mcall = request.form.get("mcall")
        worktime = request.form.get("worktime")
        age = request.form.get("age")
        job = request.form.get("job")
        try:
            cursor.execute("INSERT INTO `员工表`(id,mname,age,job,worktime,mcall)  VALUES ("+str(id)+",\""+str(mname)+"\","+str(age)+",\""+str(job)+"\","+str(worktime)+",\""+str(mcall)+"\")")
            db.commit()                                  #提交表单的操作，必须加的
            print("add a new user successfully")
            return "1"
        except Exception as e:
            print("add a new user falied:",e)
            db.rollback()
            return "-1"

#删除管理员      账户、个人信息全部删除            20
@app.route('/员工表/mangerdelete',methods=['POST'])
def del_manger():
    if request.method == "POST":#这里的username  要与前端保持一致
        mid = request.form.get("mid")
        try:
            cursor.execute("DELETE login,`员工表` FROM login JOIN `员工表` ON login.id=`员工表`.id WHERE mid="+str(mid))
            db.commit()     
            print("delete a new manger successfully")
            return "1"
        except Exception as e:
            print("delete a new manger falied:",e)
            db.rollback()
            return "-1"

#用户查询自己的信息4   可行       21
@app.route('/用户表/userone',methods=['POST'])
def select_userself():
    if request.method == "POST":       #这里的username  要与前端保持一致
        id = request.form.get("id")
        cursor.execute("SELECT login.id,username,uname,idcard,ucall,remark,login.ctime FROM login JOIN `用户表` on login.id=`用户表`.id where login.id="+str(id))
        data = cursor.fetchall();
        temp = {}
        result = []
        if(data!=None):
            for i in data:
                temp["id"]=i[0]
                temp["username"]=i[1]
                temp["uname"]=i[2]
                temp["idcard"]=i[3]
                temp["ucall"]=i[4]
                temp["remark"]=i[5]
                temp["ctime"]=i[6]
                result.append(temp.copy())
            print("result:",len(data))
            return jsonify(result)
        else:
            print("result:NULL")
            return jsonify([])

        
#用户修改自己的    用户名          可              22
@app.route('/用户表/updateusername', methods=['POST'])
def login_update_username():
    if request.method == "POST":
        id = request.form.get("id")
        username = request.form.get("username")
        try:
            cursor.execute("update login set username=\""+str(username)
                            +"\" where id="+str(id))
            db.commit()
            print("update username successfully!")
            return "1"
        except Exception as e:
            print("update username failed:",e)
            db.rollback() #发生错误就回滚
            return "-1"        
    
if  __name__ =="__main__":         #name和main   都是双下划线
    app.run(host='0.0.0.0',port=8899)
    db.close()
    print("good bye!")
