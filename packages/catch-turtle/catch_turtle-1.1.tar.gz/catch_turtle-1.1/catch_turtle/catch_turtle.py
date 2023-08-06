﻿"catch_turtle游戏主模块。"
import time,os,sys
from turtle import *
from random import randrange
try:import button,turtles
except ImportError:
    import catch_turtle.button as button
    import catch_turtle.turtles as turtles

CFGFILENAME="cfg.cfg"
CFGFILEPATHS=sys.path[1]+"\\"+CFGFILENAME,CFGFILENAME
HELPFILE="README.txt"

os.chdir(os.path.split(__file__)[0])

class Enemy(Turtle):
    "游戏中敌人的类"
    def __init__(self):
        #初始化
        super().__init__()
        self.shape("turtle")
        self.shapesize(2)
        self.fillcolor("red")
        self.pu()
    def startgame(self):self.run(go=False)
    def run(self,go=True):
        speed=CFG['l']+25
        turtles.move(self,speed,go)#移动自身
        if turtles.catches(self,p,l=25):
            return "FAIL"

class Player(Turtle):
    "游戏中玩家的类"
    def __init__(self,color="green"):
        super().__init__()
        super().shape("turtle")
        super().fillcolor(color)
        super().pu()
    def startgame(self):
        '"玩家"进入游戏状态'
        self.goto(0,60)#游戏开始时,移动海龟至初始位置
        turtles.bind(scr,self,CFG["ps"])
    def win(self):
        "判断玩家是否已赢"
        won=turtles.catches(self,c)
        if won:self.ani()
        return won
    def ani(self):
        "加分时显示动画"
        goto(self.xcor(),self.ycor())
        color("red")
        write("+10",font=("黑体",20))
        time.sleep(0.4)
        undo()
        

class ClonedPlayer(Player):
    "游戏中玩家的分身"
    def __init__(self):
        super().__init__(color="green3")
        self.startgame()
    def startgame(self):
        self.showturtle()
        self.move()
    def move(self):
        #x,y:分身与主玩家的相对位置
        dis=CFG["dc"]
        self.x=randrange(-dis,dis)
        self.y=randrange(-dis,dis)
        self.run()
    def run(self):
        '使"玩家"的分身跟着主玩家走'
        self.setheading(p.heading())
        self.goto(p.xcor()+self.x,p.ycor()+self.y)

class ScoreBoard():
    "一个记分板,用于显示分数"
    def __init__(self):
        self.fontsize=15
        self.score=0
        self.show(self.score)
    def __ready(self,score):
        "使海龟移动到记分板处,准备记录分数"
        undo()#清除前一次绘制的文本
        pu()
        goto(window_width()/2-self.fontsize*7,window_height()/2-self.fontsize*6)
        color("black")
    def show(self,score):
        self.__ready(score)
        text="分数 "+str(score)+"\n最高分 "+str(CFG["s"])+"\n等级 "+str(CFG["l"])
        write(text,align="left",font=("黑体",self.fontsize))
        self.score=score
        delay(0)

class Config(dict):
##    配置字典释义
##    e:敌人数量
##    cs:被追逐者移动速度
##    ps:玩家移动速度
##    dc:玩家分身与玩家的最大距离
##    a:是否在游戏主页中显示动画
##    s:历史最高分
##    l:玩家等级
##    spl:scores_per_level:每升一级所需分数
    def __init__(self,filename):
        self.cfgfile=open(filename)
    def read(self):
        "读取游戏配置文件"
        super().__init__()
        while True:
            text=self.cfgfile.readline().split(":")
            if not text[0]:break
            if len(text)>1:self[text[0]]=eval(text[1])
    def write(self):
        self.cfgfile=open(CFGFILENAME,'w')
        for key in self.keys():
            self.cfgfile.write("{}:{}\n".format(key,bin(self[key])))
    def close(self):
        self.cfgfile.close()

class GameError(FileNotFoundError):
    "一个异常类,在游戏发生错误(如找不到配置文件时),会被raise"
    pass

#------------------------------一些有用的函数-----------------------------------
def createturtles(num,_class):
    "出现一些游戏角色,个数为num。"
    t=[None]*num
    delay(1)#使游戏角色慢速出场
    for n in range(num):
        t[n]=_class()
        t[n].startgame()
        if n>1:delay(0)#出现第一个角色后,加快角色出场速度
    return t

def draw_button(again_text):
    "在暂停游戏(如失败或成功时),绘制出两个按钮"
    def onclick(x,y):
        if buttons[0].inarea(x,y):#如果单击了重来按钮
            reset()
            _main(create=False)
        if buttons[1].inarea(x,y):#如果单击了返回按钮
            reset()
            start(init=False)
    
    text=[again_text,"返回主页"]
    setheading(0)
    goto(-50,0)
    for n in range(2):
        buttons[n]=button.Button()
        buttons[n].color1=[180]*3
        buttons[n].color2=[140]*3
        buttons[n].text=text[n]
        buttons[n].font="华文行楷"
        buttons[n].fontsize=20
        buttons[n].draw()
        fd(40)
        lt(90)
    scr.onclick(onclick)
    return buttons

def reset():
    if players:#如果有分身
        for player in players:
            player.hideturtle()
    turtles.reset()

#----------------------------游戏主代码由此开始---------------------------------

#读取配置文件
CFG=None
for filename in CFGFILEPATHS:
    if os.path.isfile(filename):
        CFG=Config(filename)
        CFG.read()
#找不到文件时引发异常
if not CFG:
    raise GameError(
        "找不到配置文件 %r。Could not find the config file."% CFGFILENAME)

def start(init=True):
    """游戏开始界面
    init:是否初始化海龟实例"""
    #p:玩家 c:被追逐的海龟
    def __init__():
        "初始化两个新的海龟"
        global p,c,scr
        scr=Screen()
        scr.title("追逐海龟")
        # p:玩家
        # c:被追逐的海龟
        p=Player()
        c=Turtle()
        c.shape("turtle")
        c.fillcolor("yellow")
        c.pu()
    
    def onclick(x,y):
        "屏幕被单击时,判断用户单击的是哪个按钮"
        global buttons
        nonlocal ani
        ani=False
        if x>buttons[0].llx and x<buttons[0].urx:
            h=buttons[0].h
            if y<0 and y>-h:#如果是开始按钮
                global players
                players=None
                p.clearstamps()#清除复制的海龟形状
                _main()
            elif y<-2*h and y>-3*h:#如果是说明按钮
                p.clearstamps()
                info()
            elif y<-4*h and y>-5*h:#如果是退出按钮
                print("bye!")
                scr.bye()

    global buttons,scr,score,lv,clo
    
    #初始化
    if init:__init__()
    scr.onclick(None)
    scr.delay(0)
    scr.bgcolor("#A688EC")#粉色
    if scr.bgpic()!='nopic':scr.bgpic('nopic')#清除屏幕的背景图像
    pu()
    ht()
    goto(-60,150)
    write("追逐海龟",align="left",font=("华文新魏",30))#绘制文字
    #在"龟"字处拷贝海龟的形状
    p.goto(80,170)
    p.setheading(90)
    p.shapesize(0.9)
    p.stamp()
    p.shapesize(1)
    
    goto(-50,0)
    setheading(0)
    tracer(5,0)
    #依次绘制出三个按钮
    buttons=[None]*3
    text=["开始游戏","游戏说明","退出"]
    for n in range(3):
        buttons[n]=button.Button()
        buttons[n].color1=180,180,220
        buttons[n].color2=140,140,200
        buttons[n].text=text[n]
        buttons[n].font="华文行楷"
        buttons[n].fontsize=20
        buttons[n].draw()
        fd(40)
        lt(90)
    scr.onclick(onclick)

    score=0
    p.goto(0,80)
    c.goto(0,80)
    tracer(1,5)
    if CFG["a"]:
        ani=True
        try:
            for n in range(100):
                if not ani:break
                turtles.moveturtles(p,c,False)#移动海龟
        except Terminator:return

def info():
    "显示游戏说明"
    def point_at(turtle,lineto,description):
        "用线指着某个海龟"
        goto(turtle.xcor(),turtle.ycor())
        pd()
        goto(lineto[0],lineto[1])
        pu()
        write(description,True,align="left",font="微软雅黑")
    def _back():
        "返回到游戏主页"
        turtles._undo()
        turtles.stop()#再次使海龟能移动
        try:
            otherplayer.hideturtle()#隐藏玩家分身
            e.hideturtle()
        except:pass
        start(init=False)
    def onclick(x=0,y=0):
        if back.inarea(x,y):#如果单击了返回按钮
            _back()
            
    global p,c,scr
    scr.onclick(None)
    scr.bgcolor("white")
    delay(0)
    turtles.stop()#使海龟停止移动
    turtles._undo(2)
    try:f=open(HELPFILE)  #打开文件
    except:#找不到文件时提示消息
        from tkinter import messagebox as msgbox
        msgbox.showinfo("错误","找不到游戏帮助文件")
        _back()
    goto(-280,-150)
    write(f.read(),True,font=("微软雅黑",14))#读取文件,并显示文件内容
    
    #玩家
    p.goto(20,200)
    point_at(p,(200,150),"玩家")#指出"玩家"
    #被追逐者
    c.goto(150,18)
    point_at(c,(230,40),"被追逐者")
    #敌人
    e=Enemy()
    e.goto(-30,20)
    point_at(e,(40,60),"敌人")
    #玩家分身
    otherplayer=ClonedPlayer()
    otherplayer.goto(0,120)
    point_at(otherplayer,(180,100),"玩家分身")
    #绘制返回按钮
    goto(-50,-215)
    setheading(0)
    back=button.Button()
    back.color1=[180]*3
    back.color2=[140]*3
    back.text="返回"
    back.font="华文新魏"
    back.fontsize=20
    back.draw()
    scr.onclick(onclick)
    
def _main(create=True):
    "游戏主程序"
    def setscore():
        "追到海龟后设置分数、等级"
        global score,running
        score+=10
        if CFG["s"]<score:
            CFG["s"]=score
        if score % CFG["spl"]==0:
            CFG["l"]+=1
            CFG.write()
            running=False
            win()
        else:
            #使被追逐者移回原位,开始下一次追逐
            c.home()
    def run():
        global score
        for n in range(CFG["e"]):
            if enemies[n].run() == "FAIL": #使敌人"活动"
                fail()
                return "FAIL"
        turtles.move(c,CFG["cs"])
        if p.win():
            setscore()
            return "WIN"
        if players: #如果有分身
            for player in players:
                player.run()
                if player.win():
                    setscore()
                    return "WIN"
                    
        board.show(score)#显示分数
    
    global scr,running,board,enemies,players,app_path
    turtles._undo(2)
    scr.bgcolor("black")
    try:
        app_path=os.path.split(__file__)[0]#获取程序路径
        scr.bgpic(app_path+"/图片/草地.gif")#加载图片
    except:pass#忽略错误
    
    goto(-50,-150)
    write("Ready",align="left",font=("微软雅黑",30))#绘制文字Ready
    c.home()
    scr.onclick(None)#清除单击事件绑定
    if create:
        enemies=createturtles(CFG["e"],Enemy)#创建敌人
        if CFG["l"]>2:#判断玩家是否有足够等级
            players=createturtles(abs(CFG["l"]-2),ClonedPlayer)#创建玩家分身
    else:
        for enemy in enemies:
            enemy.showturtle()
        if players:
            for player in players:
                player.startgame()
    delay(0)
    undo()
    fd(20)
    write("Go!",align="left",font=("微软雅黑",30))#绘制文字Go
    p.startgame()
    time.sleep(0.15)
    undo()
    board=ScoreBoard()
    running=True
    
    while True:
        try:
            result = run()
            if result == "FAIL" or result == "WIN":
                break
        finally:
            CFG.close()#出现错误时关闭配置文件
    
    #游戏结束时,重置所有敌人
    for enemy in enemies:
        enemy.home()
        enemy.hideturtle()

def fail():
    "游戏失败时调用该函数。"
    global board,score,scr
    scr.onclick(None)
    scr.bgpic(app_path+"\图片\草地2.gif")
    score=0#失败后分数清零
    board.show(score)
    pu()
    goto(-80,150)
    color("black")
    write("Game Over!",True,align="left",font=("微软雅黑",36))#绘制文字
    goto(-50,0)
    #绘制出两个按钮
    draw_button("再来一次")

def win():
    "游戏成功时"
    global board,score,scr
    try:
        scr.onclick(None)
        scr.bgpic(app_path+"\图片\草地2.gif")
    except:pass
    board.show(score)
    pu()
    color("red")
    if CFG["l"]>2:
        goto(-250,150)
        text="胜利,恭喜进入{}级,增加1个分身!".format(CFG["l"])
    else:
        goto(-120,150)
        text="胜利,恭喜进入{}级!".format(CFG["l"])
    write(text,True,align="left",font=("隶书",30))#绘制文字
    color("black")
    draw_button("继续游戏")

if __name__=="__main__":
    start()
    mainloop()
