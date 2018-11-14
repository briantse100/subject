#!/usr/bin/env python # -*- coding: utf8 -*- 
import sys 
from xml.etree import ElementTree 
from xml.etree.ElementTree import Element, SubElement 
from lxml import etree

class PascalVocWriter: 
  def __init__(self, filename, foldername='pedestrian', databaseSrc='The pedestrian database', developer = 'box02@hascovision.com'):     
    self.foldername = foldername #pedestrian
    self.filename = filename #image path
    self.databaseSrc = databaseSrc #The pedestrian database
    self.imgSize = None #image size
    self.boxlist = [] # bounding box 
    #self.localImgPath = None 
    self.condition = None # the condition of taking picture  
    self.developer = developer

  def prettify(self, elem): 
    """
    Return a pretty-printed XML string for the Element.
    """ 
    rough_string = ElementTree.tostring(elem, 'utf8') 
    root = etree.fromstring(rough_string) 
    return etree.tostring(root, pretty_print=True) 

  def genXML(self): 
    """
    Return XML root

    """ 
    # Check conditions 
    if self.filename is None or self.foldername is None or  self.imgSize is None or  len(self.boxlist) <= 0: #bug
      #print(self.filename)
      #print(self.foldername)
      #print(self.imgSize)
      #print(len(self.boxlist))
      return None 

    top = Element('annotation') 
    folder = SubElement(top, 'folder') 
    folder.text = self.foldername 

    filename = SubElement(top, 'filename') 
    filename.text = self.filename 

    #localImgPath = SubElement(top, 'path') 
    #localImgPath.text = self.localImgPath 

    source = SubElement(top, 'source') 
    database = SubElement(source, 'database') 
    database.text = self.databaseSrc 
    weather = SubElement(source, 'weather')
    weather.text = self.condition[0]
    scene = SubElement(source, 'scene')
    scene.text = self.condition[1]
    timeofday = SubElement(source, 'timeofday')
    timeofday.text = self.condition[2]

    owner = SubElement(top, 'owner')
    developer = SubElement(owner, 'developer')
    developer.text = self.developer

    size_part = SubElement(top, 'size') 
    width = SubElement(size_part, 'width') 
    height = SubElement(size_part, 'height') 
    depth = SubElement(size_part, 'depth') 
    width.text = str(self.imgSize[0]) 
    height.text = str(self.imgSize[1]) 

    if len(self.imgSize) == 3: 
       depth.text = str(self.imgSize[2]) 
    else: 
       depth.text = '1' 

    segmented = SubElement(top, 'segmented') 
    segmented.text = '0' 
    return top 

  def addBndBox(self, xmin, ymin, xmax, ymax, name): 
    bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax} 
    bndbox['name'] = name 
    self.boxlist.append(bndbox) 

  def addInfo(self, labelsInfo):    
    self.filename = labelsInfo[0]
    self.imgSize = labelsInfo[1]
    self.condition = labelsInfo[2]
    
    for i in range(3, len(labelsInfo)):
      bndbox = {'xmin': labelsInfo[i][1], 'ymin': labelsInfo[i][2], 'xmax': labelsInfo[i][3], 'ymax': labelsInfo[i][4], 'occluded':labelsInfo[i][5], 'truncated':labelsInfo[i][6], 'trafficLightColor':labelsInfo[i][7]}    
      bndbox['name'] = labelsInfo[i][0] 
      self.boxlist.append(bndbox) 
    

  def appendObjects(self, top): 
    for each_object in self.boxlist: 
      object_item = SubElement(top, 'object') 
      name = SubElement(object_item, 'name') 
      name.text = unicode(each_object['name']) 
      pose = SubElement(object_item, 'pose') 
      pose.text = "Unspecified" 
      truncated = SubElement(object_item, 'truncated') 
      truncated.text = str(each_object['truncated']) 
      occluded = SubElement(object_item, 'occluded')
      occluded.text = str(each_object['occluded'])
      trafficLightColor = SubElement(object_item, 'trafficLightColor')
      trafficLightColor.text = str(each_object['trafficLightColor'])
      difficult = SubElement(object_item, 'Difficult') 
      difficult.text = "0" 
      bndbox = SubElement(object_item, 'bndbox') 
      xmin = SubElement(bndbox, 'xmin') 
      xmin.text = str(each_object['xmin']) 
      ymin = SubElement(bndbox, 'ymin') 
      ymin.text = str(each_object['ymin']) 
      xmax = SubElement(bndbox, 'xmax') 
      xmax.text = str(each_object['xmax']) 
      ymax = SubElement(bndbox, 'ymax') 
      ymax.text = str(each_object['ymax']) 
      
  def save(self, num, bit, saveFilePath=None, targetFile=None): 
    root = self.genXML() 
    self.appendObjects(root) 
    #print(root)
    out_file = None 
    if targetFile is None: 
      #out_file = open(saveFilePath + str(num).zfill(bit) + '.xml', 'w')
      out_file = open(saveFilePath + self.filename[:-4] + '.xml', 'w') 
    else: 
      out_file = open(targetFile, 'w') 
      print('here is the target file!!!')

    prettifyResult = self.prettify(root)
    out_file.write(prettifyResult) 
    out_file.close()
    self.imgSize = None #image size
    self.boxlist = [] # bounding box 
    self.condition = None # the condition of taking picture 

class PascalVocReader: 
  def __init__(self, filepath): 
  # shapes type: 
  # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color] 
    self.shapes = [] 
    self.filepath = filepath 
    self.parseXML() 

  def getShapes(self): 
    return self.shapes 

  def addShape(self, label, bndbox): 
    xmin = int(bndbox.find('xmin').text) 
    ymin = int(bndbox.find('ymin').text) 
    xmax = int(bndbox.find('xmax').text) 
    ymax = int(bndbox.find('ymax').text) 
    points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)] 
    self.shapes.append((label, points, None, None)) 

  def parseXML(self): 
    assert self.filepath.endswith('.xml'), "Unsupport file format" 
    parser = etree.XMLParser(encoding='utf-8') 
    xmltree = ElementTree.parse(self.filepath, parser=parser).getroot() 
    filename = xmltree.find('filename').text
 
    for object_iter in xmltree.findall('object'): 
      bndbox = object_iter.find("bndbox") 
      label = object_iter.find('name').text 
      self.addShape(label, bndbox) 
    return True 

#tempParseReader = PascalVocReader('/home/box02/data/json2xml/Annotations/000000.xml') 
#print tempParseReader.getShapes() 
'''
# Test
tmp = PascalVocWriter('temp','test_', (10,20,3))
tmp.addBndBox(10,10,20,30,'chair')
tmp.addBndBox(1,1,600,600,'car')
tmp.save('/home/box02/data/jeson2xml/test_.xml')
'''


