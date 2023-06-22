from flask import Flask, session,redirect,url_for
from flask import render_template,request
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import pathlib
import qrcode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import cv2
import ipfsapi
api = ipfsapi.Client(host='127.0.0.1', port=5001)

app = Flask(__name__)
 
app.config['UPLOADED_PHOTOS_DEST'] = 'static/files/'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

foldername='static/files/'

app.secret_key = 'any random string'

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/main')
def main():
    return render_template('index1.html') 

@app.route('/main2')
def main2():
    return render_template('displayforuser.html') 

@app.route('/main3')
def main3():
    return render_template('displayfordis.html') 

@app.route('/main1')
def main1():
    return render_template('index2.html') 

@app.route('/displayInfo')
def displayInfo():
    return render_template('displayInfo.html') 

@app.route('/logout')
def logout():
    session.pop('name',None)
    return render_template('index.html') 

@app.route('/userregister')
def userregister():
    return render_template('userregister.html') 

@app.route('/userlogin')
def userlogin():
    return render_template('userlogin.html') 

@app.route('/SessionHandle',methods=['POST','GET'])
def SessionHandle():
    if request.method == "POST":
        details = request.form
        name = details['name']
        password = details['pass']
        session['name'] = name        
        session['pass'] = password
        strofuser = name
        print (strofuser.encode('utf8', 'ignore'))
        return strofuser 
    
@app.route('/SessionHandle2',methods=['POST','GET'])
def SessionHandle2():
    if request.method == "POST":
        details = request.form
        name = details['name']
        password = details['pass']
        session['name'] = name        
        session['pass'] = password
        strofuser = name
        print (strofuser.encode('utf8', 'ignore'))
        return strofuser 
    
@app.route('/SessionHandle1',methods=['POST','GET'])
def SessionHandle1():
    if request.method == "POST":
        details = request.form
        username = details['username']
        password = details['password']
        
        if username == 'admin' and password == 'admin':            
            session['admin'] = username
            strofuser = username
            print (strofuser.encode('utf8', 'ignore'))
            return redirect(url_for('main1'))
        else:
            return redirect(url_for('adminlogin'))
    
    return redirect(url_for('adminlogin'))

@app.route('/distributorregister')
def distributorregister():
    return render_template('distributorregister.html') 

@app.route('/distributorlogin')
def distributorlogin():
    return render_template('distributorlogin.html') 

@app.route('/SessionHandle3',methods=['POST','GET'])
def SessionHandle3():
    if request.method == "POST":
        details = request.form
        name = details['name']
        password = details['pass']
        session['distributor'] = name  
        strofuser = name
        print (strofuser.encode('utf8', 'ignore'))
        return strofuser 

@app.route('/uploadProduct',methods=['POST','GET'])
def uploadProduct():
    if request.method == "POST":
        
        f2= request.files['filename'] 
        idofproduct = request.form['pid'] 
        name = request.form['pname'] 
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        Price = request.form['pprice'] 
        
        user = session.get("name")
        passwww = session.get("pass")
        
        filename_secure = secure_filename(f2.filename)
        pathlib.Path(app.config['UPLOADED_PHOTOS_DEST'], user).mkdir(exist_ok=True)
        f2.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'],user, filename_secure))     
        
        filename55 = filename_secure
        
        ListOfFile = {'a':filename55,'b':idofproduct,'c':name,
                      'd':category,'e':Price,'f':user,'g':passwww,'h':quantity}
        return ListOfFile 
    return render_template('uploadProduct.html',data={})

@app.route('/displayProduct',methods=['POST','GET'])
def displayProduct():
    if request.method == "POST":
        details = request.form
        fname = details['fname']
        data=fname.split('|')
        return render_template('displayProduct.html',data=data) 
    return render_template('displayProduct.html')

@app.route('/generateqrcode',methods=['POST','GET'])
def generateqrcode():
    if request.method == "POST":
        details = request.form
        username = details['username']
        imagename = details['imagename']
        idofp = details['idofp']
        pname = details['pname']
        pcat = details['pcat']
        pprice = details['pprice']        
        
        new_file1 = api.add("static/files/"+username+"/"+imagename)
        print(new_file1['Hash'])
        
        data = username+"|"+new_file1['Hash']+"|"+idofp+"|"+pname+"|"+pcat+"|"+pprice
        
        key = RSA.generate(2048)        
        
        pathlib.Path('static/keys/', username).mkdir(exist_ok=True)
        with open('static/keys/'+username+"/"+imagename.split('.', 1)[0]+'_private.pem', 'wb' ) as f:
            f.write( key.exportKey( 'PEM' ))        
        
        publicKey = PKCS1_OAEP.new( key )
        secret_message = bytes(data, 'utf-8')
        
        encMessage = publicKey.encrypt( secret_message ) 
        hexilify= binascii.hexlify(encMessage)
        strencry = str(hexilify.decode('UTF-8')) 
        
        pathlib.Path('static/txtdata/', username).mkdir(exist_ok=True)
        with open('static/txtdata/'+username+"/"+imagename.split('.', 1)[0]+'_encdata.txt', 'w') as f:
            f.write(strencry)
        
        dataofqr = 'static/txtdata/'+username+"/"+imagename.split('.', 1)[0]+'_encdata.txt'+","+'static/keys/'+username+"/"+imagename.split('.', 1)[0]+'_private.pem'
        img = qrcode.make(dataofqr)
        img.save('static/qrcode/'+imagename.split('.', 1)[0]+'_QR.png') 
        
        ListOfFile = {'a':idofp,'b':pname,'c':pcat,'d':pprice,'e':'static/qrcode/'+imagename.split('.', 1)[0]+'_QR.png'}
        return ListOfFile 
    return render_template('displayProduct.html')

@app.route('/getAllInfoOfImage',methods=['POST','GET'])
def getAllInfoOfImage():
    if request.method == "POST":   
        
        details = request.form
        data = details['data']
        parts = data.split("|")
        print ("dsdasdsadsadsad",parts)
        return render_template('qrcode.html',data=parts) 
    
@app.route('/getAllInfoOfImage1',methods=['POST','GET'])
def getAllInfoOfImage1():
    if request.method == "POST":   
        
        details = request.form
        data = details['data']
        parts = data.split("|")
        print ("------------------------------------------")
        print (parts)
        print ("------------------------------------------")
        return render_template('qrcode1.html',data=parts) 
    
    
@app.route('/buyProductDistributor',methods=['POST','GET'])
def buyProductDistributor():
    if request.method == "POST":
        details = request.form
        qrpath = details['qrpath']
        
        img=cv2.imread(qrpath)
        det=cv2.QRCodeDetector()
        val, pts, st_code=det.detectAndDecode(img)
        print(val)
        
        parts = val.split(",")
        print(parts)
        
        with open(parts[1],'r' ) as f:
            key = RSA.importKey( f.read() )
            
        fileObject = open(parts[0], "r")
        encdata = fileObject.read()
        print(encdata)
        
        convertedtobyte = bytes(encdata, 'utf-8')
        public_crypter =  PKCS1_OAEP.new( key )
        decrypted_data = public_crypter.decrypt(binascii.unhexlify(convertedtobyte))
        str1 = decrypted_data.decode('UTF-8') 
        print(type(str1))
        parts2 = str1.split("|")
        print(parts2) 
        
        username = session.get("distributor")
        
        data = username+"|"+parts2[1]+"|"+parts2[2]+"|"+parts2[3]+"|"+parts2[4]+"|"+parts2[5]
        
        key = RSA.generate(2048)        
        
        with open(parts[1], 'wb' ) as f:
            f.write( key.exportKey( 'PEM' ))        
        
        publicKey = PKCS1_OAEP.new( key )
        secret_message = bytes(data, 'utf-8')       
        encMessage = publicKey.encrypt( secret_message ) 
        hexilify= binascii.hexlify(encMessage)
        strencry = str(hexilify.decode('UTF-8'))       
        encfilename=parts[0]
        with open(encfilename, 'w') as f:
            f.write(strencry)      
        print ("------------------------------------------")
        print (qrpath)
        print (parts)
        print (data)
        print (encfilename)
        print ("------------------------------------------")
        
        dataofqr = encfilename+","+parts[1]
        img = qrcode.make(dataofqr)
        img.save(qrpath) 
        
        return "Ownership changed"        
    
@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        print("GET")
        src = request.form.get("src")  
        try:
            parts = src.split(",")
            print(parts)
            with open(parts[1],'r' ) as f:
                key = RSA.importKey( f.read() )
            fileObject = open(parts[0], "r")
            encdata = fileObject.read()
            print(encdata)   
            convertedtobyte = bytes(encdata, 'utf-8')
            public_crypter =  PKCS1_OAEP.new( key )
            decrypted_data = public_crypter.decrypt(binascii.unhexlify(convertedtobyte))
            str1 = decrypted_data.decode('UTF-8') 
            print(type(str1))
            parts2 = str1.split("|")
            print(parts2) 
            import urllib3
            url = 'http://127.0.0.1:8307/ipfs/'+parts2[1]
            connection_pool = urllib3.PoolManager()
            resp = connection_pool.request('GET',url )
            f = open("static/ipfs/"+parts2[1]+".jpg", 'wb')
            f.write(resp.data)
            f.close()
            resp.release_conn()
            return str1
        except:
            return "fail"
if __name__ == "__main__":
    app.run("0.0.0.0")
    
