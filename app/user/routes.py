from . import userBp
from flask import request, jsonify
from models import User
from datetime import datetime,timedelta
from mongoengine import Q

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


@userBp.get('/get')
def getUserById():
    id = request.args.get("id")
    try: 
        user = User.objects(id=id).first()

        userData = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "mobileNumber": user.mobileNumber,
            "addedTime": user.addedTime,
            "updatedTime": user.updatedTime
        }

        return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": userData})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {e}"})


@userBp.post('/new')
def createUser():
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
        return jsonify({"status" : "success", "message" : "User Added Successfully"}),200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {e}"}), 500


    
@userBp.put('/update')
def updateUser():
    userId = request.args.get("id")
                              
    data = request.get_json()
    try:
        if not userId:
            return jsonify({"status": "error", "message": "User ID not found"}), 404
        
        if data.get("name") == "" or data.get("email") == "" or data.get("password") == "":
            return jsonify({"status" : "error", "message" : "All Fields Are Required"}) ,404

        user = User.objects(id=userId).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        user.name = data["name"]
        user.password = data.get("password")
        user.mobileNumber = data.get("mobileNumber")
        user.updatedTime = datetime.now()
        user.save()

        return jsonify({"status": "success", "message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error occurred: {e}"}), 404
    
@userBp.delete('/delete')
def deleteUser():
    userId = request.args.get("id")
    try:
        if not userId:
            return jsonify({"status": "error", "message": "User ID not found"}), 404

        user = User.objects(id=userId).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        user.delete()
        return jsonify({"status": "success", "message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error : {e}"}), 404
    


    
@userBp.get('/getAll')
def getUser():
     try:
        start = int(request.args.get('start', 0))  
        length = int(request.args.get('length', 10))  
        
        
        search_value = request.args.get('search[value]', '')
        
        
        order_column_index = int(request.args.get('order[0][column]', 0))  
        order_direction = request.args.get('order[0][dir]', 'asc')
        
        columns_map = {
            0: 'name',  
            1: 'email',  
            2: 'password',
            3: 'mobileNumber',
            4: 'addedTime',
            5: 'updatedTime',  
        }
        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_direction == 'desc' else order_column
        
        user_query = User.objects()
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        show_errors = request.args.get('show_errors', 'false').lower() == 'true'

        
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                user_query = user_query.filter(log_time__gte=start_dt, log_time__lt=end_dt)
            except ValueError:
                pass  
        
        if show_errors:
            user_query = user_query.filter(status="error")


            
        
        if search_value:
            user_query = user_query.filter(
                Q(name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(mobileNumber__icontains=search_value)
            )
        
        
        total_user = User.objects().count()
        
        
        filtered_user = user_query.count()
        
        
        user_query = user_query.order_by(order_by).skip(start).limit(length)
        
        
        user_data = [{
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "mobileNumber": user.mobileNumber,
            "addedTime": user.addedTime,
            "updatedTime": user.updatedTime
        } for user in user_query]
        
        
        return jsonify({
            "draw": int(request.args.get('draw', 1)),  
            "recordsTotal": total_user, 
            "recordsFiltered": filtered_user,  
            "data": user_data 
        }), 200

     except Exception as e:
        return jsonify({"status":"error","message":f"Error Occured While retrieving to get logs: {str(e)}"}), 500





        
