import os, sqlite3
from contextlib import closing

# 此文件用于，将飞花令诗句库的 id 重新从 1 排列

database_file = os.path.join(os.path.dirname(__file__), "fei_hua_ling_repo.db")
database = sqlite3.connect(database_file)

with closing(database.cursor()) as cursor:
    all_count = cursor.execute("select count(*) from fhl_poetry").fetchall()[0][0]
    for i in range(1, all_count + 1):
        print(f"{i}/{all_count + 1}", end='\r')
        row = cursor.execute("select * from fhl_poetry where id >= ? order by id limit 1", (i,)).fetchall()
        if len(row) <= 0:
            break
        id = row[0][0]
        cursor.execute("update fhl_poetry set id = ? where id = ?", (i, id))

# 更新 sqlite_sequence 表
cursor.execute("update sqlite_sequence set seq = (select max(id) from fhl_poetry) where name = 'fhl_poetry'")

database.commit()
database.close()