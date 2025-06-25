from models import Project
from . import projectBp
from flask import jsonify, request
from datetime import datetime

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

@projectBp.get('/getAll')
def getProjects():
    try:
        projects = Project.objects()
        projectData = [
            {
                "id": str(project.id),
                "name": project.name,
                "description": project.description,
                "addedTime": project.addedTime,
                "updatedTime": project.updatedTime
            }
            for project in projects
        ]
        return jsonify({"status": "success", "data": projectData, "message": "Projects retrieved successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error : {e}"}), 404
    
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
    

        