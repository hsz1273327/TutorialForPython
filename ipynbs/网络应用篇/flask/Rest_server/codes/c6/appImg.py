# --*-- coding:utf-8 --*--
from flask import Flask,request,jsonify,make_response
from flask_restful import Api,Resource
import json

app = Flask(__name__)
api = Api(app)

from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId 

client = MongoClient('mongodb://localhost:27017/')
imgdb = client.Imgs
fs = gridfs.GridFS(imgdb)
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message":"404 not found","code":404}), 404

content_types={
    "jpg":"image/jpeg",
    "png":"image/png",
    "bmp":"application/x-bmp",
    "gif":"image/gif"
}

class ImgsAPI(Resource):
    
    def get(self):
        names = fs.list()
        result = []
        
        objs = [fs.find_one({"filename":i}) for i in names]
        for j in objs:
            imginfo = {}
            imginfo["filename"]=j.name
            imginfo["id"]=str(j._id)
            result.append(imginfo)
        return {"result":result}

    def post(self):
        file_ = request.files['file']
        filename = file_.filename
        format_= filename.decode("utf-8").split(".")[-1].encode("utf-8")
        fs.put(file_.read(),format=format_,filename=filename,owner="hsz",content_type=content_types.get(format_))
        return {"result":"save {name} done!".format(name=filename)}
    
class ImgAPI(Resource):

    def get(self,filename):
        
        img = fs.find_one({"filename":filename})
        if not img:
            abort(404)
            
        imgdata = fs.get(img._id).read()
        response = make_response(imgdata)
        response.headers["Content-Disposition"] = "attachment; filename={filename}".format(filename=filename)

        return response
        

    def delete(self,filename):
        
        fs.delete(fs.find_one({"filename":filename})._id)
        return {"result":"delete {id} done!".format(id=filename)}
    
    
api.add_resource(ImgsAPI, '/api/imgs/')        
api.add_resource(ImgAPI, '/api/img/<string:filename>')  

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)