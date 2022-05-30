import os
import pandas as pd
from flask import Flask,render_template,request,send_file,redirect,url_for,session
from werkzeug.utils import secure_filename
import shutil  
import time
import sqlite3
app = Flask(__name__)
#function used to verify a folder or file
def index_in_list(a_list, index):
    return(index < len(a_list))
app.secret_key="andreacravioto"
#endpoint for creating new directory
@app.route('/createdir',methods=['POST'])
def createdir():
    path = os.path.join("Files/"+request.form['address'], request.form['name'])
    os.mkdir(path)
    fileaddress=request.form['address']
    
    dir_list = os.listdir("./Files/"+fileaddress)
    last=[]


    for file in dir_list:
        last.append({'fun':"document.getElementById("+"'"+file+"'"+").submit()","files":[file,os.path.getsize('./Files/'+fileaddress+file)]})
    
    return render_template("sample.html",files=last,address=fileaddress)

#endpoint for uploading files
@app.route('/upload',methods=['POST'])
def upload():
    uploaded_file=request.files['file']  
    new_filename=secure_filename(uploaded_file.filename)
    uploaded_file.save('./Files/'+request.form['address'] +new_filename)
    fileaddress=request.form['address']
    
    dir_list = os.listdir("./Files/"+fileaddress)
    last=[]


    for file in dir_list:
        last.append({'fun':"document.getElementById("+"'"+file+"'"+").submit()","files":[file,os.path.getsize('./Files/'+fileaddress+file)]})
    
    return render_template("sample.html",files=last,address=fileaddress)  

#endpoint for downloading files
@app.route('/download',methods=['POST'])
def download_files():
    return send_file(request.form['address']+"/"+request.form['filename'])

#endpoint for going to the previous page
@app.route('/back',methods=['POST'])
def back():
    x=request.form['address'].split("/")
    addr=request.form['address'].replace(x[len(x)-2]+"/","")
    if addr=="":
        
        dir_list = os.listdir("./Files")

        last=[]
        for file in dir_list:
            last.append({'fun':"document.getElementById("+"'"+file+"'"+").submit()","files":[file,os.path.getsize('./Files/'+file)]})
        

        return render_template("sample.html",files=last,address="")
    else:
        
            
            
            dir_list = os.listdir("./Files/"+addr)
            last=[]


            for file in dir_list:
                last.append({'fun':"document.getElementById("+"'"+file+"'"+").submit()","files":[file,os.path.getsize('./Files/'+addr+file)]})
    
            return render_template("sample.html",files=last,address=addr)


#endpoint for renaming files
@app.route('/rename',methods=['POST'])
def rename_files():
    os.rename("./Files/"+request.form['address']+request.form['filename'],"./Files/"+request.form['address']+request.form['name'])
    
    dir_list = os.listdir("./Files/"+request.form['address'])
    last=[]


    for file in dir_list:
        last.append({'fun':"document.getElementById("+"'"+file+"'"+").submit()","files":[file,os.path.getsize('./Files/'+request.form['address']+file)]})
    
    return render_template("sample.html",files=last,address=request.form['address'])

#endpoint for deleting files
@app.route('/delete',methods=['POST'])
def delete_files():
    txt = request.form['filename']
    x = txt.split(".")
    content=[]
    if(index_in_list(x, 1)):
        os.remove("./Files/"+request.form['address']+request.form['filename'])
    else:
        try:
            shutil.rmtree("./Files/"+request.form['address']+request.form['filename'])
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))    
    
    dir_list = os.listdir("./Files/"+request.form['address'])
    last=[]


    for file in dir_list:
        last.append({'fun':"document.getElementById("+"'"+file+"'"+").submit()","files":[file,os.path.getsize('./Files/'+request.form['address']+file)]})
    
    return render_template("sample.html",files=last,address=request.form['address'])

#Main landing Page
@app.route('/folder',methods=['POST','GET'])
def Main():
    if request.method=='POST':
        txt = request.form['filename']
        x = txt.split(".")
        if(index_in_list(x, 1)):
            if x[1]=='csv':
                with open("./Files/"+request.form['address']+txt) as file:
                    df_firstn = pd.read_csv("./Files/"+request.form['address']+txt, nrows=2)
                return render_template("content.html",rows=df_firstn.to_html(),filename=txt,address="Files"+"/"+request.form['address'])
            elif x[1]=='xlsx' or x[1]=='xls':
                with open("./Files/"+request.form['address']+txt) as file:
                    df_firstn = pd.read_excel("./Files/"+request.form['address']+txt, nrows=2)
                return render_template("content.html",rows=df_firstn.to_html(),filename=txt,address="Files"+"/"+request.form['address'])

        else:
            filename=request.form['filename']
            fileaddress=request.form['address']
            
            dir_list = os.listdir("./Files/"+fileaddress+filename)
            last=[]


            for file in dir_list:
                last.append({'fun':"document.getElementById("+"'"+file+"'"+").submit()","files":[file,os.path.getsize('./Files/'+fileaddress+"/"+filename+"/"+file)]})
    
            return render_template("sample.html",files=last,address=fileaddress+filename+"/")            
    else:
        
        dir_list = os.listdir("./Files")

        last=[]
        for file in dir_list:
            last.append({'fun':"document.getElementById("+"'"+file+"'"+").submit()","files":[file,os.path.getsize('./Files/'+file)]})
        

    return render_template("sample.html",files=last,address="")

def func_type(x):
    y=x.split(".")
    if(len(y)==1):
        return "folder"
    else:
        if(y[len(y)-1]=="csv"):
            return "csv"
        elif(y[len(y)-1]=="xlsx"):
            return "xlsx"
        elif(y[len(y)-1]=="json"):
            return "json"


def parser(addr,arr):
    lst=os.listdir(addr)
    for x in lst:
        if(func_type(x)=="folder"):
            parser(addr+"/"+x,arr)
        elif(func_type(x)==request.form["type"]):
            arr.append([addr+"/"+x,x])

@app.route('/display',methods=['POST','GET'])  
def display():
    arr=[]
    if request.method=="GET":
        return render_template("display.html",files=[])
    else:
        
        parser("./Files",arr)
        
        return render_template("display.html",files=arr)

@app.route("/fileDisplay",methods=["POST"])
def fileDisplay():
    if func_type(request.form["filename"])=="csv":
        print(request.form["address"])
        data=pd.read_csv(request.form["address"],nrows=2)
        return render_template("content.html",rows=data.to_html(),address=request.form["address"].replace(request.form["filename"],""),filename=request.form["filename"])
    elif func_type(request.form["filename"])=="xlsx":
        data=pd.read_excel(request.form["address"],nrows=2)
        return render_template("content.html",rows=data.to_html(),address=request.form["address"].replace(request.form["filename"],""),filename=request.form["filename"])

@app.route("/api",methods=["POST","GET"])
def api():
    if request.method=="POST":
        content=request.form["content"]
        return render_template("api.html",content=content.upper())
    return render_template('api.html',content="")

@app.route("/",methods=["POST","GET"])
def landing():
    if (request.method=="POST"):
        with sqlite3.connect("./database/database.db") as con:
            c=con.execute("select * from users where username = '"+request.form["username"]+"' and password ='"+request.form["password"]+"';")     
            row=c.fetchone()
            if(row):
                session["desig"]=row[2]
                print(row[2])
                return redirect(url_for('home'))
            else:
                render_template("login.html")
        
    return render_template("login.html")

@app.route("/launch" ,methods=["POST","GET"])
def launch():
    time.sleep(10)
    return "done"

@app.route("/home")
def home():
    return render_template("home.html")
    
if __name__ == '__main__':
    app.run()  
