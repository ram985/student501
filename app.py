from flask import Flask,redirect,url_for,request,render_template,flash,session,send_file,abort
import mysql.connector
from io import BytesIO      # the files in the form of bytes
import io
from flask_session import Session
from flask_mysqldb import MySQL
from key import secret_key,salt,salt2
from itsdangerous import URLSafeTimedSerializer
from stoken import token
from stoken1 import token1
from cmail import sendmail
app=Flask(__name__)
app.secret_key=secret_key

app.config['SESSION_TYPE'] = 'filesystem'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'students_records'
Session(app)
mysql = MySQL(app)
app.config['SESSION_TYPE']='filesystem'

#-----------------------------------------------admin register--------------------------
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/alogin',methods=['GET','POST'])
def alogin():
    if session.get('admin'):
        return redirect(url_for('home'))
    if request.method=='POST':
        id1=request.form['id1']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT count(*) from admin where id=%s and password=%s',[id1,password])
        count=cursor.fetchone()[0]
        if count==1:
            session['admin']=id1
            return redirect(url_for('admindashboard'))
        else:
            flash('Invalid username or password')
            return render_template('login.html')
    return render_template('login.html')
@app.route('/homepage')
def home():
    if session.get('admin'):
        return redirect(url_for('allstudents'))
    else:
        return redirect(url_for('alogin'))
@app.route('/aregistration',methods=['GET','POST'])
def aregistration():
    if request.method=='POST':
        id1=request.form['id']
        email=request.form['email']
        phnumber=request.form['phnumber']
        password=request.form['password']
        ccode=request.form['ccode']
        code="codegnan@9"
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from admin where id=%s',[id1])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from admin where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if code==ccode:
            if count==1:
                flash('username already in use')
                return render_template('registration.html')
            elif count1==1:
                flash('Email already in use')
                return render_template('registration.html')
            data={'id1':id1,'email':email,'phnumber':phnumber,'password':password}
            subject='Email Confirmation'
            body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('aconfirm',token=token(data,salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Confirmation link sent to mail')
            return redirect(url_for('alogin'))
        else:
            flash('unauthorized access')
            return render_template('registration.html')
    return render_template('registration.html')
@app.route('/aconfirm/<token>')
def aconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
      
        return 'Link Expired register again'
    else:
        cursor=mysql.connection.cursor()
        id1=data['id1']
        cursor.execute('select count(*) from admin where id=%s',[id1])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('alogin'))
        else:
            cursor.execute('insert into admin values(%s,%s,%s,%s)',[data['id1'],data['email'],data['phnumber'],data['password']])
            mysql.connection.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('alogin'))


@app.route('/aforget',methods=['GET','POST'])
def aforgot():
    if request.method=='POST':
        id1=request.form['id1']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from admin where id=%s',[id1])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mysql.connection.cursor()

            cursor.execute('SELECT email  from admin where id=%s',[id1])
            email=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('areset',token=token(id1,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('alogin'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/areset/<token>',methods=['GET','POST'])
def areset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mysql.connection.cursor()
                cursor.execute('update  admin set password=%s where id=%s',[newpassword,id1])
                mysql.connection.commit()
                flash('Reset Successful')
                return redirect(url_for('alogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')
@app.route('/alogout')
def alogout():
    if session.get('admin'):
        session.pop('admin')
        flash('Successfully loged out')
        return redirect(url_for('alogin'))
    else:
        return redirect(url_for('alogin'))
#=====================================================================================================#
@app.route('/admindashboard')
def admindashboard():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select groupname from grouptable where added_by =%s',[session.get('admin')])
        groups=cursor.fetchall()
        return render_template('admindashboard.html',groups=groups)
    else:
        return redirect(url_for('alogin'))

#==================================== ADD STUDENNTS ROUTE -ADMIN===================================
@app.route('/addstudents',methods=['GET','POST'])
def addstudents():
    if session.get('admin'):
        if request.method=='POST':
            rollno=request.form['rollno']
            fname=request.form['fname']
            lname=request.form['lname']
            fathername=request.form['fathername']
            mothername=request.form['mothername']
            phnumber=request.form['phnumber']
            email=request.form['email']
            branch=request.form['branch']
            stu_year=request.form['year']
            cursor=mysql.connection.cursor()
            cursor.execute('select count(*) from students where rollno=%s',[rollno])
            count=cursor.fetchone()[0]
            if count==1: 
                flash('this rollno already exists')
            else:
                cursor.execute('insert into students values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',[rollno,fname,lname,phnumber,fathername,mothername,email,branch,stu_year])
                mysql.connection.commit()
                cursor.close()
                flash('student details are added')
                return redirect(url_for('allstudents'))
        return render_template('addstudents.html')

    else:
        return redirect(url_for('alogin'))
#============================================      all students details   ========================================
@app.route('/allstudents',methods=['GET','POST'])
def allstudents():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from students')

        data=cursor.fetchall()
        cursor.close()
        return render_template('allstudents.html',data=data)
    else:
        return redirect(url_for(alogin))
#===================================================== Create group ==============================================

@app.route('/creategroup',methods=['GET','POST'])
def creategroup():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select rollno from students')
        data=cursor.fetchall()
        cursor.execute('select groupname from grouptable where added_by=%s',[session.get('admin')])
        group=cursor.fetchall()
        cursor.execute(' select * from student_group where groupname in (select groupname from grouptable where added_by =%s)',[session.get('admin')])

        sadata=cursor.fetchall()
        if request.method=="POST":
            cursor=mysql.connection.cursor()
            cursor.execute('select groupname from grouptable where added_by=%s',[session.get('admin')])
            group_data=cursor.fetchall()
            group=request.form['group']
            if (group,) in group_data:
                flash("This Group Already Existed.......!")
            else:
                cursor.execute('insert into grouptable (groupname,added_by) values (%s,%s)',[group,session.get('admin')])
                mysql.connection.commit()
                cursor.execute('select rollno from students')
                data=cursor.fetchall()
                cursor.execute('select groupname from grouptable where added_by=%s',[session.get('admin')])
                group=cursor.fetchall()
                cursor.execute(' select * from student_group where groupname in (select groupname from grouptable where added_by =%s)',[session.get('admin')])
                sadata=cursor.fetchall()
                cursor.close()
            
        return render_template('creategroup.html',data=data,group=group,sdata=sadata)

    else:
        return redirect(url_for('alogin'))
#================================================== move students ==================================================
@app.route('/movetostudents',methods=['GET','POST'])
def movetostudents():
    if session.get('admin'):
        if request.method=="POST":
            sname=request.form['sname']
            sgroup=request.form['sgroup']
            cursor=mysql.connection.cursor()
            cursor.execute('select studentid,groupname from student_group')
            data=cursor.fetchall()
            if (int(sname), sgroup) in data:
                flash("Already Existed.....!")
            else:
                cursor.execute('insert into student_group (studentid,groupname) values (%s,%s)',[sname,sgroup])
                mysql.connection.commit()
                cursor.close()
            return redirect(url_for('creategroup'))
    else:
        return redirect(url_for('alogin'))

#=====================================================    Delete students  ========================================
@app.route('/deletestudents/<rollno>')
def deletestudents(rollno):
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('delete from students where rollno=%s',[rollno])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('allstudents'))
    else:
        return redirect(url_for('alogin'))
#==================================================    update students =========================================
@app.route('/updatestudents/<rollno>',methods=['GET','POST'])
def updatestudents(rollno):
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from students where rollno=%s',[rollno])
        items=cursor.fetchone()
        cursor.close()
        if request.method=='POST':
            fname=request.form['sfirstname']
            lname=request.form['sname']
            phnumber=request.form['phnumber']
            faname=request.form['sfathername']
            moname=request.form['smothername']
            branch=request.form['branch']
            syear=request.form['year']
            cursor=mysql.connection.cursor()
            cursor.execute('update students set s_firstname=%s,s_lastname=%s,phnumber=%s,father_name=%s,mothername=%s,branch=%s,stu_year=%s where rollno=%s',[fname,lname,phnumber,faname,moname,branch,syear,rollno])
            mysql.connection.commit()
            cursor.close()
            flash('student updated successfully')
            return redirect(url_for('allstudents'))
        return render_template('updatestudents.html',items=items)
    else:
        return redirect(url_for('alogin'))
#============================================   view particular group of the students =============================
@app.route('/branch/<branch>')
def branch(branch):
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from students where branch=%s',[branch])
        data=cursor.fetchall()
        
        return render_template('allstudents.html',data=data)
    return redirect(url_for('alogin'))

#=============================================   all assignment      ==============================================
@app.route('/allassignments',methods=['GET','POST'])
def allassignments():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select groupname from student_group where groupname in (select groupname from grouptable where added_by =%s)',[session.get('admin')])

        groups=cursor.fetchall()
       
    
        return render_template('allassignments.html',groups=groups)#data=data,
    else:
        return redirect(url_for('alogin'))
#================================================= see particular group assignments================================= 
@app.route('/groupassignments/<name>',methods=['GET','POST'])
def groupassignments(name):
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select a.studentid,a.groupname,b.assignmentname,b.filedata,b.status,b.marks,b.date from student_group as a left join assignment as b on a.studentid=b.rollno where a.groupname =%s' ,[name])
      
        data=cursor.fetchall()
        
    
        return render_template('allassignments.html',data=data)
    else:
        return redirect(url_for('alogin'))

#=============================================   add assignment ===================================
@app.route('/addassignment/<name>',methods=['GET','POST'])
def addassignment(name):
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select studentid from student_group where groupname=%s' ,[name])
        rollno=cursor.fetchall()
        cursor.execute('select * from assignment where groupname=%s',[name])
        data=cursor.fetchall()
     
        
        if request.method=="POST":
            studentid=request.form['rollno']
            aname=request.form['name']
            cursor.execute('insert into assignment (rollno,assignmentname,groupname) values(%s,%s,%s) ',[studentid,aname,name])
            mysql.connection.commit()
            return redirect(url_for('addassignment',name=name))

        return render_template('allocateassignment.html',rollno=rollno,data=data)
    else:
        return redirect(url_for('alogin'))
#--------------------------------------------    view assignment
@app.route('/assignmentview/<id1>')
def assignmentview(id1):
    if session.get('admin'):
        #rollno=session['user']
        cursor = mysql.connection.cursor()
        
        cursor.execute('select id,filedata from assignment where id=%s',[id1])
        data = cursor.fetchone()
        cursor.close()
        filename = str(data[0])
        bin_file = data[1]#unicode data(binary string-data)
        byte_data = BytesIO(bin_file)#covert binary file to bytes
        return send_file(byte_data,download_name=filename,as_attachment=False)#arguments of send_file(1st is byte data file
    #2.to convert the file in the given extension like(txt,pic,pdf)we need filename
    #if we want only the pdf file we use the mime_type(explicit convertion))
    else:
        return redirect(url_for('alogin'))


#----------------------------------------update assignment-----------------
@app.route('/updateassignment/<id1>', methods=['GET', 'POST'])
def updateassignment(id1):
    if session.get('admin'):
        if session.get('admin'): 
            if request.method == 'POST':
                status = request.form['status']
                marks = request.form['marks']
                cursor = mysql.connection.cursor()
                cursor.execute('select status from assignment where id=%s',[id1])
                current_status = cursor.fetchone()
                if current_status:
                    cursor.execute('UPDATE assignment SET status=%s WHERE id=%s',[status, id1])
                    mysql.connection.commit()
                    if status =='approved':
                        cursor.execute('UPDATE assignment SET marks=%s WHERE id=%s',[marks, id1])
                        mysql.connection.commit()
                        
                        cursor.close()
                        flash('assignment marks updated')
                        return redirect(url_for('admindashboard'))
                    else:
                        flash('student assignment  rejected')
                    return redirect(url_for('admindashboard'))


        return render_template('updateassignment.html')
    else:
        return redirect(url_for('alogin'))
#-------------------------------------------   search  for students-----------------------------
@app.route('/search',methods=['GET','POST'])
def search():
    if session.get('admin'):
        if request.method=="POST":
            name=request.form['search']
            cursor=mysql.connection.cursor()
            cursor.execute('select * from students where rollno=%s',[name])
            data=cursor.fetchall()
            return render_template('allstudents.html',data=data)
    return redirect(url_for('alogin'))
#------------------------------------- Delete assignment ----------------------------------
@app.route('/deleteassignment/<id1>')
def deleteassignment(id1):
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('delete from assignment where id=%s',[id1])
        mysql.connection.commit()
        cursor.close()
        flash('assignment deleted')
        return redirect(url_for('admindashboard'))
    return redirect(url_for('alogin'))
#--------------------------------------    ATTENDENCE  ------------------------------
@app.route('/attendence', methods=['GET', 'POST'])
def attendence():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute('select groupname from grouptable where added_by = %s',[session.get('admin')])
        data=cursor.fetchall()
        cursor.close()
        if request.method == 'POST':
            student_id = request.form['student_id']
            attendance_date = request.form['attendance_date']
            check_in_time = request.form['check_in_time']
            class1=request.form['class']
        
            cursor=mysql.connection.cursor()
            cursor.execute('select count(*) from students where rollno = %s',(student_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            if count == 0:
                flash('OOPS THE STUDENT IS NOT IN RECORDS !')
                return redirect(url_for('addstudents'))
            # Check if attendance record already exists for the given student and date
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM attendence WHERE student_id = %s AND attendence_date = %s"
            values = (student_id, attendance_date)
            cursor.execute(query, values)
            existing_record = cursor.fetchone()
            
            if not existing_record:
                # Insert new attendance record
                query = "INSERT INTO attendence (student_id, attendence_date, checkin,groupname) VALUES (%s, %s, %s,%s)"
                values = (student_id, attendance_date, check_in_time,class1)
                cursor.execute(query, values)
                mysql.connection.commit()
                return redirect(url_for('allattendance'))
            return redirect(url_for('allattendance'))
    
        return render_template('attendence.html',data=data)
    else:
        return redirect(url_for('alogin'))
#-------------------------------------- search particular rollno attendence
@app.route('/searcha',methods=['GET','POST'])
def searcha():
    if session.get('admin'):
        
        if request.method=="POST":
            name=request.form['search']
            cursor=mysql.connection.cursor()
            cursor.execute('select total_days from attendence')
            days=cursor.fetchone()
            cursor.execute('select * from attendence where student_id=%s',[name])
            attendance_records=cursor.fetchall()
            return render_template('attendencedetails.html', attendance_records=attendance_records,total=days)
    else:
        return redirect(url_for('alogin'))

#------------------------------- display the attendence

@app.route('/allattendance')
def allattendance():
    if session.get('admin'):

        cursor = mysql.connection.cursor()
        cursor.execute('select total_days from attendence')
        days=cursor.fetchone()
        cursor.execute(' select * from attendence where groupname in (select groupname from grouptable where added_by =%s)',[session.get('admin')])

        attendance_records = cursor.fetchall()
        return render_template('attendencedetails.html', attendance_records=attendance_records,total=days)
    return redirect(url_for('alogin'))

#--------------------------update the checkout

# Update Check-out Time and Calculate Attendance Percentage
@app.route('/update_checkout', methods=['GET','POST'])
def update_checkout():
    if session.get('admin'):
        attendence_id=request.form.get('attendence_id')
        if request.method == 'POST':
            attendance_id = request.form['attendance_id']
            checkout_time = request.form['checkout']
            
            # Update check-out time in the database
            cursor = mysql.connection.cursor()
            query = "UPDATE attendence SET checkout = %s WHERE student_id = %s"
            values = (checkout_time, attendance_id)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.execute('select student_id from attendence where student_id=%s',(attendance_id,))
            rollno=cursor.fetchone()
          
            
        
        return redirect(url_for('allattendance'))
     
    return redirect(url_for('alogin'))
#---------------------------------------- calculate percentage ---------------------------
@app.route('/calculate_percentage/<rollno>',methods=['GET','POST'])
def calculate_percentage(rollno):
    

    if session.get('admin'):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT total_days FROM attendence")
        total_days = cursor.fetchone()[0]
        if total_days!=None and total_days!=0:
            # Calculate present days
            # Fetch present days for the given roll number
            query = "SELECT COUNT(*) FROM attendence WHERE student_id = %s AND checkout IS NOT NULL"
            cursor.execute(query, (rollno,))
            present_days = cursor.fetchone()[0]
        

            # Calculate the attendance percentage
            attendance_percentage = (present_days / total_days) * 100

            # Update the attendance percentage in the database
            query = "UPDATE attendence SET attendencepercentage = %s WHERE student_id = %s"
            values = (attendance_percentage, rollno)
            cursor.execute(query, values)

            # Commit the changes
            mysql.connection.commit()

            # Close the database connection
            return redirect(url_for('allattendance'))
        else:
            flash('please enter total days properly')
            return redirect(url_for('allattendance'))
            
    return redirect(url_for('alogin'))
  #--------------------- --------------- total days -------------------------------------

@app.route('/totaldays',methods=['GET','POST'])
def totaldays():
    if session.get('admin'):
        if request.method=="POST":
            total=request.form['total']
            cursor=mysql.connection.cursor()
            cursor.execute("UPDATE attendence SET total_days = %s",[total])
            mysql.connection.commit()
            return redirect(url_for('update_checkout'))
        else:
            return 'total days not updated'
    else:
        return redirect(url_for('alogin')) 
#------------------------------------------------read contact us 
@app.route('/readcontactus')
def readcontactus():
    if session.get('admin'):
        cursor=mysql.connection.cursor()
        cursor.execute("select * from contactus ")
        contact=cursor.fetchall()
        return render_template('readcontactus.html',contact=contact)   
    else:
        return redirect(url_for('alogin'))        
#--------------------------------------------------------------------------------
#===================================== students register  ==============================================
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('studentsdashboard'))
    if request.method=='POST':
        id1=request.form['id1']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT count(*) from students_register where rollno=%s and password=%s',[id1,password])
        count=cursor.fetchone()[0]
        if count==1:
            session['user']=id1
            return redirect(url_for('studentsdashboard'))
        else:
            flash('Invalid username or password')
            return render_template('studentlogin.html')
    return render_template('studentlogin.html')

@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method=='POST':
        id1=request.form['id']
        name=request.form['name']
        email=request.form['email']
        branch=request.form['branch']
        password=request.form['password']
        ccode=request.form['ccode']
        code="codegnan@99"
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from students_register where rollno=%s',[id1])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from students_register where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if code==ccode:
            if count==1:
                flash('username already in use')
                return render_template('studentregistration.html')
            elif count1==1:
                flash('Email already in use')
                return render_template('studentregistration.html')
            data1={'id1':id1,'name':name,'email':email,'password':password,'branch':branch}
            subject='Email Confirmation'
            body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token1(data1,salt),_external=True)}"
            sendmail(to=email,subject=subject,body=body)
            flash('Confirmation link sent to mail')
            return redirect(url_for('login'))
        else:
            flash('unauthorized access')
            return render_template('studentregistration.html')
    return render_template('studentregistration.html')
@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt,max_age=180)
    except Exception as e:
   
        return 'Link Expired register again'
    else:
        cursor=mysql.connection.cursor()
        id1=data['id1']
        cursor.execute('select count(*) from students_register where rollno=%s',[id1])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.close()
            flash('You are already registerterd!')
            return redirect(url_for('login'))
        else:
            cursor.execute('insert into students_register values(%s,%s,%s,%s,%s)',[data['id1'],data['name'],data['email'],data['password'],data['branch']])
            mysql.connection.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('login'))


@app.route('/forget',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        id1=request.form['id1']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from students_register where  rollno=%s',[id1])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mysql.connection.cursor()

            cursor.execute('SELECT email  from students_register where rollno=%s',[id1])
            email=cursor.fetchone()[0]
            cursor.close()
            subject='Forget Password'
            confirm_link=url_for('reset',token=token1(id1,salt=salt2),_external=True)
            body=f"Use this link to reset your password-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Reset link sent check your email')
            return redirect(url_for('login'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        id1=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mysql.connection.cursor()
                cursor.execute('update  students_register set password=%s where rollno=%s',[newpassword,id1])
                mysql.connection.commit()
                flash('Reset Successful')
                return redirect(url_for('login'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        flash('Successfully loged out')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
@app.route('/studentsdashboard')
def studentsdashboard():
    if session.get('user'):
        return render_template('studentsdashboard.html')
    else:
        flash('OOPS! session expired please login here')
        return redirect(url_for('login'))

#=============================================   view student details    ====================

@app.route('/viewdetails')
def viewdetails():
    if session.get('user'):
        rollno= session['user']
        
        cursor = mysql.connection.cursor()
        cursor.execute('select count(*) from students where rollno = %s',(rollno,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            flash('sorry you are not in our data if you want to send message you can send here!')
            return render_template('contactus.html')
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('select * from students where rollno = %s',(rollno,))
            data = cursor.fetchall()
            return render_template('studentviewdetails.html',data = data)
        
    else:
        return redirect(url_for('login.html'))
#-------------------------------------------------assignment details----------------
@app.route('/assignmentdetails',methods=['GET','POST'])
def assignmentdetails():
    if session.get('user'):
        rollno= session['user']
        cursor = mysql.connection.cursor()
        cursor.execute('select count(*) from students where rollno = %s',(rollno,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            flash('sorry you are not in our data if you want to send message you can send here!')
            return render_template('contactus.html')
         #student assignment data
        else:
            cursor=mysql.connection.cursor()
            cursor.execute('select * from assignment where rollno=%s',[rollno])
            a_data = cursor.fetchall()
            if len(a_data) == None:
                flash('no assignment given')
            cursor.close()
            return render_template('assignmentdetails.html',a_data = a_data)
            
    else:
        return redirect(url_for('login.html'))
#================================================ upload the assignment ====================
@app.route('/uploadassignment/<id1>',methods=['GET','POST'])
def uploadassignment(id1):
    if session.get('user'):
        if request.method=='POST':
            file=request.files['file1']
            cursor =mysql.connection.cursor()
            cursor.execute('update assignment set filedata=%s  where id=%s',(file.read(),id1))
            mysql.connection.commit()
            return redirect(url_for('assignmentdetails'))
    else:
        return redirect(url_for('login'))
#-----------------------------------------------view uploaded file--------------------------------
@app.route('/viewfile/<id1>')
def viewfile(id1):
    if session.get('user'):
        cursor = mysql.connection.cursor()
        cursor.execute('select id,filedata from assignment where id=%s',[id1])
        data = cursor.fetchone()
        cursor.close()
        filename = str(data[0])
        bin_file = data[1]#unicode data(binary string-data)
        byte_data = BytesIO(bin_file)#covert binary file to bytes
        return send_file(byte_data,download_name=filename,as_attachment=False)#arguments of send_file(1st is byte data file
    #2.to convert the file in the given extension like(txt,pic,pdf)we need filename
    #if we want only the pdf file we use the mime_type(explicit convertion))
    else:
        return redirect(url_for('login')) 
#---------------------------------------------------- update assignment
@app.route('/editfile/<id1>',methods=['GET','POST'])
def editfile(id1):
    if session.get('user'):
        #rollno=session['user']
        if request.method=='POST':
            file=request.files['file1']
            cursor =mysql.connection.cursor()
            cursor.execute('update assignment set filedata=%s  where id=%s',(file.read(),id1))
            mysql.connection.commit()
            mysql.connection.close()
    
        flash('Assignment updated successfully')
        return redirect (url_for('assignmentdetails'))
    else:
        return redirect(url_for('login'))
#------------------------------------------------------students contact us  
@app.route('/contactus',methods=['GET','POST'])
def contactus():
    if session.get('user'):
       
        if request.method == 'POST':
            branch=request.form['branch']
            rollno = request.form['id']
            email = request.form['email']
            message = request.form['message']
            cursor = mysql.connection.cursor()
            cursor.execute('insert into contactus values(%s,%s,%s,%s)',[branch,rollno,email,message])
            mysql.connection.commit()
            cursor.close()
            flash('your feedback is submitted')
        return render_template('contactus.html')
    else:
        return redirect(url_for('login.html'))
   
#---------------------------------------------- view attenedence
@app.route('/viewattendance')
def viewattendance():
    if session.get('user'):
        student_id=session['user']
        cursor=mysql.connection.cursor()
        cursor.execute('select * from attendence where student_id=%s',[student_id]) 
        records=cursor.fetchall()
        return render_template('viewattendance.html',records=records)  
    else:
        return redirect(url_for('login.html'))

app.run(use_reloader=True,debug=True)



