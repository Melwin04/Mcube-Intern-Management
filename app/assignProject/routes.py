from flask import jsonify, request, session
from datetime import datetime, timedelta
from models import Assign_project, Project, User, Task
from . import assignBp
from mongoengine import Q

@assignBp.post('/new')
def create_assignment():
    try:
        data = request.get_json()
        user_session = session.get("user")

        if not user_session:
            return jsonify({"status": "error", "message": "Unauthorized access"}), 403

        if not data.get("task") or not data.get("user") or not data.get("deadline"):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        task = Task.objects(id=data.get("task")).first()
        user = User.objects(id=data.get("user")).first()

        if not task or not user:
            return jsonify({"status": "error", "message": "Invalid task/user"}), 404

        assignment = Assign_project(
            task=task,
            user=user,
            status=data.get("status", "Not Started"),
            deadline=datetime.strptime(data.get("deadline"), '%Y-%m-%d') if data.get("deadline") else None,
            addedTime=datetime.now()
        )
        assignment.save()

        return jsonify({"status": "success", "message": "Assignment created successfully"}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error occurred: {e}"}), 500


@assignBp.get('/getAll')
def getAssignProjects():
     try:
        start = int(request.args.get('start', 0))  
        length = int(request.args.get('length', 10))  
        
        
        search_value = request.args.get('search[value]', '')
        
        
        order_column_index = int(request.args.get('order[0][column]', 0))  
        order_direction = request.args.get('order[0][dir]', 'asc')
        
        columns_map = {
            0: 'task',    
            1: 'user',
            2: 'status',
            3: 'deadline',
            4: 'addedTime', 
            5: 'updatedTime',  
        }
        order_column = columns_map.get(order_column_index)
        order_by = f"-{order_column}" if order_direction == 'desc' else order_column
        
        assign_query = Assign_project.objects()
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        show_errors = request.args.get('show_errors', 'false').lower() == 'true'

        
        if start_date and end_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                assign_query = assign_query.filter(log_time__gte=start_dt, log_time__lt=end_dt)
            except ValueError:
                pass  
        
        if show_errors:
            assign_query = assign_query.filter(status="error")


            
        
        if search_value:
            assign_query = assign_query.filter(
                Q(status__icontains=search_value)
            )
        
        
        total_assignTasks = Assign_project.objects().count()
        
        
        filtered_assignTasks = assign_query.count()
        
        
        assign_query = assign_query.order_by(order_by).skip(start).limit(length)
        
        
        task_data = [{
            "id": task.id,
            "task": task.task.taskName,
            "project": task.task.project.name,
            "user": task.user.name,
            "status": task.status,
            "deadline": task.deadline,
            "addedTime": task.addedTime,
            "updatedTime": task.updatedTime
        } for task in assign_query]
        
        
        return jsonify({
            "draw": int(request.args.get('draw', 1)),  
            "recordsTotal": total_assignTasks,  
            "recordsFiltered": filtered_assignTasks,  
            "data": task_data  
        }), 200

     except Exception as e:
        return jsonify({"status":"error","message":f"Error Occured While retrieving to get tasks: {str(e)}"}), 500
    
# from flask import jsonify, request, session
# from datetime import datetime
# from uuid import uuid4
# from mongoengine import Document, StringField, ReferenceField, DateField, CASCADE

# from models import Assign_project, Task, User, Project
# from . import assignBp

# # Create a new assignment
# @assignBp.post('/new')
# def create_assignment():
#     try:
#         data = request.get_json()
#         user_session = session.get("user")

#         if not user_session:
#             return jsonify({"status": "error", "message": "Unauthorized access"}), 403

#         if not all([data.get("taskName"), data.get("project"), data.get("user"), data.get("status"), data.get("deadline")]):
#             return jsonify({"status": "error", "message": "Missing required fields"}), 400

#         task = Task.objects(id=data["taskName"]).first()
#         project = Project.objects(id=data["project"]).first()
#         user = User.objects(id=data["user"]).first()

#         if not all([task, project, user]):
#             return jsonify({"status": "error", "message": "Invalid task, project, or user"}), 404

#         assignment = Assign_project(
#             taskName=task,
#             project=project,
#             user=user,
#             status=data["status"],
#             deadline=datetime.strptime(data["deadline"], "%Y-%m-%d"),
#             addedTime=datetime.now()
#         )
#         assignment.save()

#         return jsonify({"status": "success", "message": "Project assigned successfully"}), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# # Get all assignments for DataTables
# @assignBp.get('/getAll')
# def get_all_assignments():
#     try:
#         assignments = Assign_project.objects()
#         assignment_data = [{
#             "id": str(assignment.id),
#             "task": assignment.taskName.taskName,
#             "project": assignment.project.name,
#             "user": assignment.user.name,
#             "status": assignment.status,
#             "deadline": assignment.deadline.strftime('%Y-%m-%d') if assignment.deadline else "N/A",
#             "addedTime": assignment.addedTime.strftime('%Y-%m-%d'),
#             "updatedTime": assignment.updatedTime.strftime('%Y-%m-%d') if assignment.updatedTime else "N/A"
#         } for assignment in assignments]

#         return jsonify({
#             "draw": int(request.args.get('draw', 1)),
#             "recordsTotal": len(assignment_data),
#             "recordsFiltered": len(assignment_data),
#             "data": assignment_data
#         }), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


# # Get all Users
# @assignBp.get('/getAllUsers')
# def get_all_users():
#     try:
#         users = User.objects()
#         data = [{"id": str(user.id), "text": user.name} for user in users]
#         return jsonify({"status": "success", "data": data}), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500



# @assignBp.get('/getAllTasks')
# def get_all_tasks():
#     try:
#         tasks = Task.objects()
#         data = [{"id": str(task.id), "text": task.taskName} for task in tasks]
#         return jsonify({"status": "success", "data": data}), 200
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

