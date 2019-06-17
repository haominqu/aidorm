# selfproject
from .models import *

# base
import os
import xlrd
import pymysql



def ReadExcel():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data = xlrd.open_workbook(BASE_DIR+'/院系信息表.xls', encoding_override="utf-8")
    sheet1_name = data.sheet_names()[0]
    sheet1 = data.sheet_by_name(sheet1_name)
    college_list_to_insert = list()
    for rows in range(1, sheet1.nrows):
        row = sheet1.row_values(rows)
        print(type(row[0]), row[1], row[2])
        if row[2] == u"是":
            row[2] = True
        elif row[2] == u"否":
            row[2] = False
        college_list_to_insert.append(College(college_id=str(int(row[0])), college_name=row[1], isDelete=row[2]))
    College.objects.bulk_create(college_list_to_insert)
    return True


#
# conn = pymysql.connect(host='localhost', user='root', password='123456', database='aidorm_db')
# cursor = conn.cursor()
# sql = "insert into College(college_id,college_name,isDelete) values (%s, %s, %s)" % (str(int(row[0])), "'"+row[1]+"'", row[2])
# cursor.execute(sql)
# conn.commit()
# cursor.close()
# conn.close()



















