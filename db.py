from pymysql import escape_string  # PyMySQL==0.9.3
import mysql.connector  # python -m pip install mysql-connector
import json
#from pixnet import *


# 裝好 MAMP 後，連接 ＭySQL 並新增 database
def creat_database(dbname):
    mydb = mysql.connector.connect(
        host="database-1.cnk8rxvxgjew.us-west-2.rds.amazonaws.com",
        user="admin",
        password="12345678",
        charset="utf8mb4",
        port=3306
    )

    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(dbname))
    mydb.close()


# 填入資料
def insertMessage(name, place, dbname):
    mydb = mysql.connector.connect(
        host="database-1.cnk8rxvxgjew.us-west-2.rds.amazonaws.com",
        user="admin",
        password="12345678",
        charset="utf8mb4",
        database=dbname,
        port=3306
    )
    cursor = mydb.cursor()

    # 建立table
    create_table = """CREATE TABLE IF NOT EXISTS `dorit` (Corp VARCHAR(100)  default NULL,Brand VARCHAR(100)  default NULL,Platform VARCHAR(100)  default NULL,Branch VARCHAR(100)  default NULL,Username VARCHAR(100)  default NULL,ReviewTime DATE,Title VARCHAR(100)  default NULL,ReviewContent VARCHAR(10000)  default NULL,ReviewStar  VARCHAR(10)  default NULL,CommentCount INT default NULL)"""
    cursor.execute(create_table)

    # 存入emoji
    sql = f'''ALTER TABLE `dorit` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci '''
    cursor.execute(sql)

    data = json.load(open('{}'.format(name) + 'Pixnet.json', 'r', encoding='utf-8'))
    for row in data:
        # val 這邊不確定怎麼填有報錯
        # print(row['ReviewStar'])
        sql = '''INSERT INTO `dorit` (Corp,Brand,Platform,Branch,Username,ReviewTime,Title,ReviewContent,ReviewStar,CommentCount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'''
        val = (row['Corp'], row['Brand'], row['Platform'], row['Branch'], row['Username'], row['ReviewTime'],escape_string(row['Title']),
               escape_string(row['ReviewContent']), row['ReviewStar'], row['CommentCount'])
        cursor.execute(sql, val)

    mydb.commit()
    mydb.close()


if __name__ == "__main__":
    dbname = "database0622"
    creat_database(dbname)
    # 輸入你們的品牌 place如果上面有刪除下面就不需要
    names = ['12MINI','HOT7','THE WANG','丰禾','王品','石二鍋','肉次方','西提','尬鍋','和牛涮','青花驕','品田牧場','原燒','夏慕尼','莆田','陶板屋','最肉燒肉','聚北海道鍋物','藝奇','饗食天堂','果然匯','小福利','饗饗','旭集','開飯川食堂','饗泰多','真珠']
    place = 'Pixnet'
    for name in names:
        insertMessage(name, place, dbname)

#先刪除原本的table 再跑一次這個城市 數字不能為null 所以只能帶文字進去 之後圖表分析再轉成數字即可 To "Dorit" 然後你們port號在改成你們要的那個