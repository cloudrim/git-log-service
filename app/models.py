from app import db


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime)
    domain = db.Column(db.String(80))
    group = db.Column(db.String(80))
    project = db.Column(db.String(80))
    status = db.Column(db.String(25))  # running/scheduling/success/failed/error
    commits = db.relationship('Commit', backref='commit', lazy='dynamic')

    def get_repo(self):
        dict = {"id": self.id,
                "last_update": self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                "domain": self.domain,
                "group": self.group,
                "project": self.project,
                "status": self.status
                }
        return dict

    def get_status(self):
        dict = {
            "domain": self.domain,
            "group": self.group,
            "project": self.project,
            "status": self.status,
            "late_update": self.last_update.strftime('%Y-%m-%d %H:%M:%S')
        }
        return dict


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'))
    revision = db.Column(db.String(255), unique=True)
    last_update = db.Column(db.DateTime)
    author = db.Column(db.String(45))
    author_email = db.Column(db.String(45))
    commit_date = db.Column(db.DateTime)
    committer = db.Column(db.String(45))
    committer_email = db.Column(db.String(25))
    title = db.Column(db.String(80))
    message = db.Column(db.String(1024))
    commitdiffs = db.relationship('CommitDiff', backref='commitdiff', lazy='dynamic')

    def get_commit(self):
        dict = {
            "id": self.id,
            "repo_id": self.repo_id,
            "revision": self.revision,
            "last_update": self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
            "author": self.author,
            "author_email": self.author_email,
            "committer": self.committer,
            "committer_email": self.committer_email,
            "title": self.title,
            "message": self.message
        }
        return dict


class CommitDiff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.Integer, db.ForeignKey('commit.id'))
    last_update = db.Column(db.DateTime)
    change_file = db.Column(db.String(255))
    add_lines = db.Column(db.Integer)
    del_lines = db.Column(db.Integer)

    def get_commit_diff(self):
        dict = {
            "id": self.id,
            "commit_id": self.commit_id,
            "last_update": self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
            "change_file": self.change_file,
            "add_lines": self.add_lines,
            "del_lines": self.del_lines
        }
        return dict