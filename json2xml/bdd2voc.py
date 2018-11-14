#reference https://blog.csdn.net/qq_17278169/article/details/82189776
import os
import pascal_voc_io 
import parseJson 

#dirName = "/media/0A4811140A481114/bdd100k_labels/labels/100k/val" 
#dirName = "/home/box02/workspace/BDD/bdd100k/labels"

dirName = "/home/box02/workspace/BDD/bdd100k/labels"
imagePathTrian = "/home/box02/workspace/BDD/bdd100k/images/100k/train/"
imagePathVal = "/home/box02/workspace/BDD/bdd100k/images/100k/val/" 
saveFilePath = "/home/box02/workspace/BDD/bdd100k/Annotations/" 
saveTxtPathTrian = "/home/box02/workspace/BDD/bdd100k/ImageSets/Main/trainval.txt"
saveTxtPathVal = "/home/box02/workspace/BDD/bdd100k/ImageSets/Main/test.txt"

j = 1 

#test
#dirName = "/home/box02/data/json2xml/test"
#imagePathTrian = "/home/box02/data/json2xml/image/Trian/"
#imagePathVal = "/home/box02/data/json2xml/image/Val/" 
#saveFilePath = "/home/box02/data/json2xml/Annotations/" 
#saveTxtPathTrian = "/home/box02/data/json2xml/image/Trian/trian.txt"
#saveTxtPathVal = "/home/box02/data/json2xml/image/Val/val.txt"

for dirpath,dirnames,filenames in os.walk(dirName): 
  print('dirpath', dirpath)
  print('dirnames', dirnames)
  print('filenames', filenames)
  
  for filepath in filenames: 
    print('filepath', filepath)
    if filepath=='bdd100k_labels_images_train.json':
      imagePath = imagePathTrian
      saveTxtPath = saveTxtPathTrian
      num = 6
    else:
      imagePath = imagePathVal
      saveTxtPath = saveTxtPathVal
      num = 5

    fileName = os.path.join(dirpath,filepath)
    print("processing: ",j) 
    j = j + 1 
    xmlFileName = filepath[:-5] 
    print("xml: ",xmlFileName) 
    objs = parseJson.parseJson(str(fileName), imagePath) 
    print('objs length: ',len(objs))
    with open(saveTxtPath, 'a') as saveTxtFile:
      if len(objs): 
        tmp = pascal_voc_io.PascalVocWriter(fileName) 
        for i in range(0, len(objs)):
        #for obj in objs[i]: 
        #print('obj length: ',len(objs[i]))
        #tmp.addBndBox(obj[0],obj[1],obj[2],obj[3],obj[4]) 
          tmp.addInfo(objs[i])
          tmp.save(i, num, saveFilePath) 
          #saveTxtFile.write(str(i).zfill(num)+'\n')
          saveTxtFile.write(objs[i][0][:-4]+'\n')
      else: 
        print("fileName: ",fileName)

