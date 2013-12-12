from math import ceil
from datetime import timedelta,date
import  time
from decimal import Decimal
from DB import DB
db = DB()

def pages(total, limit):
    # print int(ceil(total / float(limit)))
    return  int(ceil(total / float(limit)))

def checkcount(sql):
    # sql = "select count(*) from gcic_t_avl_testdata"
    countarr = db.query(sql)
    for countlist in countarr:
        for count in countlist:
            pass
        # print  count
        return count

def nextDay(ymd,num=1):
  (year, month, day) = ymd.split('-')
  x = timedelta(days = num)
  y = date(int(year), int(month),int(day))
  return y+x
  # print  y+x
def pgData(orderby,sort_order,limit,select_page,isql,date_from,date_to):
    if orderby == "":
        orderby = "d.id"
    # if selected_item =="":
    #     pass
    # else:
    #     if selected_item in ["speed","pwr_kw"]:
    #         selected_item = "d."+selected_item
    #         restrict = "and %(selected_item)s like '%%%(query_str)s%%'"%{"selected_item":selected_item,"query_str":query_str}
    #     else:
    #         selected_item = "h."+selected_item
    #         restrict = "and %(selected_item)s like '%%%(query_str)s%%'"%{"selected_item":selected_item,"query_str":query_str}
    restrict = isql
    if date_from == "" or date_to =="":
        # ISOTIMEFORMAT = '%Y-%m-%d'
        # timestr = time.strftime(ISOTIMEFORMAT,time.localtime())
        # date_from = nextDay(timestr,-90)
        # date_to = nextDay(timestr)
        # restrict = restrict + " and h.testdate>='%(date_from)s' and h.testdate<='%(date_to)s'"%{"date_from":date_from,"date_to":date_to}
        pass
    else:
        date_to = nextDay(date_to)
        restrict = restrict + " and h.testdate>='%(date_from)s' and h.testdate<='%(date_to)s'"%{"date_from":date_from,"date_to":date_to}
    if isql == "":
        sql = "select count(*) from gcic_t_avl_testdata"
        total = checkcount(sql)
        # print total
    else:
        sql = "select count(*) from gcic_t_avl_testheader h,gcic_t_avl_testdata d where h.esn=d.esn %(restrict)s"%{"restrict":restrict}
        total = checkcount(sql)
    # print total
    totalpage = pages(total,limit)
    offset = limit * (select_page - 1)
    orderby = "order by %s %s"%(orderby,sort_order)
    sql = "select h.testtype, d.speed, d.pwr_kw, h.testcell, h.pallet, h.esn, h.testdate from gcic_t_avl_testheader h,gcic_t_avl_testdata d where h.esn=d.esn %(restrict)s %(orderby)s limit %(limit)s offset %(offset)s "% {"restrict":restrict,"orderby":orderby,"limit":limit,"offset":offset}
    # print sql
    result = db.query(sql)
    keys = result.keys()
    print keys
    print "*"*20
    conarr = result.fetchall()
    data = {}
    for key in keys:
        k = key.encode("utf-8")
        data[k]=[]
    for con in conarr:
        print con
        print "*"*20
        for key in keys:
            obj = con[key]
            if   isinstance(obj, date):
                data[key].append(obj.isoformat())
            # elif isinstance(obj, Decimal):
            #     data[key].append(int(obj))
            else :
                data[key].append(obj)
        data['cols'] = keys
        data['totalpage']=totalpage
    print data
    # return data
def view(esn):
    sql = "select type, status, comments, testcell, pallet, esn, testdate, speed,  pwr_kw, torque, bsfc, fuel_rate, oil_filter_p, blowby_l_p, in_manifold_l_p, coolant_in_t, cell_air_t, fuel_in_p, fuel_in_t, fuel_out_p,  coolant_out_t,  coolant_out_p, coolant_in_p, smoke, turbo_tur_out_l_t, turbo_tur_out_l_p, opacity from gcic_t_avl_data where esn='%s'"%esn
    # print sql
    result = db.query(sql)
    keys = result.keys()
    conarr = result.fetchall()
    data  = {}
    for key in keys:
        k = key.encode("utf-8")
        data[k]=[]
    for con in conarr:
        for key in keys:
            obj = con[key]
            if isinstance(obj,date):
                data[key]=obj.isoformat()
            elif isinstance(obj,Decimal):
                data[key]=int(obj)
            else:
                data[key]=obj
            data['cols'] = keys
        print data
        return data
def export(date_from,date_to):
    date_to=nextDay(date_to)
    # date_to= date_to[:-1]+str(int(date_to[-1:])+1)
    # print date_to
    sql = "select type, status, comments, testcell, pallet, esn, testdate, speed,  pwr_kw, torque, bsfc, fuel_rate, oil_filter_p, blowby_l_p, in_manifold_l_p, coolant_in_t, cell_air_t, fuel_in_p, fuel_in_t, fuel_out_p,  coolant_out_t,  coolant_out_p, coolant_in_p, smoke, turbo_tur_out_l_t, turbo_tur_out_l_p, opacity,createdon from gcic_t_avl_data where createdon > '%s' and createdon <='%s'"%(date_from,date_to)
    result = db.query(sql)
    datalist = []
    conarr = result.fetchall()
    for con in conarr:
        data=[]
        for i in con:
            if isinstance(i,date):
                data.append(i.isoformat())
            elif isinstance(i,Decimal):
                data.append(int(i))
            else:
                data.append(i)
        #~ print data
        datalist.append(data)
    print datalist
    return datalist

if __name__=="__main__":

    # export('2013-09-19','2013-09-30')

    pgData("","desc",10,1,"and h.esn like '%87%'",'2013-09-19','2013-10-10')
    # pgData("","desc",10,1,"",'2013-09-19','2013-10-10')
    # view(7)
    # checkcount()
    # pages(12,5)
