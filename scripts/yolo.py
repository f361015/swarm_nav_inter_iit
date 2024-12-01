#!/usr/bin/env python3

import rospy
from ultralytics import YOLO
from sensor_msgs.msg import Image
import numpy as np
import cv2


from cv_bridge import CvBridge
bridge = CvBridge()

class IMGRec:
    def __init__(self,FOV_X=62.2, FOV_Y=48.8):
        self.model =  YOLO("./src/swarm_nav_inter_iit/scripts/yolo11n.pt",verbose=False)
        self.FOV_X = FOV_X
        self.FOV_Y = FOV_Y

    def angles(self,mean_boxes, cls, img):
        angles = dict()
        for rowIndex in range(len(mean_boxes)):
            row = mean_boxes[rowIndex]
            angle = (((row[0]/img.shape[0])*self.FOV_X) - (self.FOV_X/2))
            if (angle<0):
                angle += 360
            if cls[rowIndex] not in angles:
                angles[cls[rowIndex]] = [angle]
            else:
                angles[cls[rowIndex]].append(angle)
        return angles

    def getAngles(self,img):
        (IMG_X,IMG_Y, Ch) = img.shape
        res = self.model(img)
        boxes = np.ceil(res[0].boxes.xyxy.cpu().numpy()).astype('int32')
        mean_boxes = (np.array([(boxes[:,0] + boxes[:,2])/2,(boxes[:,1] + boxes[:,3])/2],dtype=np.int32).T)
        cls = np.array(list(map(lambda x: self.model.names[x], (res[0].boxes.cls.cpu().numpy().astype(np.int8)))))
        for boxIndex in range(len(boxes)):
            box = boxes[boxIndex]
            cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(0,200,0),2)
            cv2.putText(img,cls[boxIndex],(box[0],box[1]+10),cv2.FONT_HERSHEY_PLAIN,2,(10,10,100),3)
        

        return img,self.angles(mean_boxes,cls,img)

model = IMGRec()

class Listener:
    def __init__(self,id):
        self.id = id
        self.path  = f"/robot{id}/camera/rgb/image_raw"
        self.pathPub  = f"/robot{id}/camera/rgb/image_processed"
        self.sub = rospy.Subscriber(self.path,Image,self.callback)
        self.pub = rospy.Publisher(self.pathPub,Image,queue_size=5)

    def callback(self,msg):
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        img, angle = model.getAngles(cv_image)
        image = bridge.cv2_to_imgmsg(img,encoding="bgr8")
        self.pub.publish(image)
        rospy.loginfo(angle)

if __name__=="__main__":
    rospy.init_node("yolo")
    for i in range(1,10):
        Listener(i)
    rospy.spin()




