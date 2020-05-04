import mysql.connector as sql
import mysql.connector
import cv2,os
from tkinter import*
import numpy as np
from tkinter import messagebox
import datetime
import time
import datetime
from datetime import date
mydb=mysql.connector.connect(host="localhost",user="root",password="",database="ml")
mycursor=mydb.cursor()
def Attendence(root1,getId,datee,cam):
	root1.destroy()
	cam.release()
	cv2.destroyAllWindows()	

	#count=myresult[2]
	
	

	root=Tk()
	root.geometry("600x400")
	root.config(background="#e0e0e0")
		
		
	nameL1=Label(root,text="Name: ",font=("times",15,"bold"))
	idL1=Label(root,text="Id: ",font=("times",15,"bold"))
	timeL1=Label(root,text="Time: ",font=("times",15,"bold"))
	dateL1=Label(root,text=" percentage",font=("times",15,"bold"))
	statusL1=Label(root,text="Status: ",font=("times",15,"bold"))
		
	nameE1=Entry(root,text="Enter Name: ",font=("times",15,"bold"))
	idE1=Entry(root,text="Enter RollNo: ",font=("times",15,"bold"))
	timeE1=Entry(root,text="Enter ContactNo: ",font=("times",15,"bold"))
	dateE1=Entry(root,text="Enter Marks: ",font=("times",15,"bold"))
	statusE1=Entry(root,text="Enter Email: ",font=("times",15,"bold"))
		
	nameL1.grid(row=1,column=2,padx="10",ipadx=10)
	idL1.grid(row=2,column=2,padx="10",ipadx=20)
	timeL1.grid(row=3,column=2,padx="10",ipadx=10)
	dateL1.grid(row=4,column=2,padx="10",ipadx=10)
	statusL1.grid(row=5,column=2,padx="10",ipadx=8)
		

		
	nameE1.grid(row=1,column=3,pady="10",ipadx="100",ipady="10")
	idE1.grid(row=2,column=3,ipadx="100",ipady="10",pady="10")
	timeE1.grid(row=3,column=3,ipadx="100",ipady="10",pady="10")
	dateE1.grid(row=4,column=3,ipadx="100",ipady="10",pady="10")
	statusE1.grid(row=5,column=3,ipadx="100",ipady="10",pady="10")
	t1=datetime.datetime.now()
	t=date.today()
	print(t,"mi")
	a=getId
	print(a,"mik")
	b=np.uint32(a).item()
	c=str(b)
	print("mik",c,"mik")
	print(type((c)))
	sql="SELECT * FROM employee WHERE id=%s"
	val=(c,)

	mycursor.execute(sql,val)
	myresult=mycursor.fetchall()
	print(myresult)

	for x in myresult:
		count1=x[2]
		dt=x[4]
	print(count1)
	print(dt)
	if(str(dt)==str(t)):
		for x in myresult:
			nameE1.insert(0,x[0])
			idE1.insert(0,x[1])
			#marE.insert(0,x[3])
			dateE1.insert(0,x[3])
			timeE1.insert(0,x[4])	
		statusE1.insert(0,"present")
		t1=t.day
		
	else:
		count2=count1+1
		sql="UPDATE employee SET count=%s where id=%s"
		val=(count2,c)
		mycursor.execute(sql,val)
		mydb.commit()
		print(" Updated....")
		sql="UPDATE employee SET Edate=%s where id=%s"
		val=(datee,c)
		mycursor.execute(sql,val)
		mydb.commit()
		print("Updated....")
		t1=t.day
		t2=datetime.datetime.now()
		per=(count2/t1)*100
		print(per)
		sql="UPDATE employee SET percentage=%s where id=%s"
		val=(per,c)
		mycursor.execute(sql,val)
		mydb.commit()
		print("Updated....")
		for x in myresult:
			nameE1.insert(0,x[0])
			idE1.insert(0,x[1])
			#marE.insert(0,x[3])
			#dateE1.insert(0,x[4])
		timeE1.insert(0,t2)	
		dateE1.insert(0,per)
		statusE1.insert(0,"present")
	root.mainloop()

	#break
	