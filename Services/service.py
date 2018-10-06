from Services.pg_config import PgConfig
from Services.email_config import Email
from Services.crypto import Crypto
from Services.jwt import Jwt

class Service:

	@staticmethod
	def register(app, user):
		cur = None
		conn = None
		try:
			conn = PgConfig.db()
			if(conn):
				cur = conn.cursor()
				password = Crypto.encrypted_string(user['password'])

				register_query = "INSERT INTO users(first_name,last_name, email, password, \
				security_question, security_answer, status) VALUES (%s, %s, %s, %s,%s,%s, %s)"
				cur.execute(register_query, (user['firstName'], user['lastName'], \
					user['email'], password, user['securityQuestion'], user['securityAnswer'], 'deactive'));

				#Commenting email part as it was throwing BotoServerError (timezone issue)
				# email = Email(to=user['email'], subject='Welcome to Course 360')
				#
				# ctx = {'username': user['firstName'], 'url':'http://localhost:5000/activate/'+user['email']}
				# email.html('confirmRegistration.html', ctx)
				# email.send()

				conn.commit()
				return True
			else:
				return "Unable to connect"
		except Exception as e:
			return e
		finally:
				cur.close()
				conn.close()

	@staticmethod
	def activate_user(email):
		try:
			conn = PgConfig.db()
			if(conn):
				cur = conn.cursor()
				update_query = "UPDATE users SET status = %s WHERE users.email LIKE %s"
				cur.execute(update_query, ('activate', email));
				conn.commit()
				return True
			else:
				return "Unable to connect"
		except Exception as e:
			return {"Error": e}
		finally:
				cur.close()
				conn.close()

	@staticmethod
	def login(email, password):
		try:
			conn = PgConfig.db()
			if(conn):

				cur = conn.cursor()
				login_query = "SELECT users.password, users.user_id AS password \
				FROM users WHERE users.email LIKE %s"
				cur.execute(login_query, (email, ))
				user = cur.fetchone()
				response = {'token':'', 'email':''}
				if(Crypto.verify_decrypted_string(password, user[0])):
					response['token'] = str(Jwt.encode_auth_token(user_id=user[1]))
					response['email']= email
					return response
					#status = Jwt.decode_auth_token(token)
				else:
					return "Not able to login"
			else:
				return "Invalid Email or Password"

		except Exception as e:
			print(e)
			return {"Error occured": e}

		finally:
				cur.close()
				conn.close()

	@staticmethod
	def security_question(email):
		conn = None
		cur = None
		try:
			conn = PgConfig.db()
			if(conn):
				cur = conn.cursor()

				select_query = "SELECT security_question FROM users WHERE email LIKE %s"
				cur.execute(select_query, (email,))
				question = cur.fetchone()[0]

				if(question):
					return question
				else:
					return "Question not found"
			else:
				return "Unable to connect"
		except Exception as e:
			return e
		finally:
				cur.close()
				conn.close()

	"""
	Checks whether answer input by user is same as that in DB
	for his/her email
	
	Returns True or False 
	"""
	@staticmethod
	def verify_security_answer(answer_given,email):
		conn = None
		cur = None
		try:
			conn = PgConfig.db()
			if(conn):
				cur = conn.cursor()

				select_query = "SELECT security_answer FROM users WHERE email LIKE %s"
				cur.execute(select_query, (email,))
				actual_answer = cur.fetchone()[0]

				if(actual_answer == answer_given):
					return True
				else:
					return False
		except Exception as e:
			return e
		finally:
				cur.close()
				conn.close()

	@staticmethod
	def update_password(password, email):
		conn = None
		cur = None
		try:
			conn = PgConfig.db()
			if(conn):
				cur = conn.cursor()
				query = "UPDATE users SET password = %s WHERE users.email LIKE %s"
				cur.execute(query, (Crypto.encrypted_string(password),email))
				if(cur.rowcount==1):
					conn.commit()
					return True
				else:
					print('Update Failed!!!!! Email not found, maybe???')
					return False

		except Exception as e:
			return e
		finally:
			cur.close()
			conn.close()