'''

小武酷跑 简易封装 文件
BackGround() : 传入窗口对象
 move_speed: 移动速度
.is_change=False :是否交替
.load() 加载背景图片
.update() 显示到屏幕
.update (是否交替,移动速度)


Role(self,image, x, y, action=False, rate=5):  管理 角色更好地 类
创建对象实例化
.x 当前的x坐标
.y 当前角色的 y 坐标
.action  bool 值 用来判断是否是动图 如果是一组图 需要设置为True
.rate 图片切换的速率

# 一些方法
update() 方法   更新下一个动作图片
get_pos() 方法  获取当前角色的x，y坐标 返回值为 [] 列表
set_speed() 方法 设置角色的移动速度  参数为speed
get_speed() 方法 获取角色当前的移动速度
setAlive() 方法 bool值 设置角色是否活着 参数为bool值
getAlive() 方法 bool值 获取角色是否活着
move(face="left") 方法  移动角色  参数   朝某个方向移动  up down left right
setJumpHeight(self, speed=5)方法 设置角色的跳跃高度’ 参数为角色的跳跃高度 正数
jump(floor = floor)方法 让角色调整为跳跃状态 是用之前需要设置跳跃高度  参数为初始起跳的高度
distance(self, pos, center_d2=5) 当前角色和 角色2之间的距离 参数 角色2的pos元组坐标 角色2 坐标到图中心的平均值 默认为5


坐标到图中心的平均值计算方法
平均值  = (角色2 的宽除以 2 + 角色2 的高除以2) // 2

# 给角色赋予新的能力
setMyDefine(self, **kwargs):  当角色已有的属性不被满足时可以自己添加键值对的形式添加
getMyDefine(self, key) 获取自己设定属性的值
example：
    # 设置得分= 5
    Role.setMyDefine(point = 5)
    point = Role.getMyDefine("point")

'''

import pygame
from .exception import *
import math


class BackGround():
    def __init__(self, screen):
        '''

        :param screen: 窗口对象  Surface
        '''
        # if
        self.screen = screen
        self.image = None
        self.image2 = None

        self.is_change = False
        self.is_vertical = False
        self.moveSpeed = 0
        #
        self.img_width = None
        self.image1x = 0
        self.image2x = 0
        self.image1y = 0
        self.image2y = 0

        self.img_width = None

    def load_image(self, *args):
        if len(args) == 1:
            try:
                image = pygame.image.load(args[0])
                self.image = image
                self.image2 = self.image
                self.rect = image.get_rect()
                self.img_width = self.rect[2]
                self.image2x = self.rect[2]
            except:
                e = BackGround_Error("错误的图片加载路径或者这不是一张图片")
                raise e
        else:
            e = BackGround_Error("图片必须至少有一张最多两张")
            raise e

    def update(self, is_change=False, move_speed=1, vertical=False):
        self.is_change = is_change
        self.is_vertical = vertical
        self.moveSpeed = move_speed
        if self.is_change:
            if self.is_vertical:
                # 竖着
                pass
            else:
                # 横着
                self.image1x = self.image1x - self.moveSpeed
                self.image2x = self.image2x - self.moveSpeed
                if self.image1x <= -self.img_width:
                    self.image1x = self.img_width
                if self.image2x <= -self.img_width:
                    self.image2x = self.img_width
                self.screen.blit(self.image, (self.image1x, self.image1y))
                self.screen.blit(self.image2, (self.image2x, self.image2y))
        if not self.is_change:
            self.screen.blit(self.image, (self.image1x, self.image1y))


class Action():
    action = {}
    '''
    Action(): 人物 动作类
. getImages(self, images, rate)    加载图片对象Surface列表初始化动作类    参数：images 图像列表  rate 越大 速度越慢
. image_next(self): 获取下一个人物的动作

. set_jump(self, speed)        设置跳跃高度 不是像素而是内部简单的算法 数值越高 跳跃的越高
. jump(self, pos, floor)     获取跳跃时的坐标返回一个 坐标列表  pos 当前的坐标  floor ：开始跳跃的高度
. set_speed(self, speed)     设置人物移动的速度       参数 speed 移动速度
. move(self, pos, face="left")  移动角色  参数  pos坐标想 x,y 的值 朝某个方向移动  up down left right


Action.distance(pos1, pos2, distance1_center=5,distance2_center=5 ) 检测两个角色之间的距离 需要参数 角色1 的坐标，角色2的坐标
可选参数 角色1 图片左上角到圆心的距离  默认为5
可选参数 角色2 图片左上角到圆心的距离  默认为5
    '''

    def __init__(self):
        pass

        # 未设置前为空
        self.blood = None

        self.image = None
        self.images = None

        self.long = None
        self.select = 0
        self.flag = 0
        self.rate = 0
        # 跳跃
        self.height = 0
        self.speed_up_flag = 0

        # 移动
        self.speed = 0

        # role 属性
        self.rolex = None
        self.roley = None
        self.roleImage = None
        self.rolewidth = None
        self.roleheight = None
        self.__is_alive = None

    def getImages(self, images, rate):
        self.images = images
        self.long = len(images)
        self.rate = rate
        pass

    def set_attribute(self, blood):
        pass

    def image_next(self):
        self.image = self.images[self.select]

        self.flag += 1
        if self.flag >= self.rate:
            self.select += 1
            self.flag = 0
            if self.select >= self.long - 1:
                self.select = 0

        return self.image

    #   跳跃动作
    def set_jump(self, speed):
        self.speed_up_flag = -speed
        self.speed_up = self.speed_up_flag

    def jump(self, pos, floor):
        x = pos[0]
        y = pos[1]
        try:
            if self.speed_up < 0:
                pass
        except:
            Action_Error("没有给角色设置起跳高度")
        if self.speed_up < 0:
            self.speed_up += 0.6
        elif self.speed_up > 0:
            self.speed_up += 0.9
        y += self.speed_up
        if y > floor:
            y = floor
            self.speed_up = self.speed_up_flag

        pos = [x, y]
        return pos

    def set_speed(self, speed):
        self.speed = speed

    def move(self, pos, face="left"):
        x = pos[0]
        y = pos[1]
        if face == "left":
            x -= self.speed
            return [x, y]
        if face == "right":
            x += self.speed
            return [x, y]

        if face == "up":
            y -= self.speed
            return [x, y]
        if face == "down":
            y += self.speed
            return [x, y]

    def mange_role(self, x, y, img):
        self.rolex = x
        self.roley = y
        self.roleImage = img

    def setAlive(self, value):
        if type(value) == bool:
            # print("设置生命成功")
            self.__is_alive = value

    def getAlive(self):

        return self.__is_alive

    @staticmethod
    def distance(pos1, pos2, distance1_center=5, distance2_center=5):
        x1 = pos1[0] + distance1_center
        y1 = pos1[1] + distance1_center
        x2 = pos2[0] + distance2_center
        y2 = pos2[1] + distance2_center

        a = x1 - x2
        b = y1 - y2

        return math.sqrt(a * a + b * b)


class Role():
    def __init__(self, image, x, y, action=False, rate=5):
        self.rate = rate
        self.image = image
        if action == True:
            self.a = Action()
            self.a.getImages(image, self.rate)
        self.x = x
        self.y = y
        self.__is_alive = True
        self.__blood = 0
        self.__speed = 5
        self.mydict = {}

    def setBlood(self, blood):
        if type(blood) != int:
            raise Role_Error("设置的血量必须为int类型")
        self.__blood = blood

    def getBlood(self):
        return self.__blood

    def update(self):
        self.image = self.a.image_next()

    def get_pos(self):
        return [self.x, self.y]

    def setSpeed(self, speed):
        self.__speed = speed

    def getSpeed(self):
        return self.__speed

    def setAlive(self, value):
        if type(value) == bool:
            # print("设置生命成功")
            self.__is_alive = value

    def getAlive(self):
        return self.__is_alive

    def move(self, face="left"):
        faces = ["down", "up", "right", "left"]
        if face not in faces:
            raise Role_Error("必须输入一个正确的方向{}".format(faces))

        if face == "left":
            self.x -= self.__speed
        if face == "right":
            self.x += self.__speed

        if face == "up":
            self.y -= self.__speed
        if face == "down":
            self.y += self.__speed

    def setJumpHeight(self, speed=5):
        if type(speed) != int or speed < 0:
            raise Role_Error("速度必须是int类型的正数")
        self.a.set_jump(speed=speed)

    def jump(self, floor):
        try:
            if self.a.speed_up < 0:
                pass
            self.x, self.y = self.a.jump([self.x, self.y], floor=floor)
        except:
            raise Action_Error("没有给角色设置起跳高度,需要使用 setJumpHeight() 方法设定")

    def kill(self):
        self.x = -1000
        self.y = -1000
        del self

    def distance(self, pos, center_d2=5):
        try:
            x, y = pos[0], pos[1]
        except:
            raise Action_Error("被检测碰撞元素的坐标不是期望的类型 我们想要[x,y]的坐标格式")
        pos = (x, y)
        xx, yy, width, height = self.image.get_rect()
        center_d = (width // 2) + (height // 2) // 2
        value = Action.distance(self.get_pos(), pos, center_d, center_d2)
        # print(value)
        return value

    def setMyDefine(self, **kwargs):
        self.mydict = kwargs

    def getMyDefine(self, key):
        if key in self.mydict:
            return self.mydict[key]
        if key not in self.mydict:
            return None
