
import os
import pymongo
from automation_api.utils.dcm import CTImage, Seg, Struct
from automation_api.utils.mongodb import convertMetaToCollection, writeImage, writeSeg
import time
import datetime
import numpy as np
import pydicom
from ssh_pymongo import MongoSession

class DB:
  def __init__(self, dbName='automation', host="127.0.0.1", user=None, password=None, key=None, uri=None, port=22, to_host='127.0.0.1', to_port=27017):
    self.session = MongoSession(host, user, password, key, uri, port, to_host, to_port)
    self.db = self.session.connection[dbName]
    
  def __del__(self):
    self.session.stop()
  
  
  def getUsers(self):
    mycol = self.db["users"]
    
    mydoc = mycol.find().sort("username")
    
    users = []
    for doc in mydoc:
      users.append(str(doc['username']))

    return users
  

  def insertSeries(self, ctList, dataPath):
    data = self.db["data"]
    
    seriesIds = []
    ctMetas = []
    cts = []
    
    for _, ctFileName in enumerate(ctList):
      ctImage = CTImage()
      ctImage.loadCT(ctFileName)
      
      ctMeta = ctImage.getMeta()
      ctMetas.append(ctMeta)
      
      ct = ctImage.getImage()
      cts.append(ctImage.getNpImage())
      
      ctCol = convertMetaToCollection(ctMeta[0], dataPath)
      seriesId = data.insert(ctCol)
      
      seriesIds.append(str(seriesId))
      
      stride = ctMeta[0].Rows*ctMeta[0].Columns*2;
      
      for i, meta in enumerate(ctMeta):
        if (i==0):
          instanceId = seriesId
          myquery = { "_id": seriesId }

        else:
          ctCol = convertMetaToCollection(ctMeta[i], dataPath)
          seriesId2 = data.insert(ctCol)
          instanceId = seriesId2
          myquery = { "_id": seriesId2 }
          
        newvalues = { "$set": { "seriesId": str(seriesId), "instanceId": str(instanceId), "sliceNb": i } }
        data.update_one(myquery, newvalues)
        
        writeImage(dataPath, ctCol, ct[i*stride:(i+1)*stride], str(seriesId), str(instanceId))
        
    return {"seriesIds": seriesIds, "seriesMeta": ctMetas, "data": cts}


  def insertSeg(self, structFileName, ctMeta):
    data = self.db["data"]
    
    segImage = Struct()
    
    #TODO Ideally, we should change RTReferencedSeriesSequence.SeriesInstanceUID, etc. with the correct id in the DB... In the meantime provide all the necessary metaData...
    segImage.loadStruct(structFileName, ctMeta)
    
    segCol = segImage.getMeta()
    
    segIds = []
    
    segId = data.insert(segCol)
    
    return segId
    
   
  def WorkflowEntry(seriesId, segId, users, meta, info, parents, root, label):
    workflows = self.db["workflows"]
    
    ts = time.time()
    isodate = datetime.datetime.fromtimestamp(ts, None)
    
    if isinstance(meta, dict) and not isinstance(meta["PatientID"], pydicom.DataElement):
      col = {
        "root": root,
        "parents": parents,
        "date": isodate,
        "users": users,
        "seriesId": seriesId,
        "segId": segId,
        "PatientName": str(meta["PatientName"]),
        "PatientID": meta["PatientID"],
        "PatientSex": str(meta["PatientSex"]),
        "PatientAge": str(meta["PatientAge"]),
        #"PatientWeight": str(meta.PatientWeight),
        "BodyPartExamined": "",
        "info": str(info),
        "label": label
      }
    else:
      col = {
         "root": root,
        "parents": parents,
        "date": isodate,
        "users": users,
        "seriesId": seriesId,
        "segId": segId,
        "PatientName": str(meta.PatientName),
        "PatientID": meta.PatientID,
        "PatientSex": str(meta.PatientSex),
        "PatientAge": str(meta.PatientAge),
        #"PatientWeight": str(meta.PatientWeight),
        "BodyPartExamined": str(meta.BodyPartExamined) if hasattr(meta, 'BodyPartExamined') else "",
        "info": str(info),
        "label": label
      }    
    
    workflowId = workflows.insert(col)
    
    return workflowId

