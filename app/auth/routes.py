from models import User
from . import authBp
from flask import jsonify, request, session

@authBp.post('/register')
def register():
    try:

        data = request.get_json()
        if data.get("name") == "" or data.get("email") == "" or data.get("password") == "":
            return jsonify({"status" : "error", "message" : "All Fields Are Required"}) ,404
        user = User(
            name = data.get("name"),
            email = data.get("email"),
            password = data.get("password"),
            mobileNumber = data.get("mobileNumber")
        )
        user.save()
        return jsonify({"status" : "success", "message" : "User Registered Successfully"}),200
    except Exception as e :
        return jsonify({"status" : "error", "message" : f"Error {e}"}),500
    

@authBp.post('/login')
def login():
    try:
        data = request.get_json()

        if data.get("email") == "" or data.get("password") == "":
            return jsonify({"status" : "error", "message" : "All Fields Are Required"}) ,404        
        
        user = User.objects(email=data.get("email")).first()

        if not user:
            return jsonify({"status" : "error", "message" : "User Not Found."}) ,404 
        
        if user.password != data.get("password"):
            return jsonify({"status" : "error" , "message" : "Password Not Matched"}), 404
        
        session['user'] = {
            "name": user.name,
            "id": user.id,
            "email": user.email
        }
         
        return jsonify({"status" : "success" , "message" : "User Logged In Successfully"}),200
    except Exception as e:
        return jsonify({"status" : "error", "message" : f"Error {e}" }),404