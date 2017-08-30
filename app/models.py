from app import db


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime)
    domain = db.Column(db.String(80))
    group = db.Column(db.String(80))
    project = db.Column(db.String(80))
    commits = db.relationship('Commit', backref='repo', lazy='dynamic')

    def get_repo(self):
        dict = {"last_update": self.last_update,
                "domain": self.domain,
                "group": self.group,
                "project": self.project
                }
        return dict


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'))
    revision = db.Column(db.String(255))
    last_update = db.Column(db.DateTime)
    author = db.Column(db.String(45))
    author_email = db.Column(db.String(45))
    commit_date = db.Column(db.DateTime)
    committer = db.Column(db.String(45))
    committer_email = db.Column(db.String(25))
    title = db.Column(db.String(80))
    message = db.Column(db.String(1024))
    commitdiffs = db.relationship('CommitDiff', backref='commit', lazy='dynamic')

    def get_commit(self):
        dict = {
            "id": self.id,
            "repo_id": self.repo_id,
            "revision": self.revision,
            "last_update": self.last_update,
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
            "last_update": self.last_update,
            "change_file": self.change_file,
            "add_lines": self.add_lines,
            "del_lines": self.del_lines
        }
        return dict