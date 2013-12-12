import re
import csv, sys
import ConfigParser
from time import time, strftime, localtime
from  DB import DB
db = DB()
# filename = "C:\Users\Administrator\Desktop\data\SN_90003181_20131008161112_Meas.csv"
# filename = "C:\Users\Administrator\Desktop\data\SN_90003187_20131008164922_Meas.csv"
# config = ConfigParser.ConfigParser()
# config.read('config.ini')
# filename = config.get('path','filepath')
def getStrTime(sec):
    return strftime('%Y-%m-%d %H:%M:%S', localtime(sec))

def save_header(esn, testdate,cell_name):
    # print esn,testdate
    dic = {}
    # esn = esn[-8:]
    # testdate = testdate[-20:-3]
    dic["esn"]=esn[-8:]
    dic["testdate"]=testdate[-20:-3]
    dic["cell_name"]=cell_name[-4:]
    cols = '''
    pallet 1,
    testtype 1,
    teststatus 1,
    auditstatus 1,
    referenceid 1,
    lastupdateon now(),
    lastupdatedby mabotech,
    createdon now(),
    createdby mabo,
    active 1,
    rowversionstamp 1'''

    for collist in cols.split(","):
        colarr = collist.split(" ")
        dic[colarr[4]]=colarr[-1]
    print dic

    sql = "insert into gcic_t_avl_testheader(esn,testcell,pallet,testdate,testtype,teststatus,auditstatus,referenceid,lastupdateon,lastupdatedby,createdon,createdby,active,rowversionstamp)values('%(esn)s', '%(cell_name)s', '%(pallet)s', '%(testdate)s', '%(testtype)s','%(teststatus)s', '%(auditstatus)s', '%(referenceid)s', '%(lastupdateon)s', '%(lastupdatedby)s', '%(createdon)s', '%(createdby)s', '%(active)s', '%(rowversionstamp)s')"%dic
    print sql
    db.execute(sql)

def save_data(esn,row):
    dic = {}
    esn = esn[-8:]
    cols ="""
    turbo_tur_out_l_t  1,
    testdatatype       1,
    turbo_tur_out_l_p  1,
    opacity            1,
    referenceid        1,
    lastupdateon       now(),
    lastupdatedby      mabo,
    createdon          now(),
    createdby          Mabotech,
    active             1,
    rowversionstamp    1"""
    for collist in cols.split(","):
        # print collist
        colarr = collist.split(" ")
        # print colarr
        dic[colarr[4]]=colarr[-1]
    param = ['measurement number', 'speed', 'pwr_kw', 'torque', 'bsfc', 'fuel_rate', 'oil_filter_p', 'blowby_l_p', 'in_manifold_l_p', 'coolant_out_t', 'cell_air_t', 'fuel_in_p', 'fuel_in_t', 'fuel_out_p', 'coolant_in_p', 'coolant_in_t', 'coolant_out_p', 'smoke', 'cac_air_t_fb']
    for i in range(0,len(row)):
        dic[param[i]]=row[i]
    dic["esn"] = esn
    sql = " insert into gcic_t_avl_testdata(esn,rowseq,testdatatype,speed,pwr_kw,torque,bsfc,fuel_rate,oil_filter_p,blowby_l_p,in_manifold_l_p,coolant_in_t,cell_air_t,fuel_in_p,fuel_in_t,fuel_out_p,coolant_out_t,coolant_out_p,coolant_in_p,smoke,turbo_tur_out_l_t,turbo_tur_out_l_p,opacity,referenceid,lastupdateon,lastupdatedby,createdon,createdby,active,rowversionstamp)values('%(esn)s', '%(measurement number)s', '%(testdatatype)s', '%(speed)s', '%(pwr_kw)s', '%(torque)s', '%(bsfc)s', '%(fuel_rate)s', '%(oil_filter_p)s', '%(blowby_l_p)s', '%(in_manifold_l_p)s', '%(coolant_in_t)s', '%(cell_air_t)s', '%(fuel_in_p)s', '%(fuel_in_t)s', '%(fuel_out_p)s', '%(coolant_out_t)s', '%(coolant_out_p)s', '%(coolant_in_p)s', '%(smoke)s', '%(turbo_tur_out_l_t)s', '%(turbo_tur_out_l_p)s', '%(opacity)s', '%(referenceid)s', '%(lastupdateon)s', '%(lastupdatedby)s', '%(createdon)s', '%(createdby)s', '%(active)s', '%(rowversionstamp)s')"%dic
    # import datetime
    # print datetime.datetime.now()
    print sql
    db.execute(sql)

def search(keyparam,colparam):
    flag = re.search(keyparam, colparam)
    return flag

def main(filename):
    state = 0
    esn = None
    testdate = None
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                # print len(row)
                if len(row) == 0:
                    continue
                if row[0]=="[HEADER START]":
                    if state == 0:
                        state = 1
                    else:
                        raise Exception('data resource incorrect')
                elif search("MeasurementName",row[0]):
                    esn = row[0]
                    # print esn[-8:]
                elif search("MeasurementStartTime",row[0]):
                    testdate = row[0]
                    # print testdate[-20:-3]
                elif search("CELL_NAME",row[0]):
                    cell_name = row[0]
                    # print cell_name[-4:]
                elif row[0]=="[HEADER END]":
                    state = 2
                    # print esn,testdate
                    save_header(esn,testdate,cell_name)
                elif row[0] == "[DATA START]":
                    state = 3
                elif row[0] == "[DATA END]":
                    state = 0
                    esn = None
                if state == 3 and row[0] == "6":
                    if esn == None:
                        raise Exception("no esn")
                    save_data(esn, row)
                elif state == 3 and row[0] == "8":
                    save_data(esn, row)
                elif state == 3 and row[0] == "10":
                    save_data(esn, row)
                elif state == 3 and row[0] == "12":
                    save_data(esn, row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
if __name__=="__main__":
    main()
    #csvRead()
