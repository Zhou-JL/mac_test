from MyBoKe.model.bk_model import Artical
from MyBoKe.utils.user_contans import STATUE1
from elasticsearch import Elasticsearch
import pymysql
from elasticsearch import helpers

es = Elasticsearch()



def pysql():
    # 打开数据库连接
    db = pymysql.connect(host='xxxxxxxx', port=3306, user='root', passwd='xxxx', db='', charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # sql = "SELECT id,add_time,title,content,click_num,zan,favorite,yunart1,yunart2,user_id FROM artical"
    sql = "SELECT a.title,a.add_time,a.content,a.click_num,a.zan,a.favorite,a.yunart1,a.yunart2,a.user_id,b.username,b.yunicon,a.id FROM artical a inner join user b on a.user_id = b.id"
    cursor.execute(sql)
    action = ({
            "_index": "boke",
            "_source": {
                "title": row[0],
                "add_time": row[1].strftime('%Y-%m-%d'),
                "content": row[2].replace("&nbsp;", "").replace("<br/>", ""),
                "click_num": row[3],
                "zan": row[4],
                "favorite": row[5],
                "yunart1": row[6],
                "yunart2": row[7],
                "user_id": row[8],
                "username": row[9],
                "yunicon": row[10],
                "aid": row[11]
            }
        }for row in cursor.fetchall())
    helpers.bulk(es, action)


def elSearch():
    body = {
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "ik_smart"
                },
                "add_time": {
                    "type": "keyword",
                },
                "content": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "click_num": {
                    "type": "keyword",
                },
                "zan": {
                    "type": "keyword",
                },
                "favorite": {
                    "type": "keyword",
                },
                "yunart1": {
                    "type": "keyword",
                },
                "yunart2": {
                    "type": "keyword",
                },
                "user_id": {
                    "type": "keyword",
                },
                "username": {
                    "type": "keyword",
                },
                "yunicon": {
                    "type": "keyword",
                },
                "aid": {
                    "type": "keyword",
                }
            }
        }
    }
    # 删除索引
    es.indices.delete(index='boke')

    # 如果这个人索引不存在则创建
    if not es.indices.exists(index="boke"):
        print(es.indices.exists(index="boke"))
        # 创建boke这个index
        es.indices.create(index="boke", body=body)

    # es写入数库数据
    pysql()


def insertSuggest():
    dbs = pymysql.connect(host='cccccccc', port=3306, user='root', passwd='ccccccc', db='bokev2',
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = dbs.cursor()

    sql = "SELECT title FROM artical"
    cursor.execute(sql)
    action = ({
        "_index": "mysuggest",
        "_source": {
            "title1": row[0],
            "title2": row[0],
        }
    } for row in cursor.fetchall())
    helpers.bulk(es, action)


def elSuggest():
    body = {
        "mappings": {
            "properties": {
                "title1": {
                    "type": "text",
                    "analyzer": "ik_smart"
                },
                "title2": {
                    "type": "completion",
                    "analyzer": "standard"
                },
            }
        }
    }
    # 删除索引
    es.indices.delete(index='mysuggest')

    # 如果这个人索引不存在则创建
    if not es.indices.exists(index="mysuggest"):
        print(es.indices.exists(index="mysuggest"))
        # mySuggest
        es.indices.create(index="mysuggest", body=body)
    insertSuggest()



if __name__ == "__main__":
    elSearch()
    elSuggest()









