from flask import jsonify
from . import dashboardBp
from models import Intern, Project, Task

@dashboardBp.route('/intern/count')
def intern_count():
    count = Intern.objects.count()
    return jsonify({"count": count})

@dashboardBp.route('/project/count')
def project_count():
    count = Project.objects.count()
    return jsonify({"count": count})

@dashboardBp.route('/task/count')
def task_count():
    count = Task.objects.count()
    return jsonify({"count": count})
