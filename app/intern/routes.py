from . import internBp
from flask import jsonify,request
from datetime import datetime, timedelta
from models import Intern,User
from mongoengine import Q


@internBp.post('/new')
def addIntern():
    try:
        data=request.get_json()

        userId=data.get("user") 

        skills=data.get("skills", [])

        if userId == "" or len(skills) == 0:
            return jsonify({"status":"error","message":"All Fields are Required"})
        
        user=User.objects(id=userId).first()

        if not user:
            return jsonify({"status":"error","message":"User not found"})
        
        intern = Intern(
            user = user,
            skills = skills
        )

        intern.save()

        return jsonify({"status":"success","message":"Intern Added Successful"})

    except Exception as e:
        return jsonify({"status":"error","message": f"Error {e}"})
    
# @internBp.get('/getAll')
# def getAllIntern():
#     try:
#         intern = Intern.objects()

#         InternData = [
#             {
    
#                 "user": intern.user,
#                 "skills": intern.skills,
#                 "addedTime": intern.addedTime,
#                 "updatedTime": intern.updatedTime
#             }

#             for intern in intern
#         ]
#         return jsonify({"status":"success","data":InternData, "message":"Intern retrieved Successfully"})
#     except Exception as e:
#             return jsonify({"status":"error","message":"Intern retrieval error:{e}"})
    
@internBp.put('/update')
def updateIntern():
    internId = request.args.get("id")
    data= request.get_json()
    try:

        if not internId:
            return jsonify({"status":"error","message":"internId not Found"})
        

        intern=Intern.objects(id=internId).first()

        if not intern:
            return jsonify({"status" : "error","message":"Intern not found"})
        
        if data['user']=="":
            return jsonify({"status":"error","message":"Missing Required Field"})
        
        user = User.objects(id=data['user']).first()

        if not user:
            return jsonify({"status" : "error","message":"User not found"})
        

        intern.user = user 
        intern.skills = data["skills"]
        intern.updatedTime = datetime.now()
        intern.save()
        return jsonify({"status":"success","message":"Intern updated Successfully"})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"error occured{e}"})
     
@internBp.delete('/delete')
def deleteIntern():
    internId=request.args.get("id")
    try:

        if not internId:
            return jsonify({"status":"error","message":"internId not Found"})
        
        intern = Intern.objects(id=internId).first()

        if not intern:
            return jsonify({"status" : "error","message":"Intern not found"})
        
        intern.delete()
        return jsonify({"status":"success","message":"Intern Deleted Successfully"})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"error occured cant delete{e}"})
    
    



@internBp.get('/getAll')
def getInterns():
     try:
        start = int(request.args.get('start', 0))  
        length = int(request.args.get('length', 10))  
        
        
        search_value = request.args.get('search[value]', '')
        
        
        order_column_index = int(request.args.get('order[0][column]', 0))  
        order_direction = request.args.get('order[0][dir]', 'asc')
        
        columns_map = {
            0: 'user',  
            1: 'skills',  
            2: 'addedTime', 
            3: 'updatedTime',  
        }
        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_direction == 'desc' else order_column
        
        intern_query = Intern.objects()
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        show_errors = request.args.get('show_errors', 'false').lower() == 'true'

        
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                intern_query = intern_query.filter(log_time__gte=start_dt, log_time__lt=end_dt)
            except ValueError:
                pass  
        
        if show_errors:
            intern_query = intern_query.filter(status="error")


            
        
        if search_value:
            intern_query = intern_query.filter(
                Q(skills__icontains=search_value)
            )
        
        
        total_interns = Intern.objects().count()
        
        
        filtered_interns = intern_query.count()
        
        
        intern_query = intern_query.order_by(order_by).skip(start).limit(length)
        
        
        intern_data = [{
            "id": intern.id,
            "user": intern.user.name,
            "skills": intern.skills,
            "addedTime": intern.addedTime,
            "updatedTime": intern.updatedTime
        } for intern in intern_query]
        
        
        return jsonify({
            "draw": int(request.args.get('draw', 1)),  
            "recordsTotal": total_interns,  
            "recordsFiltered": filtered_interns,  
            "data": intern_data  
        }), 200

     except Exception as e:
        return jsonify({"status":"error","message":f"Error Occured While retrieving to get logs: {str(e)}"}), 500
     
@internBp.get('/get')
def getInternById():
    id = request.args.get("id")
    try: 
        intern = Intern.objects(id=id).first()

        internData = {
            "user": intern.id,
            "skills": intern.skills,
            "addedTime": intern.addedTime,
            "updatedTime": intern.updatedTime
        }

        return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": internData})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {e}"})  