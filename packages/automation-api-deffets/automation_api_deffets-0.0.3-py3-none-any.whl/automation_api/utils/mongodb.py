
import os
from bson.json_util import dumps


def convertMetaToCollection(meta, dataPath):
  #TODO Deal with numeric values and arrays
  col = {
    "dataPath": os.path.abspath(dataPath),
    "ImagePositionPatient": list(map(float, meta.ImagePositionPatient)),
    "StudyDate": str(meta.StudyDate),
    "SeriesDate": str(meta.SeriesDate) if hasattr(meta, 'SeriesDate') else "",
    "AcquisitionDate": str(meta.AcquisitionDate),
    #"ContentDate": str(meta.ContentDate),
    "Manufacturer": str(meta.Manufacturer),
    "PatientName": "",
    "PatientID": meta.PatientID,
    "PatientSex": str(meta.PatientSex),
    "PatientAge": str(meta.PatientAge),
    #"PatientWeight": meta.PatientWeight,
    "BodyPartExamined": str(meta.BodyPartExamined) if hasattr(meta, 'BodyPartExamined') else "",
    "SliceThickness": meta.SliceThickness,
    "ProtocolName": str(meta.ProtocolName) if hasattr(meta, 'ProtocolName') else "",
    "PatientPosition": str(meta.PatientPosition),
    "StudyInstanceUID": str(meta.StudyInstanceUID),
    "SeriesInstanceUID": str(meta.SeriesInstanceUID),
    "ImageOrientationPatient": list(map(float, meta.ImageOrientationPatient)),
    "Rows": meta.Rows,
    "Columns": meta.Columns,
    "PixelSpacing": list(map(float, meta.PixelSpacing)),
    "BitsAllocated": meta.BitsAllocated,
    "BitsStored": meta.BitsStored,
    "HighBit": meta.HighBit,
    #"SmallestImagePixelValue": meta.SmallestImagePixelValue,
    #"LargestImagePixelValue": meta.LargestImagePixelValue,
    "RescaleIntercept": str(meta.RescaleIntercept) if hasattr(meta, 'RescaleIntercept') else "",
    "RescaleSlope": str(meta.RescaleSlope) if hasattr(meta, 'RescaleSlope') else "",
    "modalities": str(meta.Modality),
    "modality": str(meta.Modality),
    "Modality": str(meta.Modality),
    "SeriesDescription": str(meta.SeriesDescription) if hasattr(meta, 'SeriesDescription') else ""
  }
  return col

def writeImage(dataPath, metaCol, image, seriesId, instanceId):
  dirPath = os.path.join(dataPath, seriesId)
  
  try:  
    os.mkdir(dirPath)
  except:
    None
    
  with open(os.path.join(dirPath, instanceId+'.txt'), 'w') as outfile:
    outfile.write(dumps(metaCol))
  
  with open(os.path.join(dirPath, instanceId+'.raw'), 'wb') as outfile:
    for item in image:
      outfile.write(bytes([item]))
      
def writeSeg(dataPath, segCol, segData, segId):
  dirPath = os.path.join(dataPath, segId)
  
  try:  
    os.mkdir(dirPath)
  except:
    None
    
  with open(os.path.join(dirPath, "meta.txt"), 'w') as outfile:
    outfile.write(dumps(segCol))
  
  with open(os.path.join(dirPath, 'data.raw'), 'wb') as outfile:
    outfile.write(segData)

