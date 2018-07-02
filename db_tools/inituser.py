import sys
import os
from openpyxl import load_workbook,Workbook

from openpyxl.worksheet.table import Table, TableStyleInfo


from datetime import datetime,date
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)
sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Dqrcbankjxkh.settings")
import django
django.setup()
import xlwt,openpyxl
from django.contrib.auth import get_user_model
from users.models import *
User = get_user_model()
from certificates.models import *
from depart.models import *
from rank13.models import *
from coefficient.models import *
def initsuperuser():
    u = User.objects.get(id = 1)
    u.set_password("123456")
    u.save()

def parselevel(choices,info):
    res = 1
    for t in choices:
        #print(t,info,t[1],info in t[1],t[0])
        if info in t[1]:
            res = t[0]
        else:
            continue
    return res


def initusers():
    wb = load_workbook("table.xlsx")

    sheet = wb.get_sheet_by_name("coe")
    l1 = []
    # f = open("log4.txt","a+")
    for row in sheet.iter_rows('A1:AM707'):
        l2 = []
        dic = {}
        count = 0
        for cell in row[0:18]:
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)

        datinfo = str(l2[12])
        dat = datinfo.split(".")
        if dat != "":
            if len(dat) == 2:
                stdate = date(int(dat[0]), int(dat[1]), 1)
            elif len(dat) == 1:
                stdate = date(int(dat[0]), 1, 1)
            else:
                stdate = date.today()
        else:
            stdate = ""

        dic["joinedyears"] = stdate
        dic["idcardnumber"] = l2[1]
        dic["username"] = l2[2]
        dic["name"] = l2[3]
        dic["mobile"] = l2[4]
        dic["clerkrank"] = parselevel(UserProfile.CLERKRANK_CHONCES,l2[5])
        dic["cmanagerrank"] = parselevel(UserProfile.CMANAGERRANK_CHOICES,l2[6])
        dic["cmanagerlevel"] = parselevel(UserProfile.CMANAGERLEVEL_CHOICES,l2[7])
        dic["education"] = parselevel(UserProfile.EDUCATION_CHOICES,l2[13])
        if l2[14] != "":
            dic["title"] = parselevel(UserProfile.TITLE_CHOICES,l2[14])
        else:
            dic["title"] = 0
        if l2[15] != "":
            dic["primccbp"] = int(l2[15])
        else:
            dic["primccbp"] = 0
        if l2[16] != "":

            dic["intermediateccbp"] = int(l2[16])
        else:
            dic["intermediateccbp"] = 0
        if l2[17] != "":

            dic["internel_trainer"] = parselevel(UserProfile.INTERNEL_TRAINER_CHOICES,l2[17])
        else:
            dic["internel_trainer"] = 1
        try:
            User.objects.create(**dic)
            # u = User.objects.get(idcardnumber=dic["idcardnumber"])

            #print(dic)
            pass
        except Exception:
            pass

        #print(dic)
    print("成功生成用户%d"%count)



def updateuserbaseinfo():
    wb = load_workbook("table.xlsx")

    sheet = wb.get_sheet_by_name("coe")
    l1 = []
    # f = open("log4.txt","a+")
    count = 0
    for row in sheet.iter_rows('A1:AM707'):
        l2 = []
        dic = {}

        for cell in row[0:18]:
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)

        datinfo = str(l2[12])
        dat = datinfo.split(".")
        if dat != "":
            if len(dat) == 2:
                stdate = date(int(dat[0]), int(dat[1]), 1)
            elif len(dat) == 1:
                stdate = date(int(dat[0]), 1, 1)
            else:
                stdate = date.today()
        else:
            stdate = ""

        dic["joinedyears"] = stdate
        dic["idcardnumber"] = l2[1]
        dic["username"] = l2[2]
        dic["name"] = l2[3]
        dic["mobile"] = l2[4]
        if l2[5] != "":
            dic["clerkrank"] = parselevel(UserProfile.CLERKRANK_CHONCES,l2[5])
        else:
            dic["clerkrank"] = 1
        if l2[6] != "":
            dic["cmanagerrank"] = parselevel(UserProfile.CMANAGERRANK_CHOICES,l2[6])
        else:
            dic["cmanagerrank"] = 1
        if l2[7] != "":
            dic["cmanagerlevel"] = parselevel(UserProfile.CMANAGERLEVEL_CHOICES,l2[7])
        else:
            dic["cmanagerlevel"] = 1
        dic["education"] = parselevel(UserProfile.EDUCATION_CHOICES,l2[13])

        if l2[14] != "":
            dic["title"] = parselevel(UserProfile.TITLE_CHOICES,l2[14])
        else:
            dic["title"] = 0
        if l2[15] != "":
            dic["primccbp"] = int(l2[15])
        else:
            dic["primccbp"] = 0
        if l2[16] != "":

            dic["intermediateccbp"] = int(l2[16])
        else:
            dic["intermediateccbp"] = 0
        if l2[17] != "":

            dic["internel_trainer"] = parselevel(UserProfile.INTERNEL_TRAINER_CHOICES,l2[17])
        else:
            dic["internel_trainer"] = 1
        try:

            u = User.objects.get(idcardnumber=dic["idcardnumber"])
            #print(u)
            if u.education != dic["education"] or u.title != dic["title"]\
                    or u.internel_trainer != dic["internel_trainer"] or u.clerkrank != dic["clerkrank"]\
                    or u.cmanagerrank != dic["cmanagerrank"] or u.cmanagerlevel != dic["cmanagerlevel"] :
                u.education = dic["education"]
                #print(u.education)
                u.title = dic["title"]
                u.internel_trainer = dic["internel_trainer"]
                u.clerkrank = dic["clerkrank"]
                u.cmanagerrank = dic["cmanagerrank"]
                u.cmanagerlevel = dic["cmanagerlevel"]
                count = count + 1
                # print(count)
                u.save()

            else:
                pass

            #print(dic)
            pass
        except Exception:
            pass

        #print(dic)
    print("成功更新用户学历%d"%count)







def inituserspassword():
    users = User.objects.all()
    for u in users:
        u.set_password("123456")
        u.save()
    print("完成密码重置任务")


def initcerticifates():
    wb = load_workbook("certificates.xlsx")

    sheet = wb.get_sheet_by_name("Sheet1")
    l1 = []
    # f = open("log4.txt","a+")
    count = 0
    for row in sheet.iter_rows('A1:B49'):
        l2 = []
        dic = {}

        for cell in row:
            t = cell.value
            l2.append(t)
        else:
            t = ""
            l2.append(t)
        dic["name"] = l2[0]
        dic["score"] = l2[1]
        dic["desc"] = l2[0]
        try:
            Cerficates.objects.create(**dic)
        except Exception:
            pass
        count =count+1
    print("成功生产证书%d"%count)



def initusercertificates():
    wb = load_workbook("table.xlsx")
    sheet = wb.get_sheet_by_name("coe")
    l1 = []
    # f = open("log4.txt","a+")
    for row in sheet.iter_rows('A1:AM707'):
        l2 = []
        dic = {}
        count = 0
        for cell in (row[2],row[18],row[19],row[20],row[21],row[22],row[23],):
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)

        username = l2[0]
        u = User.objects.get(username=username)
        for c in l2[1:]:

            cer = Cerficates.objects.filter(name=c)
            if cer:
                dic = {}
                dic["user"] = u
                dic["certificate"] = cer[0]
                try:
                    IndexUserCertificate.objects.create(**dic)
                    count = count + 1
                except Exception:
                    pass
            else:
                pass

            count = count +1
           #print(dic)
    print("成功生成用户%d"%count)




def initdeparts():
    wb = load_workbook("departanposts.xlsx")
    sheet = wb.get_sheet_by_name("Sheet1")
    l1 = []
    # f = open("log4.txt","a+")
    agent = Agent.objects.get(id=1)
    for row in sheet.iter_rows('A1:A76'):
        l2 =[]
        for cell in row:
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)
        for d in l2:
            dic = {}
            dic["name"] = d
            dic["desc"] = d
            dic["agent"] = agent
            dic["dept_type"] = 1
            dic["basesalary"] = 1900
            DepartDetail.objects.create(**dic)


def initposts():
    wb = load_workbook("rank13demandcoefficients.xlsx")
    sheet = wb.get_sheet_by_name("Sheet2")
    l1 = []
    # f = open("log4.txt","a+")
    #agent = Agent.objects.get(id=1)
    for row in sheet.iter_rows('A1:A88'):
        l2 =[]
        for cell in row:
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)
        for d in l2:
            dic = {}
            dic["name"] = d
            #print(dic)
            try:
                Post.objects.create(**dic)
            except Exception:
                pass



def initrank13demands():

    wb = load_workbook("rank13demandcoefficients.xlsx")
    sheet = wb.get_sheet_by_name("Sheet3")
    l1 = []
    for row in sheet.iter_rows('A1:K17'):
        l2 =[]
        for cell in row:
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)
        #print(l2)

        posts = l2[1].split(" ")
        #print(len(posts))
        try:
            for post in posts:
                dic = {}
                dic["agent"] = Agent.objects.get(id = 1)
                dic["post"] = Post.objects.get(name=post)
                dic["rank"] = l2[0]
                dic["demandyears"] = l2[2]
                dic["educationdemands"] =parselevel(Rank13Demands.EDUCATION_CHOICES,l2[3])
                dic["primccbpdemands"] = l2[4]
                dic["titledemands"] = parselevel(Rank13Demands.TITLE_CHOICES,l2[5])
                #print(l2)
                #print(dic)
                try:
                    Rank13Demands.objects.create(**dic)
                except Exception:
                    pass
        except Exception:
            pass



def initrank13coe():

    wb = load_workbook("rank13demandcoefficients.xlsx")
    sheet = wb.get_sheet_by_name("Sheet3")
    l1 = []
    for row in sheet.iter_rows('A1:K17'):
        l2 =[]
        for cell in row:
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)
        #print(l2)

        posts = l2[1].split(" ")
        #print(len(posts))
        try:
            for post in posts:
                dic = {}
                dic["agent"] = Agent.objects.get(id = 1)
                dic["post"] = Post.objects.get(name=post)
                dic["rank"] = l2[0]
                dic["demandyears"] = l2[2]
                dic["educationdemands"] =parselevel(Rank13Demands.EDUCATION_CHOICES,l2[3])
                dic["primccbpdemands"] = l2[4]
                dic["titledemands"] = parselevel(Rank13Demands.TITLE_CHOICES,l2[5])
                #print(l2)
                #print(dic)
                # try:
                #     Rank13Demands.objects.create(**dic)
                # except Exception:
                #     pass
                del dic["demandyears"]
                del dic["educationdemands"]
                del dic["primccbpdemands"]
                del dic["titledemands"]

                for i in range(1,6):
                    dic["level"] = i
                    dic["coefficent"] = l2[i+5]
                    #print(dic)
                    try:
                        Rank13Coefficent.objects.create(**dic)
                    except Exception:
                        pass


        except Exception:
            pass


def initcoe():
    wb = load_workbook("table.xlsx")
    sheet = wb.get_sheet_by_name("coe")
    l1 = []
    count = 0
    for row in sheet.iter_rows('A1:AM707'):
        l2 = []
        dic = {}

        for cell in (row[2],row[10],row[11]):
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)
        #print(l2)
        username = l2[0]

        rank13demands = Rank13Demands.objects.filter(post__name=l2[1],rank=l2[2])
        #print(rank13demands)
        if rank13demands:
            user = User.objects.get(username=username)
            dic["user"] = user
            dic["rank13demands"] = rank13demands[0]
            try:

                CoefficientDetail.objects.create(**dic)
            except Exception:
                continue
            count = count +1
        else:
            pass
    print("成功生产系数%d"%count)


def inituserdepart():
    wb = load_workbook("table.xlsx")
    sheet = wb.get_sheet_by_name("coe")
    l1 = []
    count = 0
    for row in sheet.iter_rows('A1:AM707'):
        l2 = []
        dic = {}

        for cell in (row[2],row[8],row[9]):
            if cell.value != None:
                t = cell.value
                l2.append(t)
            else:
                t = ""
                l2.append(t)
        #print(l2)
        username = l2[0]

        departs = DepartDetail.objects.filter(name=l2[1])
        #print(rank13demands)
        if departs:
            user = User.objects.get(username=username)
            dic["user"] = user
            dic["depart"] = departs[0]
            try:
                IndexUserDepart.objects.create(**dic)
            except Exception:
                continue
            count = count +1
        else:
            pass
    print("成功生产用户部门%d"%count)







if __name__=="__main__":
    print("执行函数名",sys.argv[1])
    if sys.argv[1] == "initdeparts":
        initdeparts()
    elif sys.argv[1] == "initposts":
        initposts()
    elif sys.argv[1] == "initusers":
        initusers()
    elif sys.argv[1] == "initrank13demands":
        initrank13demands()
    elif sys.argv[1] == "initrank13coe":
        initrank13coe()
    elif sys.argv[1] == "initcoe":
        initcoe()
    elif sys.argv[1] == "inituserdepart":
        inituserdepart()
    elif sys.argv[1] == "updateuserbaseinfo":
        updateuserbaseinfo()
    else:
        print(" 无效指令")


