from models import Project
from . import projectBp
from flask import jsonify, request
from datetime import datetime,timedelta
from mongoengine import Q


@projectBp.post('/new')
def createProject():
    try:
        data = request.get_json()

        if data.get("name") == "":
            return jsonify({"status": "error", "message": "Name Field required"}), 404

        project = Project(
            name=data.get("name"),
            description=data.get("description")
        )
        project.save()

        return jsonify({"status": "success", "message": "Project Added Successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {e}"}), 500

# @projectBp.get('/getAll')
# def getProjects():
#     try:
#         projects = Project.objects()
#         projectData = [
#             {
#                 "id": str(project.id),
#                 "name": project.name,
#                 "description": project.description,
#                 "addedTime": project.addedTime,
#                 "updatedTime": project.updatedTime
#             }
#             for project in projects
#         ]
#         return jsonify({"status": "success", "data": projectData, "message": "Projects retrieved successfully"}), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": f"Error : {e}"}), 404
    
@projectBp.put('/update')
def updateProject():
    projectId = request.args.get("id")
    data = request.get_json()
    try:
        if not projectId:
            return jsonify({"status": "error", "message": "Project ID not found"}), 404
        
        if data.get("name") == "":
            return jsonify({"status": "error", "message": "Name Field is Missing"}), 404

        project = Project.objects(id=projectId).first()
        if not project:
            return jsonify({"status": "error", "message": "Project not found"}), 404

        project.name = data["name"]
        project.description = data.get("description")
        project.updatedTime = datetime.now()
        project.save()

        return jsonify({"status": "success", "message": "Project updated successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error occurred: {e}"}), 404

@projectBp.delete('/delete')
def deleteProject():
    projectId = request.args.get("id")
    try:
        if not projectId:
            return jsonify({"status": "error", "message": "Project ID not found"}), 404

        project = Project.objects(id=projectId).first()
        if not project:
            return jsonify({"status": "error", "message": "Project not found"}), 404

        project.delete()
        return jsonify({"status": "success", "message": "Project deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error : {e}"}), 404
    

@projectBp.get('/getAllNames')
def getUsers():
    
    try: 
        projects = Project.objects()

        projectData = [{
                "id": project.id,
                "text": project.name
        }
        for project in projects
        ]

        return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": projectData})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error {e}"})


    
@projectBp.get('/getAll')
def getProjects():
     try:
        start = int(request.args.get('start', 0))  
        length = int(request.args.get('length', 10))  
        
        
        search_value = request.args.get('search[value]', '')
        
        
        order_column_index = int(request.args.get('order[0][column]', 0))  
        order_direction = request.args.get('order[0][dir]', 'asc')
        
        columns_map = {
            0: 'name',  
            1: 'description',  
            2: 'addedTime', 
            3: 'updatedTime',  
        }
        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_direction == 'desc' else order_column
        
        project_query = Project.objects()
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        show_errors = request.args.get('show_errors', 'false').lower() == 'true'

        
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                project_query = project_query.filter(log_time__gte=start_dt, log_time__lt=end_dt)
            except ValueError:
                pass  
        
        if show_errors:
            project_query = project_query.filter(status="error")


            
        
        if search_value:
            project_query = project_query.filter(
                Q(name__icontains=search_value) |
                Q(description__icontains=search_value)
            )
        
        
        total_project = Project.objects().count()
        
        
        filtered_project = project_query.count()
        
        
        project_query = project_query.order_by(order_by).skip(start).limit(length)
        
        
        project_data = [{
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "addedTime": project.addedTime,
            "updatedTime": project.updatedTime
        } for project in project_query]
        
        
        return jsonify({
            "draw": int(request.args.get('draw', 1)),  
            "recordsTotal": total_project,  
            "recordsFiltered": filtered_project,  
            "data": project_data 
        }), 200

     except Exception as e:
        return jsonify({"status":"error","message":f"Error Occured While retrieving to get logs: {str(e)}"}), 500





        