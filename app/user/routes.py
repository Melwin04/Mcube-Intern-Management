from . import userBp
from flask import request, jsonify
from models import User

@userBp.get('/getAllNames')
def getUsers():
    
    try: 
        users = User.objects()

        userData = [{
                "id": user.id,
                "text": user.name
        }
        for user in users
        ]

        return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": userData})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {e}"})