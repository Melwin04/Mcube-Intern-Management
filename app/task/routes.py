from models import Task, Project, User
from . import taskBp
from flask import jsonify, request, session
from datetime import datetime, timedelta
from mongoengine import Q

@taskBp.post('/new')
def createtask():
    try:
        data = request.get_json()

        user = session["user"]

        if not user:
            return jsonify({"status": "error", "message": "UnAuthorized Access. Please Login to continue"}), 403

        if data.get("taskName") == "" or data.get("project") == "" or data.get("user") == "":
            return jsonify({"status": "error", "message": "Missing Field required"}), 404

        project = Project.objects(id=data.get("project")).first()

        if not project:
            return jsonify({"status": "error", "message": "Project not found"}), 404
        

        user = User.objects(id=user.get("id")).first()

        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        task = Task(
            taskName=data.get("taskName"),
            taskDescription=data.get("taskDescription"),
            project=project,
            user=user
        )
        task.save()

        return jsonify({"status": "success", "message": "task Added Successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error: {e}"}), 500
    
# @taskBp.get('/getAll')
# def getTasks():
#     try:
#         tasks = Task.objects()
#         taskData = [
#             {
#                 "taskName": task.taskName,
#                 "taskDescription": task.taskDescription,
#                 "project":task.project,
#                 "user":task.user,
#                 "addedTime": task.addedTime,
#                 "updatedTime": task.updatedTime
#             }
#             for task in tasks
#         ]
#         return jsonify({"status": "success", "data": taskData, "message": "task retrieved successfully"}), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": f"Error : {e}"}), 404
    
@taskBp.put('/update')
def updateTask():
    data = request.get_json()
    taskId = request.args.get("id")
    try:
        user = session["user"]

        if not user:
            return jsonify({"status": "error", "message": "UnAuthorized Access. Please Login to continue"}), 403
        
        if not taskId:
            return jsonify({"status":"error","message":"taskId not Found"})
        
        if data.get("taskName") == "" or data.get("project") == "" or data.get("user") == "":
            return jsonify({"status": "error", "message": "Missing Field required"}), 404

        project = Project.objects(id=data.get("project")).first()

        if not project:
            return jsonify({"status": "error", "message": "Project not found"}), 404
        

        user = User.objects(id=user.get("id")).first()

        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404
        

        task = Task.objects(id=taskId).first()

        if not task:
            return jsonify({"status": "error", "message": "Task not found"}), 404

        task.taskName = data.get("taskName")
        task.taskDescription = data.get("taskDescription")
        task.project = project
        task.user = user
        task.updatedTime = datetime.now()
        task.save()

        return jsonify({"status": "success", "message": "Task updated successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error occurred: {e}"}), 500
    
@taskBp.delete('/delete')
def deleteTask():
    data = request.get_json()
    taskId = request.args.get("id")
    try:
        if not taskId:
            return jsonify({"status":"error","message":"taskId not Found"})

        task = Task.objects(id=taskId).first()
        if not task:
            return jsonify({"status": "error", "message": "Task not found"}), 404

        task.delete()
        return jsonify({"status": "success", "message": "Task deleted successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error occurred while deleting: {e}"}), 500



@taskBp.get('/getAll')
def getTasks():
     try:
        start = int(request.args.get('start', 0))  
        length = int(request.args.get('length', 10))  
        
        
        search_value = request.args.get('search[value]', '')
        
        
        order_column_index = int(request.args.get('order[0][column]', 0))  
        order_direction = request.args.get('order[0][dir]', 'asc')
        
        columns_map = {
            0: 'taskName',  
            1: 'taskDescription',  
            2: 'project',
            3: 'user',
            4: 'addedTime', 
            5: 'updatedTime',  
        }
        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_direction == 'desc' else order_column
        
        task_query = Task.objects()
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        show_errors = request.args.get('show_errors', 'false').lower() == 'true'

        
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                task_query = task_query.filter(log_time__gte=start_dt, log_time__lt=end_dt)
            except ValueError:
                pass  
        
        if show_errors:
            task_query = task_query.filter(status="error")


            
        
        if search_value:
            task_query = task_query.filter(
                Q(skills__icontains=search_value)
            )
        
        
        total_tasks = Task.objects().count()
        
        
        filtered_tasks = task_query.count()
        
        
        task_query = task_query.order_by(order_by).skip(start).limit(length)
        
        
        task_data = [{
            "id": task.id,
            "name": task.taskName,
            "description": task.taskDescription,
            "project": task.project.name,
            "user": task.user.name,
            "addedTime": task.addedTime,
            "updatedTime": task.updatedTime
        } for task in task_query]
        
        
        return jsonify({
            "draw": int(request.args.get('draw', 1)),  
            "recordsTotal": total_tasks,  
            "recordsFiltered": filtered_tasks,  
            "data": task_data  
        }), 200

     except Exception as e:
        return jsonify({"status":"error","message":f"Error Occured While retrieving to get tasks: {str(e)}"}), 500