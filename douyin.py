import win32api
import win32con
import win32gui
from ctypes import *
from pymouse import PyMouse
from time import sleep
import pyautogui as pag
import os
import time
import requests
import json
import shutil
import datetime
from PIL import Image


class POINT(Structure):
  _fields_ = [("x", c_ulong),("y", c_ulong)]
def get_mouse_point():
  po = POINT()
  windll.user32.GetCursorPos(byref(po))
  return int(po.x), int(po.y)
def mouse_click(x=None,y=None):
  if not x is None and not y is None:
    mouse_move(x,y)
    time.sleep(0.05)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
def mouse_dclick(x=None,y=None):
  if not x is None and not y is None:
    mouse_move(x,y)
    time.sleep(0.05)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0) 
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
def mouse_move(x,y):
  windll.user32.SetCursorPos(x, y)



class BaiduFaceIdentify():
    #此函数用于获取access_token，返回access_token的值
    #此函数被parse_face_pic调用
    def get_access_token(self):
        client_id = "xxxxxxxxxxxxxxxxxxxxxxxxxx"             #此变量赋值成自己API Key的值
        client_secret = "yyyyyyyyyyyyyyyyyyyyyyyyy"    #此变量赋值成自己Secret Key的值
        auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + client_id + "&client_secret=" + client_secret

        response_at = requests.get(auth_url)
        json_result = json.loads(response_at.text)
        access_token = json_result["access_token"]
        return access_token


      
    def imgdata(self,file1path):
        import base64
        f=open(r'%s' % file1path,'rb') 
        pic1=base64.b64encode(f.read()) 
        f.close()
        #将图片信息格式化为可提交信息，这里需要注意str参数设置，这里将图片信息转换为 base64 再提交
        #params = {"images":str(pic1,'utf-8')}
        return pic1


    #此函数进行人脸识别，返回识别到的人脸列表
    #此函数被parse_face_pic调用
    def identify_faces(self,url_pic,url_fi):
        headers = {
            "Content-Type" : "application/json; charset=UTF-8"
        }

        img_params =  self.imgdata(url_pic)
        
        post_data = {
            "image": img_params,
            "image_type" : "BASE64",
            "face_field" : "beauty,gender", #expression,faceshape,landmark,race,quality,glasses
            "max_face_num": 1
        }

        response_fi = requests.post(url_fi,headers=headers,data=post_data)
        json_fi_result = json.loads(response_fi.text)
        return json_fi_result["result"]
        #下边的print也许是最直观，你最想要的
        #print(json_fi_result[‘result‘][‘face_list‘][0][‘age‘])
        #print(json_fi_result[‘result‘][‘face_list‘][0][‘beauty‘])

    #此函数用于解析进行人脸图片，输出图片上的人脸的性别、年龄、颜值
    #此函数调用get_access_token、identify_faces
    def parse_face_pic(self,url_pic):
        #调用get_access_token获取access_token
        access_token = self.get_access_token()
        url_fi = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token=" + access_token
        #调用identify_faces，获取人脸列表
        json_faces = self.identify_faces(url_pic,url_fi)
        return json_faces
        

		
		
if __name__ == "__main__":
 
  while True:
    print('>>>> 调用程序时间：%s <<<<' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    mouse_dclick(1620, 687)
    pag.mouseDown(x=1620, y=790, button='left')
    pag.mouseUp(x=1620, y=300, button='left')
    print(">> 切换抖音用户视频页面成功")

    
    # 截图
    mouse_click(1881, 247)
    sleep(3)
    paths = "H:\myshares\Screenshots"
    for root, dirs, files in os.walk(paths):
          filename=files[0]
          print(">> 截图成功，截图文件名：%s，" % filename)
          file_dir = paths+"\\"+filename

    #file_dir="H:\myshares\Screenshots\Screenshot_2018-08-19-17-49-24.png

    # 分辨率整体缩小到原来的 0.3 ，可以加快上传速度
    to_scale = 0.3
    
    img = Image.open(file_dir)
    w,h = img.size
    tw = int(w * to_scale)
    th = int(h * to_scale)
    reImg = img.resize((tw,th),Image.ANTIALIAS)
    new_file_dir = file_dir + '.png'
    reImg.save( new_file_dir )
    print(">> 转换图片大小成功，正调用颜值API识别接口: %s" % file_dir)
    # 转换大小后删除原图
    os.remove(file_dir)

  


    url_pic =  new_file_dir
    bfi = BaiduFaceIdentify()
    results = bfi.parse_face_pic(url_pic)
    if results:
          print('返回结果: %s' % results )
          results_tmp=json.dumps(results)
          results=json.loads(results_tmp)
          beauty=results['face_list'][0]['beauty']
          sex=results['face_list'][0]['gender']['type']
          if sex == 'female':
              print('>> 识别到视频中是一女性，颜值评分为: %s' % beauty )
              if int(beauty) > 70:
                  mouse_click(1811, 481)
                  print('>> 认定为高颜值女性，已经关注了哟 ！！！！！！！！！！！！！！！！！！！！！')
                  shutil.move(new_file_dir,"H:\myshares\\bak-img")
              else:
                  os.remove(new_file_dir)
          else:
              print('>> 识别到视频中是一男性')
              os.remove(new_file_dir)
            
    else:
          print(">> 识别不到人脸，可能是侧脸或者画面没有人。复审路径: %s" % new_file_dir)
          os.remove(new_file_dir)

    print('\n')
    sleep(2)
        

"""
打印出当前鼠标所在位置
m = PyMouse()
print (m.position())
"""
