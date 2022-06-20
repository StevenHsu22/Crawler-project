from flask_restful import reqparse
import pymysql
from flask import jsonify
import util
from flask_apispec import doc, use_kwargs, MethodResource, marshal_with
from user_router_model import *
from flask_jwt_extended import jwt_required

def db_init(): 
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        port=3306,
        db='project'
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    return db, cursor


class Brand_volume(MethodResource):
    #顯示期間內品牌聲量數資訊
    @doc(description='Get brand volume.', tags=['Brand volume'])
    @use_kwargs(BrandGetSchema, location="json")
    @marshal_with(UserGetResponse, code=200)
    def get(self, **kwargs):
        db, cursor = db_init()
        user = {
            'ReviewTime_from': kwargs.get("ReviewTime_from"),
            'ReviewTime_to': kwargs.get("ReviewTime_to"),
            'Brand': kwargs.get("Brand")
        }
        
        if user['Brand'] == 'all':
            #'Brand': 'all'
            sql = """

                SELECT Brand, count(CommentCount) as CommentCount FROM project.all_article 
                where ReviewTime <='{}' AND ReviewTime >='{}'
                GROUP by brand 
                ORDER by CommentCount DESC LIMIT 10;

            """.format(user['ReviewTime_to'], user['ReviewTime_from'], user['Brand'])
        
        else:
            #'Brand': '"饗饗","饗泰多"'    
            sql = """

                SELECT Brand, count(CommentCount) as CommentCount FROM project.all_article 
                where ReviewTime <='{}' AND ReviewTime >='{}' AND Brand in '({})'
                GROUP by brand 
                ORDER by CommentCount DESC LIMIT 10;

            """.format(user['ReviewTime_to'], user['ReviewTime_from'], user['Brand'])

        cursor.execute(sql)

        users = cursor.fetchall()
        db.commit()
        db.close()
        return util.success(users)

class Corp_volume(MethodResource):
    #顯示期間內所有集團聲量數資訊
    @doc(description='Get corp volume.', tags=['Corp volume'])
    @use_kwargs(CorpGetSchema, location="json")
    @marshal_with(UserGetResponse, code=200)
    def get(self, **kwargs):
        db, cursor = db_init()
        user = {
            'ReviewTime_from': kwargs.get("ReviewTime_from"),
            'ReviewTime_to': kwargs.get("ReviewTime_to")
        }

        sql = """

            SELECT Corp, count(CommentCount) as CommentCount FROM project.all_article 
            where ReviewTime <='{}' AND ReviewTime >='{}' 
            GROUP by Corp 
            ORDER by CommentCount DESC LIMIT 10;

        """.format(user['ReviewTime_to'], user['ReviewTime_from'])

        cursor.execute(sql)

        users = cursor.fetchall()
        db.commit()
        db.close()
        return util.success(users)

class Platform_volume(MethodResource):
    #顯示期間內所有平台聲量數資訊
    @doc(description='Get Platform volume.', tags=['Platform volume'])
    @use_kwargs(PlatformGetSchema, location="json")
    @marshal_with(UserGetResponse, code=200)
    def get(self, **kwargs):
        db, cursor = db_init()
        user = {
            'ReviewTime_from': kwargs.get("ReviewTime_from"),
            'ReviewTime_to': kwargs.get("ReviewTime_to")
        }

        sql = """

            SELECT Platform, count(CommentCount) as CommentCount FROM project.all_article 
            where ReviewTime <='{}' AND ReviewTime >='{}'
            GROUP by Platform 
            ORDER by CommentCount DESC LIMIT 10;

        """.format(user['ReviewTime_to'], user['ReviewTime_from'])

        cursor.execute(sql)

        users = cursor.fetchall()
        db.commit()
        db.close()
        return util.success(users)


class Search_Branch_volume(MethodResource):
    #顯示期間內品牌分店聲量數資訊
    @doc(description='Get Brand and Branch volume that you search.', tags=["Search googlereview's brand volume"])
    @use_kwargs(SearchBranchGetSchema, location="json")
    @marshal_with(UserGetResponse, code=200)
    def get(self, **kwargs):
        db, cursor = db_init() 
        user = {
            'ReviewTime_from': kwargs.get("ReviewTime_from"),
            'ReviewTime_to': kwargs.get("ReviewTime_to"),
            'Brand': kwargs.get("Brand")
        }
        
        if user['Brand'] == 'all':

            sql = """

                SELECT Brand, Branch, count(CommentCount) as CommentCount FROM project.all_article 
                where ReviewTime <='{}' AND ReviewTime >='{}' AND Platform = 'GoogleReviews'
                GROUP by Brand
                ORDER by CommentCount DESC LIMIT 10;

            """.format(user['ReviewTime_to'], user['ReviewTime_from'])

        else:
            #'Brand': '"饗饗","饗泰多"'
            sql = """

                SELECT Brand, Branch, count(CommentCount) as CommentCount FROM project.all_article 
                where ReviewTime <='{}' AND ReviewTime >='{}' AND Brand in '({})' AND Platform = 'GoogleReviews'
                GROUP by Brand
                ORDER by CommentCount DESC LIMIT 10;

            """.format(user['ReviewTime_to'], user['ReviewTime_from'], user['Brand'])

        cursor.execute(sql)
        print(user)
        users = cursor.fetchall()
        db.commit()
        db.close()
        return util.success(users)

class Search_comment(MethodResource):
    #模糊搜尋期間內留言，並依日期排序
    @doc(description='Get 100 comments that your search.', tags=['Search Comment'])
    @use_kwargs(SearchcommentGetSchema, location="json")
    @marshal_with(UserGetResponse, code=200)
    def get(self, **kwargs):
        db, cursor = db_init() 
        user = {
            'ReviewTime_from': kwargs.get("ReviewTime_from"),
            'ReviewTime_to': kwargs.get("ReviewTime_to"),
            'Brand': kwargs.get("Brand"),
            'ReviewContent': kwargs.get("ReviewContent")
        }

        if user['Brand'] == 'all':

            sql = """

                SELECT * FROM project.all_article 
                where ReviewTime <='{}' AND ReviewTime >='{}' AND 
                ReviewContent like '%{}%' ORDER BY `ReviewTime` DESC LIMIT 100;

            """.format(user['ReviewTime_to'], user['ReviewTime_from'], user['ReviewContent'])

        else:
            #'Brand': '"饗饗","饗泰多"'
            sql = """

                SELECT * FROM project.all_article 
                where ReviewTime <='{}' AND ReviewTime >='{}' AND
                ReviewContent like '%{}%' and Brand = '{}' ORDER BY `ReviewTime` DESC LIMIT 100;

            """.format(user['ReviewTime_to'], user['ReviewTime_from'], user['ReviewContent'], user['Brand'])


        cursor.execute(sql)
        print(user)
        users = cursor.fetchall()
        db.commit()
        db.close()
        return util.success(users)
