from tkinter import *
import math
import random
import time

root=Tk()
C=Canvas(root,width=1500,height=800,bg="#ffffff")
C.pack()

C.create_rectangle(0,700,1500,900,fill="#111111",outline="",tag="collider")
C.create_rectangle(0,600,600,900,fill="#111111",outline="",tag="collider")
C.create_rectangle(0,500,300,900,fill="#111111",outline="",tag="collider")
C.create_rectangle(900,600,1500,900,fill="#111111",outline="",tag="collider")
C.create_rectangle(1200,500,1500,900,fill="#111111",outline="",tag="collider")
C.create_rectangle(1495,0,1500,700,fill="#111111",outline="",tag="collider")
C.create_rectangle(0,0,5,900,fill="#111111",outline="",tag="collider")
"C.create_line(750,0,750,700)"
Dm={}
Dmc={}
Dp={}
Dpa={}
Dsh={}
Dex={}
Dca={}
"""Dm[C.create_rectangle(100-7,150-7,100+7,150+7,fill="#ff0000",tag="mcollider")]={"s":2,"d":[1,0]}"""

def lighten_color(color):
    color=color[1:7]
    cr=eval("0x"+color[0:2])
    cg=eval("0x"+color[2:4])
    cb=eval("0x"+color[4:6])
    cr=int(cr+((255-cr)/2))
    cg=int(cg+((255-cg)/2))
    cb=int(cb+((255-cb)/2))
    cr=str(hex(cr))[2:4]
    cg=str(hex(cg))[2:4]
    cb=str(hex(cb))[2:4]
    return("#"+cr+cg+cb)

def darken_color(color):
    color=color[1:7]
    cr=eval("0x"+color[0:2])
    cg=eval("0x"+color[2:4])
    cb=eval("0x"+color[4:6])
    cr=int(cr/2)
    cg=int(cg/2)
    cb=int(cb/2)
    cr=str(hex(cr))[2:4]
    cg=str(hex(cg))[2:4]
    cb=str(hex(cb))[2:4]
    while len(cr)<2:
        cr="0"+cr
    while len(cg)<2:
        cg="0"+cg
    while len(cb)<2:
        cb="0"+cb
    return("#"+cr+cg+cb)

def random_color():
    r=lambda:random.randint(0,255)
    return("#%02x%02x%02x"%(r(),r(),r()))

def random_color_1():
    return(random.choice(['#ff0000','#ff8000','#ffff00','#80ff00','#00aa00',
                          '#00ffff','#0000ff','#8000ff','#ff00ff','#808080']))

def random_balls(amount):
    for i in range(amount):
        rx=random.randint(20,980)
        ry=random.randint(10,150)
        rc=random_color()
        Dm[C.create_oval(rx-7,ry-7,rx+7,ry+7,fill=rc,tag="mcollider")]={"s":2,"d":[random.randint(-10,10),0]}

def particles(subj,color):
    Dp[subj]=color

def handle_particles():
    for i in Dp:
        particle((C.coords(i)[0]+C.coords(i)[2])/2,(C.coords(i)[1]+C.coords(i)[3])/2,Dp[i])

def particle(x,y,color):
    rx=random.randint(-3,+3)
    ry=random.randint(-3,+3)
    Dpa[C.create_oval(x+rx,y+ry,x+rx,y+ry,fill=color,outline=lighten_color(color))]={
        "age":0,
        "maxage":random.randint(3,6)}

def smoke(x,y,color):
    rx=random.randint(-3,+3)
    ry=random.randint(-3,+3)
    Dpa[C.create_oval(x+rx,y+ry,x+rx,y+ry,fill=color,outline=lighten_color(color))]={
        "age":0,
        "maxage":random.randint(10,20)}

def handle_particle():
    l=[]
    for i in Dpa:
        l.append(i)
        coords=C.coords(i)
        Dpa[i]["age"]+=1
        if Dpa[i]["age"]<Dpa[i]["maxage"]:
            C.coords(i,coords[0]-1,coords[1]-1,coords[2]+1,coords[3]+1)
        else:
            C.coords(i,coords[0]+1,coords[1]+1,coords[2]-1,coords[3]-1)
    for i in l:
        if Dpa[i]["age"]>=Dpa[i]["maxage"]*2:
            C.delete(i)
            del Dpa[i]

def handle_explosion():
    l=[]
    for i in Dex:
        l.append(i)
        coords=C.coords(i)
        Dex[i]["age"]+=4
        C.coords(i,coords[0]-4,coords[1]-4,coords[2]+4,coords[3]+4)
        for j in range(4):
            smoke(random.randint(int(coords[0]-4),int(coords[2]+4)),random.randint(int(coords[1]-4),int(coords[3]+4)),Dex[i]["color"])
    for i in l:
        if Dex[i]["age"]>=Dex[i]["maxage"]*4:
            C.delete(i)
            for j in range(20):
                smoke(random.randint(int(coords[0]-4),int(coords[2]+4)),random.randint(int(coords[1]-4),int(coords[3]+4)),"#888888")
            del Dex[i]

def explosion(x,y,color):
    for i in range(10):
        Dm[C.create_oval(x-2,y-2,x+2,y+2,fill="#555555",outline="#222222",tag="shrapnel")]={"s":2,"d":[random.randint(-5,5),random.randint(-5,5)]}
        Dp[C.find_all()[-1]]=color
        Dsh[C.find_all()[-1]]={
            "age":random.randint(50,200)}
        C.tag_lower(C.find_all()[-1])
    Dex[C.create_oval(x,y,x,y,fill="",outline="",tag="explosion")]={
        "age":0,
        "maxage":random.randint(8,11),
        "color":color}

def muzzle(x,y,fx,fy,color):
    for i in range(8):
        Dm[C.create_oval(x-2,y-2,x+2,y+2,fill="",outline="",tag="shrapnel")]={"s":2,"d":[fx+random.randint(-5,5)/5,fy+random.randint(-5,5)/5]}
        Dp[C.find_all()[-1]]=color
        Dsh[C.find_all()[-1]]={
            "age":random.randint(5,20)}
        C.tag_lower(C.find_all()[-1])

def handle_shrapnel():
    l=[]
    for i in Dsh:
        l.append(i)
    for i in l:
        Dsh[i]["age"]-=1
        if Dsh[i]["age"]<=0:
            try:
                del Dp[i]
            except:
                pass
            if Dsh[i]["age"]<=-80:
                del Dsh[i]
                C.delete(i)
                del Dm[i]

def random_explosion(amount):
    for i in range(amount):
        explosion(random.randint(20,980),random.randint(20,500),random_color_1())

def colliders():
    for i in C.find_withtag("collider"):
        C.create_line(C.coords(i)[0],C.coords(i)[1],C.coords(i)[2],C.coords(i)[1],fill="",tag="floor")
        C.create_line(C.coords(i)[2],C.coords(i)[1],C.coords(i)[2],C.coords(i)[3],fill="",tag="leftwall")
        C.create_line(C.coords(i)[0],C.coords(i)[3],C.coords(i)[2],C.coords(i)[3],fill="",tag="roof")
        C.create_line(C.coords(i)[0],C.coords(i)[1],C.coords(i)[0],C.coords(i)[3],fill="",tag="rightwall")
        C.create_rectangle(C.coords(i)[0]+2,C.coords(i)[1]+2,C.coords(i)[2]-2,C.coords(i)[3]-2,fill="",outline="",tag="antiglitch")

def mcolliders():
    for i in C.find_withtag("mcollider"):
        Dmc[i]["t"]=C.create_line(C.coords(i)[0],C.coords(i)[1],C.coords(i)[2],C.coords(i)[1],fill="",tag=("floor","mc"))
        Dmc[i]["r"]=C.create_line(C.coords(i)[2],C.coords(i)[1],C.coords(i)[2],C.coords(i)[3],fill="",tag=("leftwall","mc"))
        Dmc[i]["l"]=C.create_line(C.coords(i)[0],C.coords(i)[3],C.coords(i)[2],C.coords(i)[3],fill="",tag=("roof","mc"))
        Dmc[i]["b"]=C.create_line(C.coords(i)[0],C.coords(i)[1],C.coords(i)[0],C.coords(i)[3],fill="",tag=("rightwall","mc"))

def delmc():
    for i in C.find_withtag("mc"):
        C.delete(i)

def gravity():
    for i in Dm:
        l=list(set(C.find_overlapping(*C.coords(i))).intersection(C.find_withtag("floor")))
        if not i in C.find_withtag("shrapnel"):
            if Dmc[i]["t"] in l:
                l.remove(Dmc[i]["t"])
        if not l:
            Dm[i]["d"][1]+=0.05
        Dm[i]["d"][0]/=1.002

def idle():
    for i in Dm:
        C.move(i,Dm[i]["d"][0]*Dm[i]["s"],Dm[i]["d"][1]*Dm[i]["s"])

def canon(x,y):
    Dca[C.create_oval(x-30,y-30,x+30,y+30,fill="#555555",tag="canon")]={}

def handle_canons():
    for i in Dca:
        x=C.coords(i)[0]+30
        y=C.coords(i)[1]+30
        C.create_line(x,y,
                      x+(cx-x)/math.sqrt((cx-x)**2+(cy-y)**2)*50,
                      y+(cy-y)/math.sqrt((cy-y)**2+(cx-x)**2)*50,
                      tag="barrel",width=30,fill="#555555")
        C.tag_raise(i)

def canon_fire(event):
    for i in Dca:
        x=C.coords(i)[0]+30
        y=C.coords(i)[1]+30
        rc=random_color()
        Dm[C.create_oval(x-7,y-7,x+7,y+7,fill=rc,tag="mcollider")]={"s":2,"d":[(cx-x)/math.sqrt((cx-x)**2+(cy-y)**2)*8,(cy-y)/math.sqrt((cy-y)**2+(cx-x)**2)*8]}
        muzzle(x,y,(cx-x)/math.sqrt((cx-x)**2+(cy-y)**2)*5,(cy-y)/math.sqrt((cy-y)**2+(cx-x)**2)*5,rc)
    for i in C.find_withtag("barrel"):
        C.tag_raise(i)
    for i in C.find_withtag("canon"):
        C.tag_raise(i)

def delca():
    for i in C.find_withtag("barrel"):
        C.delete(i)

def handle_colliders():
    L=[]
    for i in Dm:
        L.append(i)
    for i in L:
        lf=list(set(C.find_overlapping(*C.coords(i))).intersection(C.find_withtag("floor")))
        if not i in C.find_withtag("shrapnel"):
            if Dmc[i]["t"] in lf:
                lf.remove(Dmc[i]["t"])
            if Dmc[i]["r"] in lf:
                lf.remove(Dmc[i]["r"])
            if Dmc[i]["l"] in lf:
                lf.remove(Dmc[i]["l"])
            if Dmc[i]["b"] in lf:
                lf.remove(Dmc[i]["b"])
        lr=list(set(C.find_overlapping(*C.coords(i))).intersection(C.find_withtag("roof")))
        if not i in C.find_withtag("shrapnel"):
            if Dmc[i]["t"] in lr:
                lr.remove(Dmc[i]["t"])
            if Dmc[i]["r"] in lr:
                lr.remove(Dmc[i]["r"])
            if Dmc[i]["l"] in lr:
                lr.remove(Dmc[i]["l"])
            if Dmc[i]["b"] in lr:
                lr.remove(Dmc[i]["b"])
        lrw=list(set(C.find_overlapping(*C.coords(i))).intersection(C.find_withtag("rightwall")))
        if not i in C.find_withtag("shrapnel"):
            if Dmc[i]["t"] in lrw:
                lrw.remove(Dmc[i]["t"])
            if Dmc[i]["r"] in lrw:
                lrw.remove(Dmc[i]["r"])
            if Dmc[i]["l"] in lrw:
                lrw.remove(Dmc[i]["l"])
            if Dmc[i]["b"] in lrw:
                lrw.remove(Dmc[i]["b"])
        llw=list(set(C.find_overlapping(*C.coords(i))).intersection(C.find_withtag("leftwall")))
        if not i in C.find_withtag("shrapnel"):
            if Dmc[i]["t"] in llw:
                llw.remove(Dmc[i]["t"])
            if Dmc[i]["r"] in llw:
                llw.remove(Dmc[i]["r"])
            if Dmc[i]["l"] in llw:
                llw.remove(Dmc[i]["l"])
            if Dmc[i]["b"] in llw:
                llw.remove(Dmc[i]["b"])
        if lf and Dm[i]["d"][1]>=0:
            if ((math.sqrt(Dm[i]["d"][0]**2+Dm[i]["d"][1]**2)>=4.5 and False)or(math.sqrt(Dm[i]["d"][0]**2+Dm[i]["d"][1]**2)>=6.5))and not i in C.find_withtag("shrapnel"):
                explosion(C.coords(i)[0]+7,C.coords(i)[1]+7,C.itemcget(i,"fill"))
                del Dm[i]
                C.delete(i)
            else:
                Dm[i]["d"][1]=-Dm[i]["d"][1]/2
        elif lr and Dm[i]["d"][1]<0:
            if ((math.sqrt(Dm[i]["d"][0]**2+Dm[i]["d"][1]**2)>=4.5 and False)or(math.sqrt(Dm[i]["d"][0]**2+Dm[i]["d"][1]**2)>=6.5))and not i in C.find_withtag("shrapnel"):
                explosion(C.coords(i)[0]+7,C.coords(i)[1]+7,C.itemcget(i,"fill"))
                del Dm[i]
                C.delete(i)
            else:
                Dm[i]["d"][1]=-Dm[i]["d"][1]/2
        elif lrw and Dm[i]["d"][0]>0:
            if ((math.sqrt(Dm[i]["d"][0]**2+Dm[i]["d"][1]**2)>=4.5 and False)or(math.sqrt(Dm[i]["d"][0]**2+Dm[i]["d"][1]**2)>=6.5))and not i in C.find_withtag("shrapnel"):
                explosion(C.coords(i)[0]+7,C.coords(i)[1]+7,C.itemcget(i,"fill"))
                del Dm[i]
                C.delete(i)
            else:
                Dm[i]["d"][0]=-Dm[i]["d"][0]/2
        elif llw and Dm[i]["d"][0]<0:
            if ((math.sqrt(Dm[i]["d"][0]**2+Dm[i]["d"][1]**2)>=4.5 and False)or(math.sqrt(Dm[i]["d"][0]**2+Dm[i]["d"][1]**2)>=6.5))and not i in C.find_withtag("shrapnel"):
                explosion(C.coords(i)[0]+7,C.coords(i)[1]+7,C.itemcget(i,"fill"))
                del Dm[i]
                C.delete(i)
            else:
                Dm[i]["d"][0]=-Dm[i]["d"][0]/2

def dmc():
    for i in Dm:
        if not i in Dmc and not i in C.find_withtag("shrapnel"):
            Dmc[i]={}

def handle_colliderglitch():
    for i in C.find_withtag("shrapnel"):
        if set(C.find_overlapping(*C.coords(i))).intersection(C.find_withtag("antiglitch")):
            try:
                del Dp[i]
            except:
                pass

def fire_player(event):
    1

Dm[C.create_oval(750-7,400-7,750+7,400+7,fill="#4000ff",tag=("mcollider","player"))]={"s":2,"d":[0,0]}

root.bind("<Button-1>",canon_fire)
random_balls(5)
#canon(200,470)
#canon(1300,470)
"""for i in range(5):
    canon(random.randint(30,1470),random.randint(30,470))"""
colliders()
while 1:
    time.sleep(0.001)
    cx=C.winfo_pointerxy()[0]
    cy=C.winfo_pointerxy()[1]
    """if not random.randint(0,50):
        random_explosion(1)"""
    dmc()
    handle_canons()
    handle_shrapnel()
    handle_colliderglitch()
    handle_explosion()
    handle_particles()
    handle_particle()
    mcolliders()
    gravity()
    idle()
    handle_colliders()
    delmc()
    C.update()
    delca()
