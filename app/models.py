from app import db


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime)
    domain = db.Column(db.String(80))
    group = db.Column(db.String(80))
    project = db.Column(db.String(80))
    commits = db.relationship('Commit', backref='commit', lazy='dynamic')
    path = db.Column(db.String(255))  # record the sub-folder

    def get_repo(self):
        dict = {"id": self.id,
                "last_update": self.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                "domain": self.domain,
                "group": self.group,
                "project": self.project,
                "path": self.path
                }
        return dict


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'))
    revision = db.Column(db.String(255), unique=True)
    last_update = db.Column(db.DateTime)
    author = db.Column(db.String(255))
    author_email = db.Column(db.String(255))
    author_date = db.Column(db.DateTime)
    committer_date = db.Column(db.DateTime)
    committer = db.Column(db.String(255))
    committer_email = db.Column(db.String(255))
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
            "author_date": self.author_date.strftime('%Y-%m-%d %H:%M:%S'),
            "committer": self.committer,
            "committer_email": self.committer_email,
            "committer_date": self.committer_date.strftime('%Y-%m-%d %H:%M:%S'),
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