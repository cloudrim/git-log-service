from app import app, models, jsonify, request, db
from flask import render_template


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


@app.route('/repo/<int:repo_id>', methods=["GET"])
def get_repo_via_id(repo_id):
    data = models.Repo.query.filter_by(id=repo_id).first()
    result = {"status": "success", "message": "", "data": data.get_repo()}
    return jsonify(result)


@app.route('/repo/<int:repo_id>/commit', methods=['POST'])
def post_commit(repo_id):
    body = request.get_json(force=True)
    body["repo_id"] = repo_id
    query_revision = models.Commit.query.filter_by(revision=body["revision"]).first()
    if not query_revision:
        insert_data = models.Commit(**body)
        db.session.add(insert_data)
        db.session.commit()
        data = models.Commit.query.filter_by(**body).first()
        result = {"status": "success", "message": "", "data": data.get_commit()}
    else:
        result = {"status": "success", "message": "this revision already exist", "data": body}
    return jsonify(result)