from flask import Flask,g,request,json,render_template,jsonify
from Services.service import Service
from flask_cors import CORS,cross_origin

app = Flask(__name__, static_url_path='/static') #in order to access any images
app.config.from_object(__name__)

# Below is to enable requests from other domains i.e, enable React to access these APIs
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# app = Flask(__name__)
# app.config.from_object(__name__)
@app.route("/login", methods=['POST'])
@cross_origin()
def check():

	data = request.json
	try:
		response = Service.login(data['email'], data['password'])
		if (response):
			return jsonify(response), 200
		else:
			return jsonify({'Error': response}), 500
	except Exception as e:
		return jsonify(e), 500

@app.route("/register", methods=['POST'])
@cross_origin()
def register():
	try:
		data = request.json
		response = Service.register(app, data)

		if( response == True):
			return jsonify({'data': data}), 200
		else:
			return jsonify({'Error':response}), 500
	except Exception as e:
		return jsonify(e), 500

@app.route("/activate/<email>", methods=['GET'])
@cross_origin()
def activate_user(email):
	try:
		response = Service.activate_user(email)
		if(response == True):
			return jsonify({'data': 'Your account is activated'}), 200
		else:
			return jsonify({'Error': "response"}), 500
	except Exception as e:
		return jsonify(e), 500


@app.route("/securityQuestion/<email>", methods=['GET'])
@cross_origin()
def security_question(email):
	try:
		response = Service.security_question(email)
		if(response):
			return jsonify({'question': response}), 200
		else:
			return jsonify({'Error':"response"}), 500	
	except Exception as e:
		return jsonify(e), 500

"""
Verifies user's answer and actual security answer in DB
"""

@app.route("/securityAnswer", methods=['POST'])
@cross_origin()
def verify_security_answer():
	try:
		data = request.json
		response = Service.verify_security_answer(data['answer'],data['email'])
		return jsonify({'wasAnswerCorrect': response}), 200
	except Exception as e:
		return jsonify(e), 500


"""
Sets a new password for particular user, provided email and new password
"""

@app.route("/updatePassword", methods=['POST'])
@cross_origin()
def update_password():
	try:
		data = request.json
		response = Service.update_password(data['password'],data['email'])
		return jsonify({'wasUpdateSuccessful': response}), 200
	except Exception as e:
		return jsonify(e), 500



if __name__ == '__main__':
    #app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
