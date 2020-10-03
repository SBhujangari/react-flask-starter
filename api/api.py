import time
import os
from flask import Flask, request, flash, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from inference import predict

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config["SECRET_KEY"] = "secretkey"
app.config["UPLOADED_IMAGES_DEST"] = "uploads/images"
app.config["MAX_CONTENT_LENGTH"] = 0.5 * 1024 * 1024

filePath = 'dummy'
#get method via just route
@app.route('/time')
def get_current_time():
	return {'time': time.time()} 

#Example using url params
@app.route('/test', methods=['POST'])
def test():
	json = request.get_json()
	return {'lang': json['language']} 


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

#Example using url params for file
@app.route("/upload", methods=["POST"])
def upload_image():
    global filePath
    print('File Path', filePath)
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("Select An Image")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("Image successfully uploaded and displayed")
        filePath = 'static/uploads/' + filename
        print('File Path', filePath)
        return {'status': 'success'}
    else:
        flash("We only accept png, jpg, jpeg, gif")
        return redirect(request.url)

@app.route("/display/<filename>")
def display_image(filename):
    filepath = 'static/uploads/' + filename
    global filePath 
    filePath= filepath
    print('File Path inside display', filePath)
    return send_file(filepath)

@app.route("/display/defaults/<filename>")
def display_default_image(filename):
    print('Filename', filename)
    filepath = 'static/uploads/defaults/' + filename + '.jpeg'
    global filePath 
    filePath = filepath
    print('File Path inside display defaults', filePath)
    return send_file(filepath)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=5000)

@app.route("/classify")
def classify():
    print('File Path inside classify', filePath)
    x = predict(filePath)
    print("%.2f" % (x[0]*100)+'%', x[1])
    return {'prediction': str("%.2f" % (x[0]*100)+'%'+f' chance of {x[1]}')}
    #return {'prediction': '24alwkejf'}