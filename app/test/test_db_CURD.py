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
                        group="zhuke2",
                        project="modoojunko"
                        )
test_data2 = models.Repo(last_update=dt.strftime('%Y%m%d%H%M%S'),
                        domain="www.github.com",
                        group="modeoojunko",
                        project="modoojunko"
                        )

db.session.add(test_data)
db.session.add(test_data2)
db.session.commit()

## query data
print('update repo data')
update_data = models.Repo.query.filter_by(domain="www.github.com").first()
update_data.project = "zhuke"
db.session.commit()
print('update repo data done')

## query repo id
query_id = models.Repo.query.filter_by(project="zhuke").first()
query_repo_id = models.Commit.query.filter_by(repo_id=query_id.id).first()
## insert to commit table
if query_repo_id:
    print('update data')
    commit_data = models.Commit.query.filter_by(repo_id=query_id.id).first()
    commit_data.revision = "1231789580980"
    commit_data.last_update = dt.strftime('%Y%m%d%H%M%S')
    db.session.commit()
    print('update data done')
else:
    print('insert to commit table')
    commit_data = models.Commit(repo_id=query_id.id, revision="jalidjaosikbkhgykjb",
                                last_update=dt.strftime('%Y%m%d%H%M%S'),
                                author="alexander",
                                author_email="alexander@qq.com",
                                author_date=dt.strftime('%Y%m%d%H%M%S'),
                                committer_date=dt.strftime('%Y%m%d%H%M%S'),
                                committer="modoo",
                                committer_email="modoo@11.com",
                                message="world"
                                )
    db.session.add(commit_data)
    db.session.commit()
    print('insert data done')

# query commit id

query_commit_id = models.Commit.query.filter_by(revision="jalidjaosikbkhgykjb").first()
query_commit_diff_id = models.CommitDiff.query.filter_by(commit_id=query_commit_id.id).first()

if query_commit_diff_id:
    print("update commit diff table")
    commit_diff_data = models.CommitDiff.query.filter_by(commit_id=query_commit_id.id).first()
    commit_diff_data.change_file = "/hello.java"
    db.session.commit()
    print('update commit diff done')

else:
    print("insert commit diff table")
    commit_diff_data = models.CommitDiff(commit_id=query_commit_id.id,
                                         last_update=dt.strftime('%Y%m%d%H%M%S'),
                                         change_file="/user/bin/lib/hello.py",
                                         add_lines=32,
                                         del_lines=2
                                         )
    db.session.add(commit_diff_data)
    db.session.commit()
    print("insert commit diff done")


## delete data
## delete commit
delete_repo_data = models.Repo.query.filter_by(project="zhuke").first()
delete_commit_data = models.Commit.query.filter_by(revision="jalidjaosikbkhgykjb").first()
delete_commit_diff = models.CommitDiff.query.filter_by(commit_id=1).first()
db.session.delete(delete_repo_data)
db.session.delete(delete_commit_data)
db.session.delete(delete_commit_diff)
db.session.commit()

## drop all data

#db.drop_all()
