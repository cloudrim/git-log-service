from app import db


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime)
    domain = db.Column(db.String(80))
    group = db.Column(db.String(80))
    project = db.Column(db.String(80))
    commits = db.relationship('Commit', backref='repo', lazy='dynamic')

    def get_json(self):
        dict = {"last_update": self.last_update,
                "domain": self.domain,
                "group": self.group,
                "project": self.project
                }
        return dict


class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey('repo.id'))
    hash = db.Column(db.String(255))
    last_update = db.Column(db.DateTime)


