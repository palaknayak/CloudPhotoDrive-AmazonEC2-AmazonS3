#reference: http://ishwortimilsina.com/upload-file-cloudant-nosql-db-using-python-flask

import os
from flask import Flask, jsonify, request, make_response
from cloudant import Cloudant
import hashlib
import datetime

app = Flask(__name__)
USERNAME = "e92c4fcd-5b2d-4adf-a1a6-4c2b9ff6b17b-bluemix"
PASSWORD = "718054e80b9553e037d9635ab2d505634ceb967d75ec70d3dde712b7ca3b57e4"
URL = "https://e92c4fcd-5b2d-4adf-a1a6-4c2b9ff6b17b-bluemix:718054e80b9553e037d9635ab2d505634ceb967d75ec70d3dde712b7ca3b57e4@e92c4fcd-5b2d-4adf-a1a6-4c2b9ff6b17b-bluemix.cloudant.com"

client = Cloudant(USERNAME, PASSWORD, url=URL)
# Connect to the account
client.connect()
my_database = client['palakcloudantpythonflask']


@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
	response = " "
	#receive the file uploaded from upload form of index.html
	filename = request.files['file']
	file_name = filename.filename
	file_content = filename.read()
	hash_object = hashlib.md5(file_content.encode()) #hash a content and use it to comapre to the hash value of files present on cloudant
	file_content_hashed=hash_object.hexdigest()
	flag = False #flag will true if there exist a file with same name on cloudant

	for document in my_database:
		if (document['file_name'] == file_name):  #check if there is a file with same name?
			flag = True
			if(document['hashed_content']==file_content_hashed):  #if yes, the check the content us same?
				response = response+"<h3>The File with the same content is already present</h3><form action='../'><input type='Submit' value='Back to Home Page'></form>"
			else:
				version = document['version']+1
				timestamp = str(datetime.datetime.now())
				data1 = {'file_name': file_name,'data': file_content,'hashed_content':file_content_hashed, 'version':version, 'timestamp':timestamp}
				doc = my_database.create_document(data1)
				response = response+"<h1>File has been uploaded on Cloudant.</h1><form action='../'><input type='Submit' value='Back to Home Page'></form>"
	if flag==False: #if flag is flase, there is no file wih same name. Store a new file on cloudant with version=1
		timestamp = str(datetime.datetime.now())
		data1 = {'file_name': file_name,'data': file_content,'hashed_content':file_content_hashed,'version':1,'timestamp':timestamp}
		doc = my_database.create_document(data1)
		response = response+"<h1>File has been uploaded on Cloudant.</h1><form action='../'><input type='Submit' value='Back to Home Page'></form>"
	return response
		
	
	
@app.route('/download', methods=['POST'])
def download():
	file_name = request.form['filename']
	file_version = request.form['fileversion']
	for document in my_database:
		if (document['file_name'] == file_name and document['version'] == int(file_version)):
			dt = document['data']
			f= open(file_name,"w+")
			f.write(dt)  #file will be downloaded in the current local directory
			response = "<h3>The requested file has been downloaded</h3><form action='../'><input type='Submit' value='Back to Home Page'></form>"
		else:
			response = "<h3>File not Found</h3><form action='../'><input type='Submit' value='Back to Home Page'></form>"
	return response

@app.route('/list_files', methods=['POST'])
def list():
	file_list="<html><body><h1>The Files on Cloudants are:</h1><h4>"
	for document in my_database:
		file_list=file_list+"File Name: "+document['file_name']+" "+"Version: "+str(document['version'])+" "+"Last Updated: "+document['timestamp']+"</br>"
	file_list=file_list+"</h4><form action='../'><input type='Submit' value='Back to Home Page'></form></body></html>"
	return file_list
		

@app.route('/delete', methods=['POST'])
def delete():
	file_name = request.form['filename']
	file_version = request.form['fileversion']
	print '------------------>>>>>>>>>>>>>>>>'
	print file_version
	for document in my_database:
		if (document['file_name'] == file_name and document['version'] == int(file_version)):
			print("File found and deleted")
			document.delete()
			#document.delete_attachment(file_name)
		else:
			print ('File not found')
	return "<h1>File has been deleted</h1><form action='../'><input type='Submit' value='Back to Home Page'></form>"

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
