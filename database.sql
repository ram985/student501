-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: students_records
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` varchar(9) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phnumber` bigint DEFAULT NULL,
  `password` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('123456789','nagalakshmijarugulla2003@gmail.com',7816057287,'hi'),('23','gracekumari625@gmail.com',7788996655,'hello');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assignment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rollno` int DEFAULT NULL,
  `assignmentname` varchar(60) DEFAULT NULL,
  `filedata` longblob,
  `status` enum('approved','rejected','pending') DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `marks` varchar(3) NOT NULL DEFAULT 'NA',
  `groupname` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `assignment_ibfk_1` (`rollno`),
  KEY `groupname` (`groupname`),
  CONSTRAINT `assignment_ibfk_1` FOREIGN KEY (`rollno`) REFERENCES `students` (`rollno`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `assignment_ibfk_2` FOREIGN KEY (`groupname`) REFERENCES `grouptable` (`groupname`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignment`
--

LOCK TABLES `assignment` WRITE;
/*!40000 ALTER TABLE `assignment` DISABLE KEYS */;
INSERT INTO `assignment` VALUES (32,203907,'oops',_binary 'from itsdangerous import URLSafeTimedSerializer\r\nfrom key import secret_key\r\ndef token(data,salt):\r\n    serializer=URLSafeTimedSerializer(secret_key)\r\n    return serializer.dumps(data,salt=salt)','approved','2023-07-04 16:43:24','78','python'),(35,203907,'generations',_binary 'import random\r\ndef genotp():\r\n    u_c=[chr(i) for i in range(ord(\'A\'),ord(\'Z\')+1)]\r\n    l_c=[chr(i) for i in range(ord(\'a\'),ord(\'z\')+1)]\r\n    otp=\'\'\r\n    for i in range(3):\r\n        otp+=random.choice(u_c)\r\n        otp+=str(random.randint(0,9))\r\n        otp+=random.choice(l_c)\r\n    return otp\r\n','approved','2023-07-04 16:46:40','99','DBMS'),(36,203907,'functions',_binary 'from itsdangerous import URLSafeTimedSerializer\r\nfrom key import secret_key\r\ndef token(data,salt):\r\n    serializer=URLSafeTimedSerializer(secret_key)\r\n    return serializer.dumps(data,salt=salt)','rejected','2023-07-04 16:43:24','NA','python'),(38,8,'class',NULL,NULL,'2023-07-04 18:17:39','NA','python'),(39,123,'LBMS',_binary '                                #Diary Management\r\n\'\'\' installing all the packages that are needed to our project\'\'\'\r\nfrom flask import Flask,redirect,render_template,request,url_for,session,flash,send_file\r\nfrom flask_session import Session \r\nfrom flask_mysqldb import MySQL\r\nfrom io import BytesIO      # the files in the form of bytes\r\nimport io\r\nfrom itsdangerous import URLSafeTimedSerializer\r\n#from tokenreset import token1\r\nfrom stoken import token\r\nfrom cmail import sendmail\r\nfrom key import secret_key,salt1,salt2\r\nfrom itsdangerous import TimedJSONWebSignatureSerializer as Serializer\r\n\r\nimport random\r\napp=Flask(__name__)\r\napp.secret_key = secret_key\r\napp.config[\'SESSION_TYPE\'] = \'filesystem\'\r\napp.config[\'MYSQL_HOST\'] = \'localhost\'\r\napp.config[\'MYSQL_USER\'] = \'root\'\r\napp.config[\'MYSQL_PASSWORD\'] = \'admin\'\r\napp.config[\'MYSQL_DB\'] = \'spm\'\r\nSession(app)\r\nmysql = MySQL(app)\r\n@app.route(\'/\') \r\ndef index():\r\n    return render_template(\'index.html\')\r\n@app.route(\'/registration\', methods = [\'GET\',\'POST\'])\r\ndef register():\r\n    if request.method == \'POST\':\r\n       \r\n        name = request.form[\'name\']\r\n        \r\n        password = request.form[\'password\']\r\n        email = request.form[\'email\']\r\n        \r\n        \r\n        cursor = mysql.connection.cursor()\r\n       \r\n        cursor.execute (\'select email from students\')\r\n        edata = cursor.fetchall()\r\n          \r\n        if (email,)in edata:\r\n            flash(\'email already exits\')                                                                                                                                                                                                                                                                                                                                                                                                                                                         \r\n            return render_template(\'register.html\')\r\n        cursor.close()\r\n        data={\'username\':name,\'password\':password,\'email\':email}\r\n        subject=\'Email Confirmation\'\r\n        body=f\"Thanks for signing up\\n\\nfollow this link for further steps-{url_for(\'confirm\',token=token(data,salt1),_external=True)}\"\r\n        sendmail(to=email,subject=subject,body=body)\r\n        flash(\'confirmation link sent to mail\')\r\n        return redirect(url_for(\'login\'))\r\n    return render_template(\'register.html\')\r\n@app.route(\'/confirm/<token>\')\r\ndef confirm(token):\r\n    try:\r\n        serializer=URLSafeTimedSerializer(secret_key)\r\n        data=serializer.loads(token,salt=salt1,max_age=180)\r\n    except Exception as e:\r\n        return \'Link Expired register again\'\r\n    else:\r\n        cursor=mysql.connection.cursor()\r\n        username=data[\'email\']\r\n        cursor.execute(\'select count(*) from students where email=%s\',[username])\r\n        count=cursor.fetchone()[0]\r\n        if count==1:\r\n            cursor.close()\r\n            flash(\'You are already registerterd!\')\r\n            return redirect(url_for(\'login\'))\r\n        else:\r\n            cursor.execute(\'insert into students values(%s,%s,%s)\',[data[\'email\'],data[\'username\'],data[\'password\']])\r\n            mysql.connection.commit()\r\n            cursor.close()\r\n            flash(\'Details registered!\')\r\n            return redirect(url_for(\'login\'))\r\n@app.route(\'/login\',methods =[\'GET\',\'POST\'])\r\ndef login():\r\n    if session.get(\'user\'):\r\n        return redirect(url_for(\'home\'))\r\n    if request.method == \'POST\':\r\n        rollno = request.form[\'id\']\r\n        password = request.form[\'password\']\r\n        cursor = mysql.connection.cursor()\r\n        cursor.execute(\'select count(*) from students where email=%s and password=%s\',[rollno,password])#if the count is 0 then either username or password is wrong or if it is 1 then it is login successfully\r\n        count = cursor.fetchone()[0]\r\n        if count == 0:\r\n            flash(\'Invalid username or password\')\r\n            return render_template(\'login.html\')\r\n        else:\r\n            session[\'user\'] = rollno\r\n            return redirect(url_for(\'home\'))\r\n    return render_template(\'login.html\')\r\n@app.route(\'/studenthome\')\r\ndef home():\r\n    if session.get(\'user\'):\r\n        return render_template(\'home.html\')\r\n    else:\r\n        flash(\'login first\')#implemente flash\r\n        return redirect(url_for(\'login\'))   \r\n@app.route(\'/logout\')\r\ndef logout():\r\n    if session.get(\'user\'):\r\n        session.pop(\'user\')\r\n        flash(\'Successfully logged out\')\r\n        return redirect(url_for(\'login\'))\r\n    else:\r\n        return redirect(url_for(\'login\'))\r\n@app.route(\'/noteshome\')\r\ndef notehome():\r\n    if session.get(\'user\'):\r\n        rollno = session.get(\'user\')\r\n        cursor = mysql.connection.cursor()\r\n        cursor.execute(\'select * from diary where email = %s\',[rollno])\r\n        notes_data=cursor.fetchall()\r\n       \r\n        cursor.close()\r\n        return render_template(\'addnotetable.html\',data = notes_data)\r\n    else:\r\n        return redirect(url_for(\'login\'))\r\n@app.route(\'/addnotes\',methods = [\'GET\',\'POST\'])\r\ndef addnote():\r\n    if session.get(\'user\'):\r\n        if request.method == \'POST\':\r\n            title = request.form[\'title\']\r\n            content=request.form[\'content\']\r\n            cursor=mysql.connection.cursor()\r\n            rollno=session.get(\'user\')\r\n            cursor.execute(\'insert into diary(email,title,content) values (%s,%s,%s)\',[rollno,title,content])\r\n            mysql.connection.commit()\r\n            cursor.close()\r\n            flash(f\'{title} added successfully\')\r\n            return redirect (url_for(\'notehome\'))\r\n            \r\n            \r\n        return render_template(\'notes.html\')\r\n    else:\r\n        return redirect(url_for(\'login\'))\r\n@app.route(\'/viewnotes/<nid>\')\r\ndef viewnotes(nid):\r\n    cursor=mysql.connection.cursor()\r\n    cursor.execute(\'select title,content from diary where nid=%s\',[nid])\r\n    data=cursor.fetchone()#to fetch single row\r\n    return render_template(\'notesview.html\',data=data)\r\n@app.route(\'/updatenotes/<nid>\',methods=[\'GET\',\'POST\'])\r\ndef updatenotes(nid):\r\n    if session.get(\'user\'):\r\n        cursor=mysql.connection.cursor()\r\n        cursor.execute(\'select title,content from diary where nid=%s\',[nid])\r\n        data=cursor.fetchone()\r\n        cursor.close()\r\n        if request.method==\'POST\':\r\n            title=request.form[\'title\']\r\n            content=request.form[\'content\']\r\n            cursor=mysql.connection.cursor()\r\n            cursor.execute(\'update diary set title=%s,content=%s where nid=%s\',[title,content,nid])\r\n            mysql.connection.commit()\r\n            cursor.close()\r\n            flash(\'Diary updated successfully\')\r\n            return redirect(url_for(\'notehome\'))\r\n        return render_template(\'updatenote.html\',data=data)\r\n    else:\r\n        return redirect(url_for(\'login\'))\r\n@app.route(\'/deteletnotes/<nid>\')\r\ndef deletenotes(nid):\r\n    cursor=mysql.connection.cursor()\r\n    cursor.execute(\'delete from diary where nid=%s\',[nid])\r\n    mysql.connection.commit()\r\n    cursor.close()\r\n    flash(\'notes deleted successfully\')\r\n    return redirect(url_for(\'notehome\'))\r\n\r\n@app.route(\'/forget\',methods=[\'GET\',\'POST\'])\r\ndef forgot():\r\n    if request.method==\'POST\':\r\n        email=request.form[\'id\']\r\n        cursor=mysql.connection.cursor()\r\n        cursor.execute(\'select count(*) from students where email=%s\',[email])\r\n        count=cursor.fetchone()[0]\r\n        cursor.close()\r\n        if count==1:\r\n            \r\n            subject=\'Forget Password\'\r\n            confirm_link=url_for(\'reset\',token=token(email,salt=salt2),_external=True)\r\n            body=f\"Use this link to reset your password-\\n\\n{confirm_link}\"\r\n            sendmail(to=email,body=body,subject=subject)\r\n            flash(\'Reset link sent check your email\')\r\n            return redirect(url_for(\'login\'))\r\n        else:\r\n            flash(\'Invalid email id\')\r\n            return render_template(\'forgot.html\')\r\n    return render_template(\'forgot.html\')\r\n@app.route(\'/reset/<token>\',methods=[\'GET\',\'POST\'])\r\ndef reset(token):\r\n    try:\r\n        serializer=URLSafeTimedSerializer(secret_key)\r\n        email=serializer.loads(token,salt=salt2,max_age=180)\r\n    except:\r\n        abort(404,\'Link Expired\')\r\n    else:\r\n        if request.method==\'POST\':\r\n            newpassword=request.form[\'npassword\']\r\n            confirmpassword=request.form[\'cpassword\']\r\n            if newpassword==confirmpassword:\r\n                cursor=mysql.connection.cursor()\r\n                cursor.execute(\'update students set password=%s where email=%s\',[newpassword,email])\r\n                mysql.connection.commit()\r\n                flash(\'Reset Successful\')\r\n                return redirect(url_for(\'login\'))\r\n            else:\r\n                flash(\'Passwords mismatched\')\r\n                return render_template(\'newpassword.html\')\r\n        return render_template(\'newpassword.html\')\r\n\r\n    \r\n\r\napp.run(use_reloader=True,debug=True)\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n','approved','2023-07-04 18:34:33','50','python');
/*!40000 ALTER TABLE `assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendence`
--

DROP TABLE IF EXISTS `attendence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendence` (
  `student_id` int NOT NULL,
  `attendence_date` date NOT NULL,
  `checkin` time DEFAULT NULL,
  `checkout` time DEFAULT NULL,
  `attendencepercentage` decimal(5,2) DEFAULT NULL,
  `total_days` int DEFAULT NULL,
  `groupname` varchar(20) NOT NULL,
  PRIMARY KEY (`student_id`,`attendence_date`,`groupname`),
  KEY `groupname` (`groupname`),
  CONSTRAINT `attendence_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`rollno`),
  CONSTRAINT `attendence_ibfk_2` FOREIGN KEY (`groupname`) REFERENCES `grouptable` (`groupname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendence`
--

LOCK TABLES `attendence` WRITE;
/*!40000 ALTER TABLE `attendence` DISABLE KEYS */;
INSERT INTO `attendence` VALUES (8,'2023-07-03','20:03:00','21:22:00',1.00,100,'python'),(123,'2023-07-04','17:22:00','22:25:00',1.02,100,'python'),(203901,'2023-07-04','12:19:00','13:19:00',1.00,100,'C'),(203907,'2023-07-03','20:37:00','00:00:00',3.00,100,'DBMS'),(203907,'2023-07-04','10:33:00','00:00:00',3.00,100,'python'),(203907,'2023-07-05','16:29:00','00:00:00',3.00,100,'DBMS');
/*!40000 ALTER TABLE `attendence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contactus`
--

DROP TABLE IF EXISTS `contactus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contactus` (
  `branch` varchar(50) DEFAULT NULL,
  `rollno` varchar(9) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `message` tinytext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactus`
--

LOCK TABLES `contactus` WRITE;
/*!40000 ALTER TABLE `contactus` DISABLE KEYS */;
INSERT INTO `contactus` VALUES ('BCA','2','test@example.com','my email is wrong'),('mca','987','nagalakshmijarugulla2003@gmail.com','I want to join with ur organisation');
/*!40000 ALTER TABLE `contactus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grouptable`
--

DROP TABLE IF EXISTS `grouptable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grouptable` (
  `groupname` varchar(20) NOT NULL,
  `added_by` varchar(9) DEFAULT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`groupname`),
  KEY `added_by` (`added_by`),
  CONSTRAINT `grouptable_ibfk_1` FOREIGN KEY (`added_by`) REFERENCES `admin` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grouptable`
--

LOCK TABLES `grouptable` WRITE;
/*!40000 ALTER TABLE `grouptable` DISABLE KEYS */;
INSERT INTO `grouptable` VALUES ('C','123456789','2023-07-04 06:47:25'),('DBMS','23','2023-07-03 14:06:08'),('java','123456789','2023-07-03 12:20:40'),('mern-stack','123456789','2023-07-04 12:44:59'),('python','123456789','2023-07-03 12:18:22');
/*!40000 ALTER TABLE `grouptable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student_group`
--

DROP TABLE IF EXISTS `student_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_group` (
  `studentid` int NOT NULL,
  `groupname` varchar(20) NOT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`studentid`,`groupname`),
  KEY `groupname` (`groupname`),
  CONSTRAINT `student_group_ibfk_1` FOREIGN KEY (`studentid`) REFERENCES `students` (`rollno`),
  CONSTRAINT `student_group_ibfk_2` FOREIGN KEY (`groupname`) REFERENCES `grouptable` (`groupname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_group`
--

LOCK TABLES `student_group` WRITE;
/*!40000 ALTER TABLE `student_group` DISABLE KEYS */;
INSERT INTO `student_group` VALUES (8,'C','2023-07-04 12:18:49'),(8,'java','2023-07-03 12:20:42'),(8,'python','2023-07-04 12:19:21'),(123,'java','2023-07-04 12:23:35'),(123,'mern-stack','2023-07-04 12:45:13'),(123,'python','2023-07-04 11:49:13'),(203901,'C','2023-07-04 06:47:31'),(203901,'python','2023-07-04 12:22:02'),(203907,'DBMS','2023-07-03 14:06:14'),(203907,'python','2023-07-03 12:18:28');
/*!40000 ALTER TABLE `student_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `rollno` int NOT NULL,
  `s_firstname` varchar(30) DEFAULT NULL,
  `s_lastname` varchar(40) DEFAULT NULL,
  `phnumber` bigint DEFAULT NULL,
  `father_name` varchar(50) DEFAULT NULL,
  `mothername` varchar(40) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `branch` enum('BCA','BSC','MPCS','MSCS','BBA') DEFAULT NULL,
  `stu_year` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`rollno`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (8,'ramya','veena',5667897744,'venu','vedavi','girijajarugulla420@gmail.com','BBA','2017-2020'),(123,'rama','kondhanda',8799544090,'nanna','amma','nagalakshmi2003@gmail.com','BCA','2020-2023'),(987,'rama','kondhanda',8799544090,'father','mother','nagalakshmijarugulla2003@gmail.com','BSC','2020-2023'),(203901,'ameena','bibi',1122334488,'ameena father','ameena mother','ameena@gmail.com','BCA','2020-2023'),(203907,'nagalakshmi','jarugulla',8639728809,'shyam','padhmavathi','v@codegnan.com','BCA','2020-2023');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students_register`
--

DROP TABLE IF EXISTS `students_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_register` (
  `rollno` varchar(9) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `branch` enum('BCA','BSC','MPCS','MSCS','BBA') DEFAULT NULL,
  PRIMARY KEY (`rollno`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students_register`
--

LOCK TABLES `students_register` WRITE;
/*!40000 ALTER TABLE `students_register` DISABLE KEYS */;
INSERT INTO `students_register` VALUES ('123','rama','gracekumari625@gmail.com','rama@123','BCA'),('203907','j.nagalakshmi','nagalakshmijarugulla2003@gmail.com','hello','BCA');
/*!40000 ALTER TABLE `students_register` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-05 19:47:30
