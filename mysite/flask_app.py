
# A very simple Flask Hello World app for you to get started with...
import os
from flask import Flask, flash, request, redirect, render_template
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)
upload_folder = '/home/AriChikkere/mysite/images'

#Depends on web server's settings
app.secret_key = "secret key"

app.config['upload_folder'] = upload_folder
accepted_extensions = set(['jpg', 'jpeg', 'png', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in accepted_extensions

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['upload_folder'], filename))
		flash('File(s) successfully uploaded')
		return redirect('/')

if __name__ == "__main__":
    app.run()