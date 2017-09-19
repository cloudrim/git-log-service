from app import app, models, jsonify, request, db
from flask import render_template


# repo api
@app.route('/repo', methods=['POST'])
def insert_repo():
    body = request.get_json(force=True)  # send data to rabbitmq in queue
    query_repo_exists = models.Repo.query.filter_by(group=body["group"],
                                                    domain=body["domain"],
                                                    project=body["project"]
                                                    ).first()
    if query_repo_exists:
        result = {"status": "202", "message": "this repo already exist", "data": body}
    else:
        insert_repo_data = models.Repo(**body)
        db.session.add(insert_repo_data)
        db.session.commit()
        data = models.Repo.query.filter_by(**body).first()
        if data:
            result = {"status": "200", "message": "", "data": data.get_repo()}
        else:
            result = {"status": "401", "message": "insert data to repo table error", "data": ""}
    return jsonify(result)


@app.route('/')
@app.route('/repo', methods=["GET"])
def get_repo():
    repo_list = []
    if request.args: #handle ?abc=hello&xyz=world&ab=hellohello query
        print("read params")
        params = {}
        data_list = []
        for item in request.args.items():
            params[item[0]] = item[1]
        if models.Repo.query.filter_by(**params).first():
            datas = models.Repo.query.filter_by(**params)  # use ** to support dict to key=value
            for data in datas:
                data_list.append(data.get_repo())
            result = {"status": "200", "message": "", "data": data_list}
        else:
            result = {"status": "201", "message": "no data for these params: " + str(request.args.items()), "data": ""}
        return jsonify(result)

    else:
        repos = models.Repo.query.all()
        for repo in repos:
            repo_list.append(repo.get_repo())
        result = {"status": "200", "message": "", "data": repo_list}
        return jsonify(result)


@app.route('/repo/<int:repo_id>', methods=["PUT"])
def update_repo(repo_id):
    pre_update_repo = models.Repo.query.filter_by(id=repo_id).first()
    body = request.get_json(force=True)
    if pre_update_repo:
        if "domain" in body:
            pre_update_repo.domain = body["domain"]
        if "group" in body:
            pre_update_repo.group = body["group"]
        if "project" in body:
            pre_update_repo.project = body["project"]
        if "last_update" in body:
            pre_update_repo.last_update = body["last_update"]
        db.session.commit()
        data = models.Repo.query.filter_by(id=repo_id).first()
        result = {"status": "200", "message": "", "data": data.get_repo()}
    else:
        result = {"status": "201", "message": "no data for the repo id: " + repo_id, "data": ""}
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
    if request.args:  # handle ?abc=hello&xyz=world&ab=hellohello query
        params = {}
        for item in request.args.items():
            params[item[0]] = item[1]
        data = models.Commit.query.filter_by(**params).first()  # use ** to support dict to key=value
        if data:
            result = {"status": "200", "message": "", "data": data.get_commit()}
        else:
            result = {"status": "201", "message": "no data for these params: " + str(request.args.items()), "data": ""}
        return jsonify(result)
    else:
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
            if request.args:  # handle ?abc=hello&xyz=world&ab=hellohello query
                params = {}
                for item in request.args.items():
                    params[item[0]] = item[1]
                data = models.CommitDiff.query.filter_by(**params).first()  # use ** to support dict to key=value
                if data:
                    result = {"status": "200", "message": "", "data": data.get_commit_diff()}
                else:
                    result = {"status": "201", "message": "no data for these params: " + str(request.args.items()),
                              "data": ""}
            else:
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
