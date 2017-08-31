from app import app, models, jsonify, request
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
    if request.get_json():
        body = request.data
        if "repo_id" in body:
            if "revision" in body:
                if "last_update" in body:
                    if "author" in body:
                        if "author_email" in body:
                            if "commit_date" in body:
                                if "committer" in body:
                                    if "committer_email" in body:
                                        if "title" in body:
                                            if "message" in body:
                                                result = {"status": "success","message": "", "data": body}
                                            else:
                                                result = {"status": "failed","message": "message is missed", "data": ""}
                                        else:
                                            result = {"status": "failed","message": "title is missed", "data": ""}
                                    else:
                                        result = {"status": "failed","message": "committer_email is missed", "data": ""}
                                else:
                                    result = {"status": "failed","message": "committer is missed", "data": ""}
                            else:
                                result = {"status": "failed","message": "commit_date is missed", "data": ""}
                        else:
                            result = {"status": "failed","message": "author_email is missed", "data": ""}
                    else:
                        result = {"status": "failed","message": "author is missed", "data": ""}
                else:
                    result = {"status": "failed","message": "last_update is missed", "data": ""}
            else:
                result = {"status": "failed","message": "revision is missed", "data": ""}
        else:
            result = {"status": "failed","message": "repo_id is missed", "data": ""}
    else:
        result = {"status": "failed", "message": "body is missed", "data": ""}
    return jsonify(result)