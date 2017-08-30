from app import app, models, jsonify, request
from flask import render_template
import json


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'} # fake user
    return render_template("index.html", title='Home', user=user)

@app.route('/repo', methods=["GET"])
def repo():
    repo_list = []
    if request.args: #handle ?abc=hello&xyz=world&ab=hellohello query
        #get [('abc', u'hello'), ('xyz', u'world'), ('ab', u'hellohello')]
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