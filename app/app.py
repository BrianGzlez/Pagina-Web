from enum import unique
from unicodedata import category
from flask import Flask, render_template, request, Response, flash , send_file
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
import datetime 
import cv2
import smtplib, ssl 
import os 
from matplotlib import pyplot as plt
from os import environ
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import choice 
import time 



app = Flask(__name__)

secret_key = "123456"

app = Flask(__name__)

app.config['SECRET_KEY'] = secret_key


##CONNECT TO DB
try:
    URI = {}["Se_me_olvido"]
    if (URI.startswith("postgres")):
        URI = f"postgresql{URI.split('postgres')[1]}"
    app.config["SQLALCHEMY_DATABASE_URI"] = URI
except KeyError:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50), unique= True)
    email = db.Column(db.String(40))
    password = db.Column(db.String(66))
    created_date = db.Column(db.DateTime, default = datetime.datetime.now)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

#db.create_all()

## CAMERA
camera = cv2.VideoCapture(0)  

def gen_frames():  
    while True:
      
        success, frame = camera.read()  
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



secret_key = environ["Contraseña_Gmail"]
gmail = environ["gmail"]

def face(img, faces):
    data = plt.imread(img)
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]
        x2, y2 = x1 + ancho, y1 + alto
        plt.subplot(1,len(faces), i + 1)
        plt.axis("off")
        face = cv2.resize(data[y1:y2, x1:x2],(150,200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, face)
        plt.imshow(data[y1:y2, x1:x2])

def register_capture(username):

    cap = cv2.VideoCapture(0)
    user_reg_img = username 
    img = f"{user_reg_img}.jpg"

    while True:
        ret, frame = cap.read()
        cv2.imshow("Registro Facial", frame)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()
    
    pixels = plt.imread(img)
   
    face(img)

def compatibility(img1, img2):
    orb = cv2.ORB_create()

    kpa, dac1 = orb.detectAndCompute(img1, None)
    kpa, dac2 = orb.detectAndCompute(img2, None)

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = comp.match(dac1, dac2)

    similar = [x for x in matches if x.distance < 70]
    if len(matches) == 0:
        return 0
    return len(similar)/len(matches)

def login_capture(username):
    cap = cv2.VideoCapture(0)
    user_login = username
    img = f"{user_login}_login.jpg"
    img_user = f"{user_login}.jpg"

    while True:
        ret, frame = cap.read()
        cv2.imshow("Login Facial", frame)
        if cv2.waitKey(1) == 27:
            break
    
    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

   
    
    pixels = plt.imread(img)
   

    face(img)
    res_db = db.getUser(user_login, img_user)
    if(res_db["affected"]):
        my_files = os.listdir()
        if img_user in my_files:
            face_reg = cv2.imread(img_user, 0)
            face_log = cv2.imread(img, 0)

            comp = compatibility(face_reg, face_log)
            
            if comp >= 0.94:
                print("{}Compatibilidad del {:.1%}{}".format(float(comp)))
                print( f"Bienvenido, {user_login}", 1)
            else:
                print("{}Compatibilidad del {:.1%}{}".format(float(comp)))
                print( "¡Error! Incopatibilidad de datos", 0)
            os.remove(img_user)

def Enviar_Mensaje_Bienvenida(username,email):   

 conexion = smtplib.SMTP( "smtp.gmail.com", port= 587)
 conexion.ehlo()
 conexion.starttls()    #Encriptación TLS
 conexion.login(gmail,secret_key)     #Inciar sesión en el servidor STMP 

 

 mensaje = MIMEMultipart("alternative")
 mensaje["Subject"] = "Welcome to Bortex Community"
 mensaje["From"] = "bortexcompany@gmail.com"
 mensaje["To"] = email

 

 html = f""" 
 <html>
 <body>
  <b>Hi {username}, welcome to Bortex Community!</b>

  <p>Congratulations , you’ve just joined a community of experience innovators who want to make their customers happier and their organizations stronger! </p>

  <p>Here are a few resources that will quickly help you to start using <b>Bortex</b> efficiently. Hang onto this email and fall back to it whenever you need guidance.</p>

  
  <p>We are a company committed to your safety, feel free to write to us at <b> bortexcompany@gmail.com </b> if you have any questions.</p>

 </body>
 </html>

 """
 parte_html = MIMEText(html, "html")
 mensaje.attach(parte_html)
 conexion.sendmail(gmail,email,mensaje.as_string())
 conexion.quit()
 print("Su contraseña se ha enviado correctamente!")

def Intento_De_VolarSistema(email, username):

    
    Password = ""
    longitud = 8 
    valores = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAMNBVCXZ!/&%$#"
    Contraseña_Random = ""
    Contraseña_Random = Contraseña_Random.join([choice(valores)for i in range(longitud)])
    
    
    conexion = smtplib.SMTP( "smtp.gmail.com", port= 587)
    conexion.ehlo()
    conexion.starttls()    #Encriptación TLS
    conexion.login(gmail,secret_key)     #Inciar sesión en el servidor STMP 

    

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Security flaw"
    mensaje["From"] = "bortexcompany@gmail.com"
    mensaje["To"] = email

    html = f""" 
 <html>
 <body>
  <b>Hi {username}, your security has tried to be lowered!</b>

  <p>At Bortex we take the safety of our members very seriously, which is why we have taken a series of measures so that it does not happen again. </p>

  <p>We have changed your primary security password, which is <b>{Contraseña_Random}</>. In the event of another security breach attempt, we will be forced to implement other measures.</p>

  
  <p> <b>Bortex, committed to safety</b></p>

 </body>
 </html>

 """
    parte_html = MIMEText(html, "html")
    mensaje.attach(parte_html)
    conexion.sendmail(gmail,"brianarielgonzalez21@gmail.com",mensaje.as_string())
    conexion.quit()
    print("Correo enviado!")

def Recuperar_contraseña(email, password, username):
 conexion = smtplib.SMTP( "smtp.gmail.com", port= 587)
 conexion.ehlo()
 conexion.starttls()    #Encriptación TLS
 conexion.login(gmail,secret_key)     #Inciar sesión en el servidor STMP 

 mensaje = MIMEMultipart("alternative")
 mensaje["Subject"] = "Recover password"
 mensaje["From"] = "bortexcompany@gmail.com"
 mensaje["To"] = email

 html = f""" 
 <html>
 <body>
  <b>Hi {username}, we just received your password recovery notification!</b>

  <p> Your password is <b>{password}</b> , in case you want to change it, <b><a href= "">click here</a></b> </p>

  

 </body>
 </html>

 """
 parte_html = MIMEText(html, "html")
 mensaje.attach(parte_html)
 conexion.sendmail(gmail,email,mensaje.as_string())
 conexion.quit()
 print("Su contraseña se ha enviado correctamente!")  




@app.route('/')
def inicio():
    return render_template('index.html') 

@app.route("/Subir Archivo.html", methods = ['GET','POST'])
def subir_archivos():
    if request.method == "POST":
        file = request.files['file']
        
        upload = Upload(filename = file.filename, data= file.read())
        db.session.add(upload)
        db.session.commit()

    return render_template("/Subir Archivo.html")
   
@app.route('/download')
def download(upload_id):
    upload = Upload.query.filter_by(id= upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)

@app.route('/index.html')
def index():
    return render_template('index.html') 
   
@app.route('/code.html')
def code():
    return render_template('code.html')

@app.route('/login.html', methods=["POST", "GET"])
def login():
    if (request.method=="POST"):
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if (user != None):
            if (password == user.password):
                print("Verificado")
                return render_template("/Subir Archivo.html")
            else:
                print("Incorrecta")
                
                Intento_De_VolarSistema(user.email, username)
                return render_template('camera.html')
            


    return render_template('login.html')

@app.route('/recover.html', methods = ['GET', 'POST'] )
def recover():
    if (request.method == "POST"):
        email = request.form["email"]

        user = User.query.filter_by(email = email).first()
        if (email != None):
            if email == user.email:
              print("email encontrado")
              Recuperar_contraseña(user.email, user.password, user.username)
          
            else:
                print("No fue encontrado su email")
               


           
    return render_template('recover.html')
    

@app.route('/singup.html', methods=['POST', 'GET'])
def singup():
    if (request.method=="POST"):
        # Get data
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmation_password = request.form["password_confirmation"]

        if len(email) < 4:
            flash('Email must  be greater than 3 characters.' , category= "error")
        elif len(username) < 3:
            flash('Your username must be greater than 2 characters.', category= "error")
        elif len(password) < 7 :
            flash('Your password must be greater than 6 characters', category= "error")
        else:

          if (User.query.filter_by(email=email).first() == None and confirmation_password==password):
            # Create user
              Enviar_Mensaje_Bienvenida(username,email)
              user = User(username=username, email=email, password=password)

            # Add new user
              db.session.add(user)
              db.session.commit()
              flash('Usuario Registrado', category='success')  
              return render_template('/login.html') 

              
              
        
    return render_template('/singup.html')


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')





if __name__ == "__main__":
    app.run(debug = True, port = 5000)