from app import app, models, jsonify, request, db
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'} # fake user
    return render_template("index.html", title='Home', user=user)


# repo api
@app.route('/repo', methods=["GET"])
def get_repo():
    repo_list = []
    if request.args: #handle ?abc=hello&xyz=world&ab=hellohello query
        print("read params")
        params = {}
        for item in request.args.items():
            params[item[0]] = item[1]
        data = models.Repo.query.filter_by(**params).first() #use ** to support dict to key=value
        if data:
            result = {"status": "200", "message": "", "data": data.get_repo()}
        else:
            result = {"status": "201", "message": "empty data", "data": ""}
        return jsonify(result)

    else:
        repos = models.Repo.query.all()
        for repo in repos:
            repo_list.append(repo.get_repo())
        result = {"status": "200", "message": "", "data": repo_list}
        return jsonify(result)


@app.route('/repo/<int:repo_id>', methods=["GET"])
def get_repo_via_id(repo_id):
    data = models.Repo.query.filter_by(id=repo_id).first()
    if data:
        result = {"status": "200", "message": "", "data": data.get_repo()}
    else:
        result = {"status": "201", "message": "empty data", "data": ""}
    return jsonify(result)


# commit api
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
        result = {"status": "200", "message": "", "data": data.get_commit()}
    else:
        result = {"status": "202", "message": "this revision already exist", "data": body}
    return jsonify(result)


@app.route('/repo/<int:repo_id>/commit', methods=["GET"])
def query_commit_id(repo_id):
    commit_id_list = models.Commit.query.filter_by(repo_id=repo_id)
    if commit_id_list:
        data = []
        for commit_id in commit_id_list:
            data.append(commit_id.get_commit())
        result = {"status": "200", "message": "", "data": data}
    else:
        result = {"status": "201", "message": "empty data", "data": ""}
    return jsonify(result)


@app.route('/repo/<int:repo_id>/commit/<int:commit_id>', methods=["GET"])
def query_one_commit_id(repo_id, commit_id):
    query_repo = models.Repo.query.filter_by(id=repo_id).first().get_repo()
    if query_repo:
        query_commit = models.Commit.query.filter_by(id=commit_id, repo_id=repo_id).first()
        if query_commit:
            result = {"status": "200", "message": "", "data": query_commit.get_commit()}
        else:
            result = {"status": "201", "message": "empty data for commit_id: " + str(commit_id), "data": ""}
    else:
        result = {"status": "201", "message": "empty data for repo_id: " + str(repo_id), "data": ""}
    return jsonify(result)


# commit diff api
@app.route('/repo/<int:repo_id>/commit/<int:commit_id>/commit_diff', methods=["POST"])
def insert_commit_diff(repo_id, commit_id):
    query_repo = models.Repo.query.filter_by(id=repo_id).first()
    body = request.get_json(force=True)
    if query_repo:
        query_commit = models.Commit.query.filter_by(id=commit_id, repo_id=repo_id).first()
        if query_commit:
            query_commit_diff = models.CommitDiff.query.filter_by(**body).first()
            if not query_commit_diff:
                insert_commit_diff_data = models.CommitDiff(**body)
                db.session.add(insert_commit_diff_data)
                db.session.commit()
                data = models.CommitDiff.query.filter_by(**body).first().get_commit_diff()
                result = {"status": "200", "message": "", "data": data}
            else:
                result = {"status": "202", "message": "commit_diff table already has this", "data": ""}
        else:
            result = {"status": "201", "message": "empty data for commit : " + str(commit_id), "data": ""}
    else:
        result = {"status": "201", "message": "empty data for repo_id: " + str(repo_id), "data": ""}
    return jsonify(result)


@app.route('/repo/<int:repo_id>/commit/<int:commit_id>/commit_diff', methods=["GET"])
def query_commit_diff(repo_id, commit_id):
    query_repo = models.Repo.query.filter_by(id=repo_id).first()
    if query_repo:
        query_commit = models.Commit.query.filter_by(id=commit_id, repo_id=repo_id).first()
        if query_commit:
            query_commit_diff_data = models.CommitDiff.query.filter_by(commit_id=commit_id)
            if query_commit_diff_data.first():
                data = []
                for commit_diff in query_commit_diff_data:
                    data.append(commit_diff.get_commit_diff())
                result = {"status": "200", "message": "", "data": data}
            else:
                result = {"status": "201", "message": "empty commit diff data for commit : " + str(commit_id),
                          "data": ""}
        else:
            result = {"status": "201", "message": "empty commit data for commit : " + str(commit_id), "data": ""}
    else:
        result = {"status": "201", "message": "empty repo data for repo_id: " + str(repo_id), "data": ""}

    return jsonify(result)
