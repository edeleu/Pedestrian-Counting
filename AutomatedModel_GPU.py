#This script reads image files from a folder and outputs the pedestrian-counting results to a CSV file
#Image processing and deep learning tasks are performed on the CPU.

from matplotlib import pyplot as plt
from gluoncv import model_zoo, data, utils
import os, csv, time, mxnet as mx

path = "FilePathWithImageFoldersHere"
folder_name="ImageFolderNameHere"
dir=os.path.join(path,folder_name) #Directory with Images
ctx=mx.gpu(0) #Initialize GPU Processing
model_var = "faster_rcnn_resnet50_v1b_coco" #Var from GluonCV modelzoo
#Initialize Deep Learning Model
net = model_zoo.get_model(model_var, pretrained=True,ctx=ctx)

#Reset Classes 
net.reset_class(classes=['person'], reuse_weights=['person'])
tval=0.25 #Threshold Value
tvals=[0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,
0.7,0.75,0.8,0.85,0.9,0.95]
    
def LoadModel(file,filename): #Process image with model
    prev_time=time.time() #Save start time
    #Pre-Process Image
    x, orig_img = data.transforms.presets.rcnn.load_test(file)
    #Run Image through Model
    box_ids, scores, bboxes = net(x.as_in_context(mx.gpu(0)))

    ax = utils.viz.plot_bbox(orig_img, bboxes[0], scores[0], box_ids[0], 
    class_names=net.classes,thresh=tval)
    plt.show() #Visualize Detections

    NewScores=scores.asnumpy().squeeze()
    CSVRow=[str(filename)]
    for NewT in tvals: #Loop over Confidence Thresholds
        people=0
        for i in range(len(NewScores)): #Count People
            if NewScores[i]>=NewT: people+=1
        CSVRow.append(str(people))

    Duration = round((time.time()-prev_time),10) #Calculate Time
    CSVRow.append(str(Duration)) #Add outputs to CSV list
    print(CSVRow)
    return CSVRow

CSVRows=[]
for filename in sorted(os.listdir(dir)): #Loop over images
    if filename.endswith(".jpeg"):
        filepath=os.path.join(dir, filename)
        CSVRows.append(LoadModel(filepath,filename))
    
fields = ['Filename', '0.05','0.10','0.15','0.20','0.25','0.30','0.35',
'0.40','0.45','0.50','0.55','0.60','0.65', '0.70', '0.75','0.80','0.85',
'0.90','0.95',"Duration"] #CSV Headings

csvName = "CSVName.csv" #CSV Filename
CSVpath=os.path.join(path,csvName) 
with open(CSVpath, 'w') as csvfile: #Write data to CSV File
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(CSVRows)


