from app import db, models
from datetime import datetime

## remove db first

db.drop_all()

## init db

db.create_all()

## insert data

dt=datetime.now()
test_data = models.Repo(last_update=dt.strftime('%Y%m%d%H%M%S'),
                        domain="www.github.com",
                        group="modeoojunko",
                        project="modoojunko"
                        )

db.session.add(test_data)
db.session.commit()

## query data
print('test update data')
update_data = models.Repo.query.filter_by(domain="www.github.com").first()
update_data.project = "zhuke"
db.session.commit()
print('test update data done')

## query repo id
query_id = models.Repo.query.filter_by(project="zhuke").first()
query_commit_id = models.Commit.query.filter_by(repo_id=query_id.id).first()
## insert to commit table
if query_commit_id:
    print('update data')
    commit_data = models.Commit.query.filter_by(repo_id=query_id.id).first()
    commit_data.hash = "1231789580980"
    commit_data.last_update = dt.strftime('%Y%m%d%H%M%S')
    db.session.commit()
    print('update data done')
else:
    print('insert to commit table')
    commit_data = models.Commit(repo_id=query_id.id, hash="jalidjaosikbkhgykjb",last_update=dt.strftime('%Y%m%d%H%M%S'))
    db.session.add(commit_data)
    db.session.commit()
    print('insert data done')


## delete data
## delete commit
delete_repo_data = models.Repo.query.filter_by(project="zhuke").first()
delete_commit_data = models.Commit.query.filter_by(hash="jalidjaosikbkhgykjb").first()
db.session.delete(delete_repo_data)
db.session.delete(delete_commit_data)
db.session.commit()

## drop all data

#db.drop_all()
