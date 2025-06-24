from . import internBp
from flask import jsonify,request
from datetime import datetime
from models import Intern,User


@internBp.post('/new')
def addIntern():
    try:
        data=request.get_json()

        userId=data.get("user") 

        skills=data.get("skills", [])

        if user == "" or len(skills) == 0:
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
    
@internBp.get('/getAll')
def getAllIntern():
    try:
        intern = Intern.objects()

        InternData = [
            {
    
                "user": intern.user,
                "skills": intern.skills,
                "addedTime": intern.addedTime,
                "updatedTime": intern.updatedTime
            }

            for intern in intern
        ]
        return jsonify({"status":"success","data":InternData, "message":"Intern retrieved Successfully"})
    except Exception as e:
            return jsonify({"status":"error","message":"Intern retrieval error:{e}"})
    
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
        
        intern = Intern.objects(intern=internId).first()

        if not intern:
            return jsonify({"status" : "error","message":"Intern not found"})
        
        intern.delete()
        return jsonify({"status":"success","message":"Intern Deleted Successfully"})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"error occured cant delete{e}"})
    
               
     
            
    
