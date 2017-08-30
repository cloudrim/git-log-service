from app import app, models, jsonify, request
from flask import render_template
import json


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'} # fake user
    return render_template("index.html", title='Home', user=user)


@app.route('/repo', methods=["GET"])
def get_repo():
    repo_list = []
    if request.args: #handle ?abc=hello&xyz=world&ab=hellohello query
        print("read params")
        params = {}
        for item in request.args.items():
            params[item[0]] = item[1]
        data = models.Repo.query.filter_by(**params).first() #use ** to support dict to key=value
        result = {"status": "success","message": "", "data": data.get_repo()}
        return jsonify(result)

    else:
        repos = models.Repo.query.all()
        for repo in repos:
            repo_list.append(repo.get_repo())
        result = {"status": "success","message": "","data": repo_list}
        return jsonify(result)


@app.route('/repo/<int:repo_id>')
def get_repo_via_id(repo_id):
    data = models.Repo.query.filter_by(id=repo_id).first()
    result = {"status": "success","message": "", "data": data.get_repo()}
    return jsonify(result)