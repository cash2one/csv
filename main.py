from flask import Flask, request,  jsonify
from flask_jsonrpc import JSONRPC
import simplejson as json

from query import pgData,view
# from export_1 import genXls
app = Flask(__name__)
jsonrpc = JSONRPC(app,'/rpc')
app.config.from_object(__name__)


# @jsonrpc.method('data.collector')
# def rec(data):
#     obj = json.loads(data)
#     dataToPg(obj)
#     return "OK"

# @jsonrpc.method('data.update')
# def update(data):
#     obj = json.loads(data)
#     dataUpdate(obj)
#     return "OK"
@jsonrpc.method('data.query')
def query(orderby,sort_order,limit,select_page,isql,date_from,date_to):
    print (orderby,sort_order,limit,select_page,isql,date_from,date_to)
    return pgData(orderby,sort_order,limit,select_page,isql,date_from,date_to)

@jsonrpc.method('gcic.viewUpdate')
def viewUpdate(pointgroup):
    return view(pointgroup)
# @jsonrpc.method('data.export')
# def export(date_from,date_to):
#     # genXls(date_from,date_to)
#     return genXls(date_from,date_to)
# @app.route("/rpc/genexcel",methods=["GET","POST"])
# def gexecel():
#     date_from=request.args.get('date_from')
#     date_to=request.args.get('date_to')
#     resxls =  genXls(date_from,date_to)
#     return  resxls

if __name__=='__main__':
    app.debug =True #
    app.run(host = "127.0.0.1", port = 8888)

    
