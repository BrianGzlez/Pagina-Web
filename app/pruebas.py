import smtplib, ssl 
from os import environ
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import choice 

secret_key = environ["Contraseña_Gmail"]
gmail = environ["gmail"]


def Enviar_Mensaje_Bienvenida():   

 conexion = smtplib.SMTP( "smtp.gmail.com", port= 587)
 conexion.ehlo()
 conexion.starttls()    #Encriptación TLS
 conexion.login(gmail,secret_key)     #Inciar sesión en el servidor STMP 

 destinario = "mejm3571@gmail.com"

 mensaje = MIMEMultipart("alternative")
 mensaje["Subject"] = "Welcome to Bortex Community"
 mensaje["From"] = "bortexcompany@gmail.com"
 mensaje["To"] = destinario

 string_v = """
 
 
 """

 html = f""" 
 <html>
 <body>
  <b>Hi {destinario}, welcome to Bortex Community!</b>

  <p>Congratulations , you’ve just joined a community of experience innovators who want to make their customers happier and their organizations stronger! </p>

  <p>Here are a few resources that will quickly help you to start using <b>Bortex</b> efficiently. Hang onto this email and fall back to it whenever you need guidance.</p>

  
  <p>We are a company committed to your safety, feel free to write to us at <b> bortexcompany@gmail.com </b> if you have any questions.</p>

 </body>
 </html>

 """
 parte_html = MIMEText(html, "html")
 mensaje.attach(parte_html)
 conexion.sendmail(gmail,"mejm3571@gmail.com",mensaje.as_string())
 conexion.quit()
 print("Su contraseña se ha enviado correctamente!")






def Intento_De_VolarSistema():
    Password = ""
    longitud = 8 
    valores = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAMNBVCXZ!/&%$#"
    Contraseña_Random = ""
    Contraseña_Random = Contraseña_Random.join([choice(valores)for i in range(longitud)])
    
    
    conexion = smtplib.SMTP( "smtp.gmail.com", port= 587)
    conexion.ehlo()
    conexion.starttls()    #Encriptación TLS
    conexion.login(gmail,secret_key)     #Inciar sesión en el servidor STMP 

    destinario = "brianarielgonzalez21@gmail.com"

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = "Welcome to Bortex Community"
    mensaje["From"] = "bortexcompany@gmail.com"
    mensaje["To"] = destinario

    html = f""" 
 <html>
 <body>
  <b>Hi {destinario}, your security has tried to be lowered!</b>

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
    print("Su contraseña se ha enviado correctamente!")



def Recuperar_contraseña():
 conexion = smtplib.SMTP( "smtp.gmail.com", port= 587)
 conexion.ehlo()
 conexion.starttls()    #Encriptación TLS
 conexion.login(gmail,secret_key)     #Inciar sesión en el servidor STMP 

 destinario = "mejm3571@gmail.com"
 password = "na,acriar'otro"
 mensaje = MIMEMultipart("alternative")
 mensaje["Subject"] = "Welcome to Bortex Community"
 mensaje["From"] = "bortexcompany@gmail.com"
 mensaje["To"] = destinario


 
 


 html = f""" 
 <html>
 <body>
  <b>Hi {destinario}, we just received your password recovery notification!</b>

  <p> Your password is <b>{password}</b> , in case you want to change it, <b><a href= "">click here</a></b> </p>

  

 </body>
 </html>

 """
 parte_html = MIMEText(html, "html")
 mensaje.attach(parte_html)
 conexion.sendmail(gmail,"mejm3571@gmail.com",mensaje.as_string())
 conexion.quit()
 print("Su contraseña se ha enviado correctamente!")  

Recuperar_contraseña()

