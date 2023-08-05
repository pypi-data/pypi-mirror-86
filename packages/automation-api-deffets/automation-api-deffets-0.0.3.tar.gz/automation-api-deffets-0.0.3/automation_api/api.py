
import os
import pymongo
from automation_api.utils.dcm import CTImage, Seg, Struct
from automation_api.utils.mongodb import convertMetaToCollection, writeImage, readImage
import time
import datetime
import numpy as np
import pydicom
from ssh_pymongo import MongoSession
import pysftp
from bson.objectid import ObjectId

class DB:
  def __init__(self, dataPath="home/ubuntu/test_data", dbName='automation', host="127.0.0.1", user=None, password=None, key=None, port=22, to_host='127.0.0.1', to_port=27017):
    self.session = MongoSession(host, user, password, key=key, uri=None, port=port, to_host=to_host, to_port=to_port)
    self.db = self.session.connection[dbName]
    
    self.sftp = pysftp.Connection(host, username=user, password=password, private_key=key)
    self.dataPath = dataPath;
    
  def __del__(self):
    self.session.stop()
    self.close()
  
  
  
  def getSeg(self, segId):
    data = self.db["data"]
    
    seg = data.find_one({'_id': ObjectId(segId)}, {"_id": 0})
    
    return seg
    
    
  def getSeries(self, seriesId):
    data = self.db["data"]
    
    seriesEntries = list(data.find({'seriesId': str(seriesId)}, {"_id": 0}).sort("sliceNb"))
    
    npImages = []
    
    for i, meta in enumerate(seriesEntries):
      print("Import slice " + str(i+1) + "/" + str(len(seriesEntries)))
      
      sliceData = readImage(seriesEntries[0]["dataPath"], meta, sftp=self.sftp)
      npImages.append(sliceData)
      
      sliceData.reshape((seriesEntries[0]["Rows"], seriesEntries[0]["Columns"]))
    
    data = np.dstack(npImages).astype("float32")
    
    return {"meta": seriesEntries, "data": data}
  
  
  def getUsers(self):
    mycol = self.db["users"]
    
    users = mycol.find().sort("username")
    
    return list(users)
    

  def getUserNames(self):
    users = self.getUsers()
    
    userNames = []
    for user in users:
      userNames.append(str(user['username']))

    return userNames
    
  
  def getWorkflow(self, workflowId):
    workflows = self.db["workflows"]
    
    workflow = workflows.find({"workflowId": str(workflowId)})
      
    return list(workflow)
  
  
  def getWorkflowEntry(self, entryId):
    workflows = self.db["workflows"]
    
    workflow = workflows.find_one({'_id': ObjectId(entryId)}, {"_id": 0})

    return workflow


  def insertSeg(self, structFileName, ctMeta):
    data = self.db["data"]
    
    segImage = Struct()
    
    #TODO Ideally, we should change RTReferencedSeriesSequence.SeriesInstanceUID, etc. with the correct id in the DB... In the meantime provide all the necessary metaData...
    segImage.loadStruct(structFileName, ctMeta)
    
    segCol = segImage.getMeta()
    
    segIds = []
    
    segId = data.insert(segCol)
    
    return segId
    
  
  # Only one dcm file per series. ctList can contain several series
  def insertSeries(self, ctList):
    if not isinstance(ctList, list):
      ctList = [ctList]
    
    data = self.db["data"]
    
    seriesIds = []
    ctMetas = []
    cts = []
    
    for _, ctFileName in enumerate(ctList):
      print("Import series " + str(ctFileName))
      
      ctImage = CTImage()
      ctImage.loadCT(ctFileName)
      
      ctMeta = ctImage.getMeta()
      ctMetas.append(ctMeta)
      
      ct = ctImage.getImage()
      cts.append(ctImage.getNpImage())
      
      ctCol = convertMetaToCollection(ctMeta[0], self.dataPath)
      seriesId = data.insert(ctCol)
      
      seriesIds.append(str(seriesId))
      
      stride = ctMeta[0].Rows*ctMeta[0].Columns*2;
      
      for i, meta in enumerate(ctMeta):
        print("Import slice " + str(i+1) + "/" + str(len(ctMeta)))
        
        if (i==0):
          instanceId = seriesId
          myquery = { "_id": seriesId }

        else:
          ctCol = convertMetaToCollection(ctMeta[i], self.dataPath)
          seriesId2 = data.insert(ctCol)
          instanceId = seriesId2
          myquery = { "_id": seriesId2 }
          
        newvalues = { "$set": { "seriesId": str(seriesId), "instanceId": str(instanceId), "sliceNb": i } }
        data.update_one(myquery, newvalues)
        
        writeImage(self.dataPath, ctCol, ct[i*stride:(i+1)*stride], str(seriesId), str(instanceId), sftp=self.sftp)
        
    return {"seriesIds": seriesIds, "seriesMeta": ctMetas, "data": cts}
    
    
  def insertWorkflowEntry(self, seriesId, segId, users, meta, info, parents, label):
    if(not seriesId):
      seriesId = []
    if(not segId):
      segId = ""
    if(not users):
      users = []
    if(not parents):
      parents = []
    
    
    workflows = self.db["workflows"]
    
    ts = time.time()
    isodate = datetime.datetime.fromtimestamp(ts, None)
    
    if isinstance(meta, dict) and not isinstance(meta["PatientID"], pydicom.DataElement):
      col = {
        "parents": parents,
        "date": isodate,
        "users": users,
        "seriesId": seriesId,
        "segId": segId,
        "PatientName": str(meta["PatientName"]),
        "PatientID": meta["PatientID"],
        "PatientSex": str(meta["PatientSex"]),
        "PatientAge": str(meta["PatientAge"]),
        "BodyPartExamined": "",
        "info": str(info),
        "label": label
      }
    else:
      col = {
        "parents": parents,
        "date": isodate,
        "users": users,
        "seriesId": seriesId,
        "segId": segId,
        "PatientName": str(meta.PatientName),
        "PatientID": meta.PatientID,
        "PatientSex": str(meta.PatientSex),
        "PatientAge": str(meta.PatientAge),
        "BodyPartExamined": str(meta.BodyPartExamined) if hasattr(meta, 'BodyPartExamined') else "",
        "info": str(info),
        "label": label
      }    
    
    entryId = workflows.insert(col)
    
    if (not len(parents)):
      workflowId = str(entryId)
    else:
      parentEntry = self.getWorkflowEntry(parents[0])
      workflowId = parentEntry["workflowId"]
    
    workflows.update_one({"_id": entryId}, {"$set": {"workflowId": workflowId}})
    
    return entryId

