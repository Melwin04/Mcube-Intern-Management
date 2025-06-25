from models import Task, Project, User
from . import taskBp
from flask import jsonify, request
from datetime import datetime

@taskBp.post('/new')
def createtask():
    try:
        data = request.get_json()

        if data.get("taskName") == "" or data.get("project") == "" or data.get("user") == "":
            return jsonify({"status": "error", "message": "Missing Field required"}), 404

        project = Project.objects(id=data.get("project")).first()

        if not project:
            return jsonify({"status": "error", "message": "Project not found"}), 404
        

        user = User.objects(id=data.get("user")).first()

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
    
@taskBp.get('/getAll')
def getTasks():
    try:
        tasks = Task.objects()
        taskData = [
            {
                "taskName": task.taskName,
                "taskDescription": task.taskDescription,
                "project":task.project,
                "user":task.user,
                "addedTime": task.addedTime,
                "updatedTime": task.updatedTime
            }
            for task in tasks
        ]
        return jsonify({"status": "success", "data": taskData, "message": "task retrieved successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error : {e}"}), 404
    
@taskBp.put('/update')
def updateTask():
    data = request.get_json()
    taskId = request.args.get("id")
    try:
        if not taskId:
            return jsonify({"status":"error","message":"taskId not Found"})
        
        if data.get("taskName") == "" or data.get("project") == "" or data.get("user") == "":
            return jsonify({"status": "error", "message": "Missing Field required"}), 404

        project = Project.objects(id=data.get("project")).first()

        if not project:
            return jsonify({"status": "error", "message": "Project not found"}), 404
        

        user = User.objects(id=data.get("user")).first()

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

