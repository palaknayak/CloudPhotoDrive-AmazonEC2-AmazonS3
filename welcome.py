#reference: http://boto3.readthedocs.io/en/latest/guide/s3.html#uploads , http://www.slsmk.com/using-python-boto3-with-amazon-aws-s3-buckets/
import os
import boto3
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)


access_key = 'AKIAICSMVZYTW2JCYCJA'
secret_key = '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'

s3 = boto3.client('s3')
#s3 = boto3.resource('s3')
my_bucket = 'palakclouda3'

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
	response = " "
	f = request.files['file']
	file_name = f.filename
    	s3.upload_fileobj(f, my_bucket, file_name,ExtraArgs={'ContentType': 'image/jpeg'})
	response = response+"<h1>File has been uploaded on S3.</h1><form action='../'><input type='Submit' value='Back to Home Page'></form>"
	return response
		
	
	
@app.route('/download', methods=['POST'])
def download():
	file_name = request.form['filename']
	response = s3.get_object(Bucket=my_bucket,Key=file_name)
	contents = response['Body'].read()
	response = make_response(contents)
        response.headers["Content-Disposition"] = "attachment; filename=%s"%file_name
	return response

@app.route('/list_files', methods=['POST'])
def list():
	response = " "
	#for bucket in s3.buckets.all():
	response = "<h1> List of images on Amazon S3: </h1>"
	theobjects = s3.list_objects_v2(Bucket=my_bucket)
    	for object in theobjects["Contents"]:
        	print(object["Key"])
		response = response + object["Key"] + "</br>"
	response = response + "</br><form action='../'><input type='Submit' value='Back to Home Page'></form>"
	return response
		

@app.route('/delete', methods=['POST'])
def delete():
	file_name = request.form['filename']
	s3.delete_object(Bucket=my_bucket,Key=file_name)
	response = "<h1>File has been deleted from S3.</h1><form action='../'><input type='Submit' value='Back to Home Page'></form>"
	return response

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(debug='true',host='0.0.0.0', port=int(port))
