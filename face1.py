from face2 import*
import cv2,os
import PIL.Image
import matplotlib.pyplot as plt
import csv
#from PIL import Image,ImageTk
import pandas as pd 
import PIL.Image
import datetime
import time
from datetime import timedelta 
import datetime
import mysql.connector as sql
import mysql.connector
from tkinter import messagebox
from os import listdir
from os.path import isfile,join
import numpy as np
import yaml
from datetime import date
from scipy.misc import imread
mydb=mysql.connector.connect(host="localhost",user="root",password="",database="ml")
mycursor=mydb.cursor()
from datetime import time


import numpy as np
from tkinter import*
root1=Tk()
root1.geometry("900x600")
root1.config(background="#e0e0e0")
	
name1=Label(root1,text="Enter Name",bg="#43abc9")
name1.config(font=("Verdana",24))	
name1.grid(row=1,column=2,ipadx=35,padx=60)
nameE1=Entry(root1,text="Enter Name: ",font=("times",15,"bold"))
nameE1.grid(row=1,column=3,pady="10",ipadx="120",ipady="13")


eid=Label(root1,text="Enter Id",bg="#43abc9")
eid.config(font=("Verdana",24))	
eid.grid(row=2,column=2,ipadx=65,padx=60)
eidE1=Entry(root1,text="Enter Id: ",font=("times",15,"bold"))
eidE1.grid(row=2,column=3,pady="10",ipadx="120",ipady="13")

def TakeImage():
	name=nameE1.get()
	idE=eidE1.get()
	print(type(idE))
	if name=="" or idE=="":
		messagebox.showinfo("Invalide","Plz Fill All Details")
	else:
		
		b=name
		c=idE
		sql="INSERT INTO employee(username,id,count,percentage,Edate)VALUES(%s,%s,%s,%s,%s)"
		val=(b,c,'0','0','0')
		mycursor.execute(sql,val)
		mydb.commit()
		messagebox.showinfo("valide","register Successfully....")
	
		cam=cv2.VideoCapture(0)
		print(type(cam))
		detector=cv2.CascadeClassifier('C:/Users/Abhi/Anaconda3/New folder/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
		count=0
		while(True):
			ret,img=cam.read()
			gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			face=detector.detectMultiScale(gray,1.3,5)
			for(x,y,w,h) in face:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				count=count+1
				cv2.imwrite('C:/Users/Abhi/Desktop/features/'+name+"."+idE+"."+str(count)+".jpg",gray[y:y+h,x:x+w])
				cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
				#cv2.waitKey()
				cv2.imshow('Frame',img)
			if cv2.waitKey(100) & 0xFF==ord('q'):
				break
			elif count >=20: 
				break
		cam.release()
		cv2.destroyAllWindows()
		#databasesave
		row=[idE,name]
		with open('EmployeeDetails/Employee.csv','a+')as csvFile:
			writer=csv.writer(csvFile)
			writer.writerow(row)
		csvFile.close()
		print("successfully")


def TrainImage():
	path="C:/Users/Abhi/Desktop/features/"
	time1=datetime.datetime.now()
	now = datetime.datetime.now() 
	today11am = now.replace(hour=11, minute=0, second=0, microsecond=0)

  
	#path="C:/Users/Abhi/Desktop/features/"
	if(now<=today11am):
		model= cv2.face.LBPHFaceRecognizer_create()
		onlyfiles=[f for f in listdir(path)if isfile(join(path,f))]
		print(onlyfiles)
		Training_data,Labels=[],[]
		for i,imagepath in enumerate(onlyfiles):
			image_path=path + onlyfiles[i]
			ID=os.path.split(imagepath)[-1].split(".")[1]
			images=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
			Training_data.append(np.asarray(images,dtype=np.uint8))
			
			Labels.append(ID)

			
		
			#images=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
			#Training_data.append(np.asarray(images,dtype=np.uint8))
			
		#Labels.append(ids1)
		print(Labels)
		Labels=np.asarray(Labels,dtype=np.int32)
		model.train(np.asarray(Training_data),np.asarray(Labels))
		model.save("E:/face1/trainningData1/Trainner1.yml")
		print("complete.....")
		face_classifier=cv2.CascadeClassifier('C:/Users/Abhi/Anaconda3/New folder/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
		temp=[]
		for x in Labels:
			if x not in temp:
				temp.append(x)
		print(temp)
		cam=cv2.VideoCapture(0)
		model= cv2.face.LBPHFaceRecognizer_create()
		#print(type(cam))
		model.read("E:/face1/trainningData1/Trainner1.yml")
		identity=0
		#font=cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX,5,1,0,4)
		#cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
		fontface = cv2.FONT_HERSHEY_COMPLEX
		fontscale = 1
		fontcolor = (255, 255, 255)
		ct=0
		a=[]
		f=0
		dict={}
		#cv2.putText(im, str(Id), (x,y+h), fontface, fontscale, fontcolor) 
		while(True):
			ret,img=cam.read()
			gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			face=face_classifier.detectMultiScale(gray,1.3,5)
			
			for(x,y,w,h) in face:
				cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
				#count=count+1
				#print(identity)
				ct=ct+1
				identity,conf=model.predict(gray[y:y+h,x:x+w])

				cv2.putText(img,str(identity),(x,y+h), fontface, fontscale, fontcolor)
				a.append(identity)
			if ct>20:
				
				ct1=0
				print(a)
				for i in temp:
					str(i)
					b=a.count(i)
					print(i,":",b)
					dict[i]=b#add
				print(dict)
				max=list(dict.keys())[0]
				print(max)
				max1=dict[max]
				for x in dict.values():
					if(x>max1):
						max1=x
				print(max1)
				key_list=list(dict.keys())
				value_list=list(dict.values())
				getId=key_list[value_list.index(max1)]
				print(getId,"mik")

				print(datetime.datetime.now())

				datee=date.today()


				print(date.today())
				t=date.today()
				print(t.day)
				print(t.month)
				print(t.year)
				Attendence(root1,getId,datee,cam)
				break

				#print(type(t.day))
				
				
				
				#root1.destroy()
				
				
					

			

				#print(len(a))


		
			cv2.imshow('face',img)
			if cv2.waitKey(100) & 0xFF==ord('q'):
				break
		
		
		cam.release()
		cv2.destroyAllWindows()
	else:
		messagebox.showinfo("invalide","u r late....")
now = datetime.datetime.now() 
print(now)
t=date.today()
t1=str(t)
print(t1)
today11am = now.replace(hour=11, minute=0, second=0, microsecond=0)
if(now>today11am):
	print("mikudi")

	sql="SELECT * FROM employeeab WHERE date_a!=%s"
	val=(t1,)

	mycursor.execute(sql,val)
	myresult1=mycursor.fetchall()
	print(myresult1)
	sql="SELECT * FROM employee WHERE Edate!=%s"
	val=(t1,)

	mycursor.execute(sql,val)
	myresult=mycursor.fetchall()
	mycursor.execute("SELECT * FROM employeeab")
	myresult2=mycursor.fetchall()
	x=len(myresult2)
	print(x)
	if x==0:
		
		#print(myresult)
		for x in myresult:
			a=x[0]
			b=x[1]
			c=t1
			sql="INSERT INTO employeeab(username,id,date_a)VALUES(%s,%s,%s)"
			val=(a,b,c)
			mycursor.execute(sql,val)
			mydb.commit()
			print("done")
	else:
		sql="SELECT * FROM employeeab WHERE date_a=%s"
		val=(t1,)

		mycursor.execute(sql,val)
		myresult4=mycursor.fetchall()
		
		x=len(myresult4)
		print(x)
		if x>0:
			print("already updated....")
		else:
			for x in myresult:
				a=x[0]
				b=x[1]
				c=t1
				sql="INSERT INTO employeeab(username,id,date_a)VALUES(%s,%s,%s)"
				val=(a,b,c)
				mycursor.execute(sql,val)
				mydb.commit()
				print("done232323")


		








'''root2=Tk()
root2.geometry("800x500")
root2.config(background="#e0e0e0")
	

title=Label(root2,text="Employee Records",background="#e0e0e0")
title.config(font=("Verdana",24))
title.grid(row=3,column=17,columnspan=10,ipadx="150",ipady=30,pady="40",padx=150,rowspan=120)


btn1=Button(root2,text="STATUS",bg="#43abc9",font=("times",15,"bold"),command=lambda:status(root2)).grid(row=150,column=20,pady=15,ipadx=270,ipady=15,padx=10)


###############################################################################################################3'''

def status(root1):
	t=date.today()
	
	
	t1=str(t)
	root1.destroy()
	root=Tk()
	root.title("")
	root.config(background="#e0e0e0")
	root.geometry("1000x500")
	
 
	
	heading=Label(root,text="    Status      ",bg="#e0e0e0")
	heading.config(font=("Courier",15))
	heading.grid(row=1,column=0,columnspan=4)

	sql="SELECT * FROM employee WHERE Edate=%s"
	val=(t1,)

	mycursor.execute(sql,val)
	myresult=mycursor.fetchall()
	i=6


	heading=Label(root,text="username",bg="pink")
	heading.config(font=("Courier",15))
	heading.grid(row=3,column=1)


	heading=Label(root,text="id",bg="pink")
	heading.config(font=("Courier",15))
	heading.grid(row=3,column=2)


	heading=Label(root,text="percentage",bg="pink")
	heading.config(font=("Courier",15))
	heading.grid(row=3,column=3)


	heading=Label(root,text="date",bg="pink")
	heading.config(font=("Courier",15))
	heading.grid(row=3,column=4)

	heading=Label(root,text="status",bg="pink")
	heading.config(font=("Courier",15))
	heading.grid(row=3,column=5)


	

	
	sql="SELECT * FROM employeeab WHERE date_a=%s"
	val=(t1,)

	mycursor.execute(sql,val)
	myresult1=mycursor.fetchall()
	

	for x in myresult:
		heading=Label(root,text=x[0],bg="#e0e0e0")
		heading.config(font=("Courier",15))
		heading.grid(row=i,column=1)
	
	
		heading10=Label(root,text=x[1],bg="#e0e0e0")
		heading10.config(font=("Courier",15))
		heading10.grid(row=i,column=2)

		heading10=Label(root,text=x[3],bg="#e0e0e0")
		heading10.config(font=("Courier",15))
		heading10.grid(row=i,column=3)

		heading10=Label(root,text=x[4],bg="#e0e0e0")
		heading10.config(font=("Courier",15))
		heading10.grid(row=i,column=4)


		heading10=Label(root,text='present',bg="#e0e0e0")
		heading10.config(font=("Courier",15))
		heading10.grid(row=i,column=5)

		

		i=i+1

	for x in myresult1:
		heading1=Label(root,text=x[0],bg="#e0e0e0")
		heading1.config(font=("Courier",15))
		heading1.grid(row=i,column=1)
		text=x[0]
		sql="SELECT percentage FROM employee WHERE username=%s"
		val=(text,)

		mycursor.execute(sql,val)
		myresult2=mycursor.fetchall()
		print(myresult2)
	
		heading11=Label(root,text=x[1],bg="#e0e0e0")
		heading11.config(font=("Courier",15))
		heading11.grid(row=i,column=2)

		heading11=Label(root,text=x[2],bg="#e0e0e0")
		heading11.config(font=("Courier",15))
		heading11.grid(row=i,column=4)

		heading11=Label(root,text=myresult2,bg="#e0e0e0")
		heading11.config(font=("Courier",15))
		heading11.grid(row=i,column=3)

		heading11=Label(root,text='absent',bg="#e0e0e0")
		heading11.config(font=("Courier",15))
		heading11.grid(row=i,column=5)



		i=i+1

	Button(root,text="Change Status",bg="#43abc9",font=("times",15,"bold"),command=lambda:loginb(root)).grid(row=i,column=1,pady=70,ipadx=350,ipady=10,padx=100,columnspan=5)
	print(i)
	
	
	root.mainloop()
#############################################################################################################################

def loginb(root):
	
	root.destroy()
	
		
	root3=Tk()
	root3.geometry("980x400")
	root3.config(background="#e0e0e0")
	
	
	uname1=Label(root3,text="Enter Name",bg="#43abc9")
	uname1.config(font=("Verdana",24))	
	uname1.grid(row=1,column=2,ipadx=92,padx=10)
	unameE1=Entry(root3,text="Enter Name: ",font=("times",15,"bold"))
	unameE1.grid(row=1,column=3,pady="10",ipadx="120",ipady="13")


	pass1=Label(root3,text="Enter Password",bg="#43abc9")
	pass1.config(font=("Verdana",24))	
	pass1.grid(row=2,column=2,ipadx=65,padx=60)
	passE1=Entry(root3,text="Enter Id: ",font=("times",15,"bold"))
	passE1.grid(row=2,column=3,pady="10",ipadx="120",ipady="13")
	
	Button(root3,text="Login",bg="#43abc9",font=("times",15,"bold"),command=lambda:check(root3,unameE1,passE1)).grid(row=8,column=2,pady=15,ipadx=300,ipady=10,columnspan=5,padx=100)
	

	root3.mainloop()

################################################################################################################################333

def upd(idE2,nameE2,statusE2,t1):
	f1=0
	f5=0
	b=idE2.get()
	#b=dateE2.get()
	print(b)
	sql="SELECT * FROM employee WHERE id=%s and Edate=%s"
	val=(b,t1)

	mycursor.execute(sql,val)
	myresult=mycursor.fetchall()
	if idE2.get()=="" :
		f1=1
		messagebox.showinfo("invalide","plz Enter valide id....")
		print("invalide")
	else:
	
		if myresult==[]:
			print(10)
			sql="SELECT * FROM employeeab WHERE id=%s and date_a=%s"
			val=(b,t1)

			mycursor.execute(sql,val)
			myresult1=mycursor.fetchall()
			for x in myresult1:
				nameE2.insert(0,x[0])
				statusE2.insert(0,'absent')
				f1=0
			
		else:	
			for x in myresult:
				
				
				nameE2.insert(0,x[0])
				statusE2.insert(0,'present')
				
				
				f1=0
	if f1==1:
		messagebox.showinfo("invalide","plz Enter valide id....")



def updateinfo(root4,idE2,statusE2,):
	
	a=statusE2.get()
	b=idE2.get()
	print(a,b)
	t=date.today()
	#print(t)
	t1=str(t)
	if a=="present":
		sql="SELECT * FROM employee WHERE id=%s"
		val=(b,)

		mycursor.execute(sql,val)
		myresult1=mycursor.fetchall()
		for x in myresult1:
			t2=x[2]
		t3=t2+1
		t4=str(t3)
		sql="UPDATE employee SET count=%s where id=%s"
		val=(t4,b)
		mycursor.execute(sql,val)
		mydb.commit()
		print(" Updated....")
		sql="UPDATE employee SET Edate=%s where id=%s"
		val=(t1,b)
		mycursor.execute(sql,val)
		mydb.commit()
		print(" Updated....")
		sql="DELETE FROM employeeab WHERE date_a=%s and id=%s"
		adr1=(t1,b)
		mycursor.execute(sql,adr1)
		mydb.commit()
		print(" deleteted....")
		t1=t.day
		t2=datetime.datetime.now()
		per=(t3/t1)*100
		print(per)
		sql="UPDATE employee SET percentage=%s where id=%s"
		val=(per,b)
		mycursor.execute(sql,val)
		mydb.commit()
		print("Updated....")
		#messagebox.showinfo("updated","info Updated...........")
	else:
		sql="SELECT * FROM employee WHERE id=%s"
		val=(b,)

		mycursor.execute(sql,val)
		myresult1=mycursor.fetchall()
		for x in myresult1:
			t2=x[2]
			t7=x[0]
		t3=t2-1
		print(t7)
		t4=str(t3)
		sql="UPDATE employee SET count=%s where id=%s"
		val=(t4,b)
		mycursor.execute(sql,val)
		mydb.commit()
		print(" Updated....")
		newd=date.today() - timedelta(days=1)
		sql="UPDATE employee SET Edate=%s where id=%s"
		val=(newd,b)
		mycursor.execute(sql,val)
		mydb.commit()
		print(" Updated....")
		sql="INSERT INTO employeeab(username,id,date_a)VALUES(%s,%s,%s)"
		val=(t7,b,t1)
		mycursor.execute(sql,val)
		mydb.commit()
		print(" deleteted....")
		t1=t.day
		t2=datetime.datetime.now()
		per=(t3/t1)*100
		print(per)
		sql="UPDATE employee SET percentage=%s where id=%s"
		val=(per,b)
		mycursor.execute(sql,val)
		mydb.commit()
		print("Updated....")
	root4.destroy()




	


def add(root3):
	
	root3.destroy()
	root4=Tk()

	root4.geometry("1100x500")
	root4.config(background="#e0e0e0")



	idL2=Label(root4,text="Enter id: ",bg="#43abc9")
	idL2.config(font=("Verdana",24))
	idE2=Entry(root4,text="Enter id: ",font=("times",15,"bold"))
	idL2.grid(row=2,column=2,ipadx=67,padx=60)
	idE2.grid(row=2,column=3,pady="10",ipadx="120",ipady="13")	
	t=date.today()
	#print(t)
	t1=str(t)
	
	Button(root4,text="FIND",bg="light blue",font=("times",15,"bold"),command=lambda:upd(idE2,nameE2,statusE2,t1)).grid(row=8,column=2,pady=15,ipadx=450,ipady=10,columnspan=15,padx=100)




	nameL2=Label(root4,text="Enter Name:",bg="#43abc9")
	nameL2.config(font=("Verdana",24))
	nameE2=Entry(root4,text="Enter name:",font=("times",15,"bold"))
	nameL2.grid(row=12,column=2,ipadx=40,padx=60)
	nameE2.grid(row=12,column=3,pady="10",ipadx="123",ipady="13")


	statusL2=Label(root4,text="Enter status:",bg="#43abc9")
	statusL2.config(font=("Verdana",24))
	statusE2=Entry(root4,text="Enter status:",font=("times",15,"bold"))
	statusL2.grid(row=11,column=2,ipadx=40,padx=60)
	statusE2.grid(row=11,column=3,pady="10",ipadx="120",ipady="13")
	
	
	
	
	
	Button(root4,text="UPDATEINFO",bg="light blue",font=("times",15,"bold"),command=lambda:updateinfo(root4,idE2,statusE2)).grid(row=16,column=2,pady=15,ipadx=400,ipady=10,columnspan=5,padx=100)
	
	
	root4.mainloop()
	

################################################################################################################################

def check(root3,unameE1,passE1):
	
	un=unameE1.get()
	print(un)
	pw=passE1.get()
	fl=0
	if un==" " or pw==" ":
		messagebox.showinfo("Empty Input","Plz Fill All Details")
	else:
		mycursor.execute("SELECT * FROM login")
		myresult=mycursor.fetchall()
		for x in myresult:
			if x[0]==un:
				if x[1]==pw:
					fl=1
	#print(x[2])
	if fl==1:
		messagebox.showinfo("valide","Login Successfully....")
		add(root3)
		
		
	else:
		messagebox.showinfo("Invalide Input","Plz Fill All Details")
	
	
	#root2.mainloop()




########################################################################






if(now>today11am):
	currentDT= datetime.datetime.now().time()
	print ("time: ",currentDT)
	currentDT1= datetime.datetime.now().date()
	print ("date: ",currentDT1)
	from calendar import monthrange
	num_days = monthrange(currentDT1.year, currentDT1.month)[1] 
	if currentDT1.day==num_days:
		print("the date is",currentDT1.day,"so this is the last day from this month")
		sql="UPDATE employee SET count=%s"
		val=(0,)
		mycursor.execute(sql,val)
		mydb.commit()
		print("Updated....")


		



		
#

Button(root1,text="Take Image",bg="#43abc9",font=("times",15,"bold"),command=TakeImage).grid(row=4,column=2,pady=15,ipadx=300,ipady=10,columnspan=5,padx=100)
Button(root1,text="Attendence",bg="#43abc9",font=("times",15,"bold"),command=TrainImage).grid(row=5,column=2,pady=10,ipadx=300,ipady=10,columnspan=5,padx=100)
Button(root1,text="Status",bg="#43abc9",font=("times",15,"bold"),command=lambda:status(root1)).grid(row=6,column=2,pady=10,ipadx=320,ipady=10,columnspan=5,padx=100)
Button(root1,text="Check",bg="#43abc9",font=("times",15,"bold")).grid(row=7,column=2,pady=10,ipadx=315,ipady=10,columnspan=5,padx=100)
	
root1.mainloop()


