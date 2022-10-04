
import base64
import time
from datetime import datetime
from email.mime.application import MIMEApplication
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from quoters import Quote
import pdfkit
import json
from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import jwt
from celery import Celery
from celery.schedules import crontab
from flask_cors import CORS 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from flask_sse import sse
from flask_restful import Resource,reqparse,Api
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///finalone.sqlite3"
app.secret_key="!@#$%^!@#$%&*()("
app.config["SECURITY_PASSWORD_SALT"]=")(*&^%$#$#%!@!@"
app.config["REDIS_URL"]="redis://localhost:6379"
app.config["CACHE_TYPE"]="RedisCache"
app.config["CACHE_REDIS_HOST"]="localhost"
app.config["CACHE_REDIS_PORT"]=6379
db=SQLAlchemy(app)
api=Api(app)
CORS(app)
bcrypt=Bcrypt(app)
cache=Cache(app)
app.register_blueprint(sse,url_prefix="/stream")
celery=Celery("test")
celery.conf.broker_url = "redis://localhost:6379/1"
celery.conf.result_backend = "redis://localhost:6379/2"
class users(db.Model):
    id=db.Column("id",db.Integer,primary_key=True,autoincrement=True)
    username=db.Column("username",db.String)
    email=db.Column("email",db.String)
    password=db.Column("password",db.String)
    def __init__(self,name,password,email):
        self.username=name
        self.password=password
        self.email=email
class trackers(db.Model):
    tid=db.Column("tid",db.Integer,primary_key=True,autoincrement=True)
    uid=db.Column("uid",db.Integer,db.ForeignKey("users.id"))
    name=db.Column("name",db.String)
    description=db.Column("description",db.String)
    types=db.Column("type",db.String)
    timestamp=db.Column("timestamp",db.String)
    subs=db.Column("subs",db.String)
    settings=db.Column("settings",db.String)
    def __init__(self,uid,name,description,types,timestamp,subs,settings):
        self.uid=uid
        self.description=description
        self.types=types
        self.timestamp=timestamp
        self.name=name
        self.subs=subs
        self.settings=settings
    def __str__(self):
        if(self.timestamp!=""):
            k=datetime.fromtimestamp(float(self.timestamp))
            y=datetime.strftime(k,"%d/%m/%Y %I:%M %p")
        else:
            y=""
        s={"tid":self.tid,"uid":self.uid,"name":self.name,"description":self.description,"types":self.types,"timestamp":y,"subs":self.subs,"settings":self.settings}
        return json.dumps(s)
class logs(db.Model):
    lid=db.Column("lid",db.Integer,primary_key=True,autoincrement=True)
    tracker=db.Column("tracker",db.Integer,db.ForeignKey("trackers.tid"))
    timestamp=db.Column("timestamp",db.String)
    value=db.Column("value",db.String)
    note=db.Column("note",db.String)
    def __init__(self,tracker,timestamp,value,note):
        self.tracker=tracker
        self.value=value
        self.timestamp=timestamp
        self.note=note

    def __str__(self):
        k=datetime.fromtimestamp(float(self.timestamp))
        y=datetime.strftime(k,"%d/%m/%Y %I:%M %p")
        s={"lid":self.lid,"tracker":self.tracker,"value":self.value,"note":self.note,"timestamp":y}
        return json.dumps(s)

class apiforuser(Resource):
    def get(self,id):
        try:
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            b=users.query.filter_by(id=id).first()
            if b != None:
                print(b.password)
                return {"name":b.username.strip()},200
            else:
                return "oops",400
        except:
            return "oops",400
    def post(self):
        try:
            print("reached")
            req=reqparse.RequestParser()
            req.add_argument("username")
            req.add_argument("email")
            req.add_argument("password")
            ans=req.parse_args()
            uname=ans.get("username",None)
            uemail=ans.get("email",None)
            upass=ans.get("password",None)
            t=users.query.filter_by(username=uname).first()
            if(t is not None):
                return {"message":"username already in use"},400
            if uname==None or upass==None:
                return {"message":"invalid name or password"},400
            if re.match("^[a-zA-Z0-9_]+$",uname)==None:
                return {"message":"invalid name or password"},400
            if re.match("^[a-zA-Z0-9]+@gmail.com",uemail)==None:
                return {"message":"invalid email address"},400
            newuserobj=users(uname,bcrypt.generate_password_hash(upass),uemail)
            db.session.add(newuserobj)
            print(newuserobj.id)
            db.session.commit()
            token=(jwt.encode({"id":newuserobj.id,"name":uname},key="!@#$%^&*(ASDFGHSDFGH"))
            return {"token":token.decode("UTF-8")}
        except:
            return "oops",400
    def delete(self,id):
        try:
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            if(b["id"]==id):
                alltrackers=trackers.query.filter_by(uid=id).all()
                for i in alltrackers:
                    logs.query.filter_by(tracker=i.tid).delete()
                    tracker.query.filter_by(tid=i.tid).delete()
                old=users.query.filter_by(id=id).first()
                db.session.delete(old)
                db.session.commit()
            else:
                return "u dont have access",400
            return "success",200
        except:
            return "oops",400
    def put(self):
        try:
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            req=reqparse.RequestParser()
            req.add_argument("username")
            req.add_argument("email")

            req.add_argument("password")
            ans=req.parse_args()
            uname=ans.get("username",None)
            uemail=ans.get("email",None)
            upass=ans.get("password",None)
            newuserobj=users.query.filter_by(id=b["id"]).first()
            if(newuserobj is not None):
                if(newuserobj.username is not None):
                    newuserobj.username=uname
                if(newuserobj.password is not None):
                    newuserobj.password=bcrypt.generate_password_hash(upass)
                if (newuserobj.email is not None):
                    newuserobj.email=uemail
            else:
                return "no such user",400
            # db.session.add(newuserobj)
            db.session.commit()
            return "success",200    
        except:
            return "oops",400

@cache.memoize(timeout=30)
def cache_for_logs(tid):
    print(tid)
    try:
        code=(request.headers.get("Authorization").split()[1])
        decodedtoken=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
        orgtrack=trackers.query.filter_by(tid=tid).first()
        if(decodedtoken["id"]==orgtrack.uid):
            b=logs.query.filter_by(tracker=tid).order_by(logs.timestamp).all()
            s=[]
            for k in b:
                if k==None:
                    continue
                print(k)
                s.append(json.loads(str(k)))
            print(" to check i am recomputed")
            if b != None:
                return s,200
            else:
                return "oops",400
        else:
            return "u dont have access",400
    except:
        return "oops",400

class apiforlogs(Resource):
    def get(self,tid):
        return cache_for_logs(tid)

    def post(self):
        try:
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            req=reqparse.RequestParser()
            req.add_argument("tracker")
            req.add_argument("timestamp")
            req.add_argument("value")
            req.add_argument("note")
            ans=req.parse_args()
            tracker=ans.get("tracker",None)
            value=ans.get("value",None)
            note=ans.get("note",None)
            timestamp=ans.get("timestamp",None)
            newlogobj=logs(tracker,timestamp,value,note)
            db.session.add(newlogobj)
            db.session.commit()
            tc=trackers.query.filter_by(tid=tracker).first()
            if tc.timestamp=="":
                tc.timestamp=timestamp
            else:
                prev=datetime.fromtimestamp(float(tc.timestamp))
                present=datetime.fromtimestamp(float(timestamp))
                print(present,prev)
                if((present-prev).total_seconds()>=0):
                    tc.timestamp=timestamp
            db.session.commit()
            with app.app_context():
                cache.delete_memoized(cache_for_logs)
                cache.delete_memoized(cache_for_tracker)
            return"success",200
        except:
            return "oops",404
    def delete(self,lid):
        try:
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            old=logs.query.filter_by(lid=lid).first()
            tid=old.tracker
            tc=trackers.query.filter_by(tid=tid).first()
            if(tc.uid==b["id"]):
                print("tid==",tid)
                print("before delete cache")
                print("after delete cache")
                db.session.delete(old)
                db.session.commit()
                can=logs.query.filter_by(tracker=tid).order_by(desc(logs.timestamp)).first()
                print(can)
                if (can!=None):
                    tc.timestamp=can.timestamp
                else:
                    tc.timestamp=""
                db.session.commit()
                cache.delete_memoized(cache_for_logs)
                cache.delete_memoized(cache_for_tracker)
                return "success",200
            else:
                return "u dont have access to the data",400
        except:
            return "oops",400
    def put(self,lid):
        try:
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            req=reqparse.RequestParser()
            req.add_argument("timestamp")
            req.add_argument("value")
            req.add_argument("note")
            ans=req.parse_args()
            value=ans.get("value",None)
            note=ans.get("note",None)
            timestamp=ans.get("timestamp",None)
            newlogobj=logs.query.filter_by(lid=lid).first()
            tack=trackers.query.filter_by(tid=newlogobj.tracker).first()
            if(tack.uid==b["id"]):
                tid=newlogobj.tracker
                newlogobj.value=value
                newlogobj.note=note
                if(timestamp!=None):
                    newlogobj.timestamp=timestamp
                db.session.commit()
                tc=trackers.query.filter_by(tid=tid).first()
                can=logs.query.filter_by(tracker=tid).order_by(desc(logs.timestamp)).first()
                print("can==",can)
                if (can):
                    tc.timestamp=can.timestamp
                else:
                    tc.timestamp=""
                db.session.commit()
                print("before delete cache")
                cache.delete_memoized(cache_for_logs)
                cache.delete_memoized(cache_for_tracker)
                print("after delete cache")
                return "success",200    
            else:
                return "permission denied",400
        except:
            return "oops",400

@cache.memoize(timeout=30)
def cache_for_tracker():
    try:
        code=(request.headers.get("Authorization").split()[1])
        b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
        print("s----------")
        print(b)
        uid=b["id"]
        b=trackers.query.filter_by(uid=uid).all()
        s=[]
        for k in b:
            print(k)
            s.append(json.loads(str(k)))
        print(s)
        if b != None:
            return s,200
        else:
            return "oops",400
    except:
        return "u dont have access to the resource.",400

class apifortracker(Resource):
    def get(self):
        return cache_for_tracker()
    def post(self):
        try:
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            req=reqparse.RequestParser()
            req.add_argument("uid")
            req.add_argument("name")
            req.add_argument("description")
            req.add_argument("types")
            req.add_argument("timestamp")
            req.add_argument("subs")
            req.add_argument("settings")

            ans=req.parse_args()
            name=ans.get("name",None)
            description=ans.get("description",None)
            types=ans.get("types",None)
            timestamp=ans.get("timestamp",None)
            subs=ans.get("subs",None)
            settings=ans.get("settings",None)
            print(b)
            newtrackerobj=trackers(b.get("id"),name,description,types,timestamp,subs,settings)
            db.session.add(newtrackerobj)
            db.session.commit()
            cache.delete_memoized(cache_for_tracker)
            return"success",200
        except:
            return "oops",400
    def delete(self,tid):
        try:
            print(" ia ma called")
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            old=trackers.query.filter_by(tid=tid,uid=b.get("id")).first()
            logs.query.filter_by(tracker=tid).delete()
            db.session.delete(old)
            db.session.commit()
            cache.delete_memoized(cache_for_tracker)
            return "success",200
        except:
            return "oops",400
    def put(self,tid):
        try:
            print("hip-hup huray \n\n\n\n\n")
            code=(request.headers.get("Authorization").split()[1])
            b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
            print(b)
            req=reqparse.RequestParser()
            req.add_argument("name")
            req.add_argument("description")
            req.add_argument("subs")
            ans=req.parse_args()
            name=ans.get("name",None)
            description=ans.get("description",None)
            subs=ans.get("subs",None)
            print(subs)
            newtrackerobj=trackers.query.filter_by(tid=tid,uid=b["id"]).first()
            newtrackerobj.name=name
            newtrackerobj.description=description
            newtrackerobj.subs=subs
            db.session.commit()
            cache.delete_memoized(cache_for_tracker)

            return "success",200    
        except:
            return "oops",400






api.add_resource(apiforuser,"/users/<id>","/newuser")
api.add_resource(apifortracker,"/tracker/<uid>","/tracker","/trackercrud/<tid>")
api.add_resource(apiforlogs,"/log/<tid>","/log","/logcrud/<lid>")


@app.route("/logview/<tid>")
def tracker(tid):
    try:
        code=(request.headers.get("Authorization").split()[1])
        b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
        print("s----------")
        print(b)
        uid=b["id"]
        b=trackers.query.filter_by(uid=uid,tid=tid).first()
        s=(json.loads(str(b)))
        print("sending......",s)
        if b != None:
            return s,200
        else:
            return "oops",400
    except:
        return "u dont have access to the resource.",400




@app.route("/login",methods=["POST"])
def testing():
    try:
        print("reached")
        print(request.headers)
        args=reqparse.RequestParser()
        args.add_argument("username")
        args.add_argument("password")
        ans=args.parse_args()
        uname=ans.get("username",None)
        passw=ans.get("password",None)
        if uname==None or passw==None:
            return {"message":"invalid name or password"},400
        if re.match("^[a-zA-Z0-9_]+$",uname)==None:
            return {"message":"invalid name or password"},400
        print(uname,passw)
        t=users.query.filter_by(username=uname).first()
        print(t)
        if t is not None and bcrypt.check_password_hash(t.password,passw.encode("UTF-8")):
            print("sending response")
            token=(jwt.encode({"id":t.id,"name":uname},key="!@#$%^&*(ASDFGHSDFGH"))
            return {"token":token.decode("UTF-8")}
        else:
            return {"message":"invalid name or password"},400
    except:
        return {"message":"invalid name or password"},400

@app.route("/exporttracker/<token>")
def trackerexporting(token):
    try:
        b=jwt.decode(token,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
        s=second_task.delay(uid=b.get("id"),token=token)
        return "Success",200
    except:
        return "invalid request",400
@app.route("/exportlog/<tid>/<token>")
def exporting(tid,token):
    try:
        slow_task.delay(tid=tid,token=token)
        return "Success",200
    except:
        return "internal error",500

@app.route("/")
def home():
    a=users.query.filter_by(id=1,username="summa").first()
    print(a)
    return "hello world"

@celery.task(name="slow_task")
def slow_task(tid,token):
    try:
        b=jwt.decode(token,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
        uid=b.get("id")
        b=logs.query.filter_by(tracker=tid).all()
        t=trackers.query.filter_by(tid=tid).first()
        a=open(str(t.name)+".csv","w")
        a.write("lid,tracker,value,note,timestamp\n")
        for k in b:
            if k==None:
                continue
            if(k.timestamp!=""):
                ks=datetime.fromtimestamp(float(k.timestamp))
                y=datetime.strftime(ks,"%d/%m/%Y %I:%M %p")
            else:
                y=""
            a.write(str(k.lid)+","+str(k.tracker)+","+str(k.value)+","+str(k.note)+","+str(y)+"\n")
        a.close()
        sendid=users.query.filter_by(id=uid).first().email
        postmail("the requested documents are attached..",sendid,"Exported logs",str(t.name)+".csv")
        with app.app_context():
            sse.publish({"message":"hello"},type=token)
        print("sending push notification")
    except:
        print("eeoer")
        pass
@celery.task(name="second_task")
def second_task(uid,token):
    try:
        b=trackers.query.filter_by(uid=uid).all()
        f=users.query.filter_by(id=uid).first()
        a=open(str(f.username)+".csv","w")
        a.write("tid,name,description,types,subs,settings,lastupdatetime\n")
        print(b)
        for k in b:
            if k==None:
                continue
            print(k)
            if(k.timestamp!=""):
                ks=datetime.fromtimestamp(float(k.timestamp))
                y=datetime.strftime(ks,"%d/%m/%Y %I:%M %p")
            else:
                y=""
            a.write(str(k.tid)+","+str(k.name)+","+str(k.description)+","+str(k.types)+","+str(k.subs)+","+str(k.settings)+","+str(y)+"\n")
        a.close()
        sendid=f.email
        postmail("the requested documents are attached..",sendid,"Exported trackers",str(f.username)+".csv")
        with app.app_context():
            sse.publish({"message":"hello"},type=token)
        print("sending push notification")
    except Exception as ep:
        print(ep)
        pass
@celery.task(name="send_email")
def send_email():
    try:
        userlist=users.query.filter_by().all()
        for i in userlist:
            remainder.delay({"username":i.username,"id":i.id,"email":i.email})
    except:
        pass
def makeatemplate(filename,data):
    with app.app_context():
        return render_template(filename,message=data,mot=Quote.print())

@celery.task(name="remainder")
def remainder(i):
    try:
        subslist=trackers.query.filter_by(uid=i.get("id"),subs=1).all()
        for j in subslist:
            if j.timestamp=="" or (abs(datetime.fromtimestamp(float(j.timestamp))-datetime.now()).days>=1):
                print("making template")
                mailcontent=makeatemplate("remainder.html",[i.get("username"),j.name])
                print("made tempate and send mail")
                postmail(mailcontent,i.get("email"),"Daily Remainder")
    except:
        print("error")
        pass

def postmail(actualmessage,send_id,subject,attachment=None):
    try:
        port=465
        server="smtp.gmail.com"
        sender_email="srivat0707@gmail.com"
        password="tuegxuyrdghcdrfi"
        message=MIMEMultipart()
        message["From"]=sender_email
        message["To"]=send_id
        message["Subject"]=subject
        message.attach(MIMEText(actualmessage,"html"))
        if attachment!=None:
            with open(attachment,"rb") as file:
                message.attach(MIMEApplication(file.read(),Name=attachment))
        context=ssl.create_default_context()
        with smtplib.SMTP_SSL(server,port,context=context) as server:
            server.login(sender_email,password)
            server.send_message(message)
            print("sent email")
    except:
        pass

@celery.task(name="monthlytask")
def monthlytask():
    t=datetime.now().month
    y=datetime.now().year
    tc=0
    ty=0
    if(t==1):
        tc=12
        ty=y-1
    else:
        tc=t-1
        ty=y
    userlist=users.query.all()
    for i in userlist:
        data=[]
        subslist=trackers.query.filter_by(uid=i.id).all()
        for j in subslist:
            if (j.types=="numerical" or j.types=="timeduration"):
                k=logs.query.filter_by(tracker=j.tid).order_by(desc(logs.timestamp)).all()
                validlogs=[]
                for each in k:
                    ks=datetime.fromtimestamp(float(each.timestamp))
                    y=datetime.strftime(ks,"%d/%m/%Y %I:%M %p")
                    if (int(y.split(" ")[0].split("/")[1])==tc and int(y.split(" ")[0].split("/")[2])==ty):
                        validlogs.append(each.value)
                    else:
                        break
                if(len(validlogs)>0):
                    data.append([j.types,j.name,len(validlogs),max(validlogs),min(validlogs)])
                else:
                    data.append([j.types,j.name,0,0,0])
            elif (j.types=="boolean"):
                k=logs.query.filter_by(tracker=j.tid).order_by(desc(logs.timestamp)).all()
                validlogs={"true":0,"false":0}
                for each in k:
                    ks=datetime.fromtimestamp(float(each.timestamp))
                    y=datetime.strftime(ks,"%d/%m/%Y %I:%M %p")
                    if (int(y.split(" ")[0].split("/")[1])==tc and int(y.split(" ")[0].split("/")[2])==ty):
                        if each.value=="true":
                            validlogs["true"]+=1
                        else:
                            validlogs["false"]+=1
                    else:
                        break
                print(validlogs)
                print("printing data...")
                print(validlogs["true"])
                print(validlogs["false"])
                print("data sent to matplot")
                print([validlogs["true"],validlogs["false"]],["true","false"])
                if(validlogs["false"]+validlogs["true"]==0):
                    data.append([j.types,j.name,validlogs["false"]+validlogs["true"],""])
                else:
                    plt.pie([validlogs["true"],validlogs["false"]],labels=["true","false"],autopct="%.1f")
                    new_graph_name = "tacker"+str(j.tid) +".png"
                    plt.savefig("static/"+new_graph_name)
                    plt.close()
                    ad=base64.b64encode(open("static/"+new_graph_name,"rb").read()).decode(encoding="ascii")
                    data.append([j.types,j.name,validlogs["false"]+validlogs["true"],ad])
            else:
                k=logs.query.filter_by(tracker=j.tid).order_by(desc(logs.timestamp)).all()
                alltypes=j.settings.split(";")
                validlogs={}
                total=0
                for t in alltypes:
                    validlogs[t]=0
                for each in k:
                    ks=datetime.fromtimestamp(float(each.timestamp))
                    y=datetime.strftime(ks,"%d/%m/%Y %I:%M %p")
                    if (int(y.split(" ")[0].split("/")[1])==tc and int(y.split(" ")[0].split("/")[2])==ty):
                        validlogs[each.value]+=1
                        total+=1
                    else:
                        break
                # print([validlogs[i] for i in validlogs.keys()],alltypes)
                if(total==0):
                    data.append([j.types,j.name,total,"",alltypes])
                else:   
                    plt.pie([validlogs[i] for i in validlogs.keys()],labels=alltypes,autopct="%.1f")
                    new_graph_name = "tacker"+str(j.tid) +".png"
                    plt.savefig("static/"+new_graph_name)
                    plt.close()
                    ad=base64.b64encode(open("static/"+new_graph_name,"rb").read()).decode(encoding="ascii")
                    data.append([j.types,j.name,total,ad,alltypes])
        print("making template")
        mailcontent=makeatemplate("monthlyreport.html",data)
        print("made tempate and send mail")
        #todo
        pdfkit.from_string(mailcontent,"out.pdf")
        postmail("The Monthly report can be found as an attachment with this mail 😊😊",i.email,"Monthly Report","report.pdf")
        print("done")

@app.route("/test")
def testingroute():
    t="xjzbxgcguteopnxu" 
    # vue account password
    b=monthlytask.delay()
    s=b.wait()
    return s 

@app.route("/importtracker",methods=["POST"])
def importing():
    try:
        code=(request.headers.get("Authorization").split()[1])
        b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
        d=(request.data.decode(encoding="ascii"))
        import_aysnc_one.delay(b=b,d=d,code=code)
        cache.delete_memoized(cache_for_logs)
        cache.delete_memoized(cache_for_tracker)
        return {"message":"s"},200
    except:
        return {"message":"oops"},400
@celery.task(name="import_aysnc_one")
def import_aysnc_one(b,d,code):
    try: 
        c=d.split("\n\r\n")[1].split("\n")
        for i in c[1:]:
            arr=i.split(",")
            if(arr[6]==""):
                y=arr[6]
            else:
                k=datetime.strptime(arr[6],"%d/%m/%Y %I:%M %p")
                y=(time.mktime(k.timetuple()))
            newtrac=trackers(name=arr[1],description=arr[2],types=arr[3],subs=arr[4],settings=arr[5],timestamp=y,uid=b["id"])
            db.session.add(newtrac)
        db.session.commit()
        with app.app_context():
            sse.publish({"message":"uploaded"},type=code)
        print("sending push notification")
    except:
        pass
@celery.task(name="import_aysnc_two")
def import_async_two(b,d,code):
    try:
        c=d.split("\n\r\n")[1].split("\n")
        print(c)
        for i in c[1:]:
            arr=i.split(",")
            if(arr[4]==""):
                y=arr[4]
            else:
                k=datetime.strptime(arr[4],"%d/%m/%Y %I:%M %p")
                y=(time.mktime(k.timetuple()))
            ctrac=trackers.query.filter_by(tid=arr[1]).first()
            if ctrac==None:
                return {"message":"please provide valid logs"},400
            newtrac=logs(tracker=arr[1],value=arr[2],note=arr[3],timestamp=y)
            db.session.add(newtrac)
        db.session.commit()
        with app.app_context():
            sse.publish({"message":"uploaded"},type=code)
        print("sending push notification")
    except:
        pass

@app.route("/importlog",methods=["POST"])
def importinglog():
    try:
        code=(request.headers.get("Authorization").split()[1])
        b=jwt.decode(code,key="!@#$%^&*(ASDFGHSDFGH",algorithms="HS256")
        d=(request.data.decode(encoding="ascii"))
        import_async_two.delay(b=b,d=d,code=code)
        cache.delete_memoized(cache_for_logs)
        cache.delete_memoized(cache_for_tracker)
        return {"message":"s"},200
    except:
        return {"message":"oops"},400

@celery.on_after_configure.connect
def setup_periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(crontab(hour=17,minute=30),send_email.s(),name="daily periodic jobs")
    sender.add_periodic_task(crontab(hour=1,minute=0,day_of_month=1),monthlytask.s(),name="monthly periodic jobs")

if __name__=="__main__":
    app.run(debug=True)

