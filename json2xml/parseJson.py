#!/usr/bin/env python # -*- coding: utf8 -*- #parse json，input json filename,output info needed by voc 
from pprint import pprint
from PIL import Image
import json #这里是我需要的8个类别 
#categorys = ['car','bus','person','bike','truck','motor','train','rider'] 
categorys = ['person','rider']
imagePath = "/home/box02/data/json2xml/image/"
def parseJson(jsonFile, imagePath): 
  objs = []
  objtemp = []
  obj = [] 
  f = open(jsonFile) 
  info = json.load(f) 
  print("The number of image is: ",len(info))
  for m in range(0, len(info)):
    objects = info[m]['labels'] 
    flag = 0
    for n in objects: 
      if(n['category'] in categorys): 
        #print("category: ",n['category'])
        flag = 1
    if(flag==1):
      #print('m: ',m)
      #print("The number of image is: ",len(info))
      #objtemp.append([])
      imageName = info[m]['name']
      image = Image.open(imagePath+imageName)
      #print('宽：%d,高：%d'%(im.size[0],im.size[1]))
      #obj.append(str(imageName))
      #print('frame num m: ',m)
      #objs[m].append(obj)
      #obj = []
      objtemp.append(str(imageName))

      obj.append(image.size[0])
      obj.append(image.size[1])
      obj.append(3)
      objtemp.append(obj)
      obj = []

      obj.append(str(info[m]['attributes']['weather']))
      obj.append(str(info[m]['attributes']['scene']))
      obj.append(str(info[m]['attributes']['timeofday']))
      objtemp.append(obj)
      obj = []

      #objects = info[0][0]['objects'] 
      objects = info[m]['labels'] 
      for i in objects: 
        if(i['category'] in categorys): 
          obj.append(str(i['category']))
          #obj.append(str('person'))
          obj.append(int(i['box2d']['x1'])) 
          obj.append(int(i['box2d']['y1'])) 
          obj.append(int(i['box2d']['x2'])) 
          obj.append(int(i['box2d']['y2'])) 
          obj.append(str(i['attributes']['occluded']))
          obj.append(str(i['attributes']['truncated']))   
          obj.append(str(i['attributes']['trafficLightColor']))
          objtemp.append(obj) 
          obj = [] 
      objs.append(objtemp)
      objtemp = []
  #print("objs",objs) 
  print(len(objs))
  #print(objs[0][0])
  #print('%%%%%%%%%')
  #print(len(objs[1]))
  #print('%%%%%%%%%')
  print(objs[0])
  print('%%%%%%%%%')
  print(objs[1])
  return objs 

#test 
#parseJson("/home/box02/data/json2xml/test1/test (copy).json", imagePath)
#parseJson("/home/box02/workspace/BDD/bdd100k/labels/bdd100k_labels_images_train.json", "/home/box02/workspace/BDD/bdd100k/images/100k/train/")

