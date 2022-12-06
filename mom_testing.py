from calc3 import *
import math,pygame,time,random
import numpy as np
from numba import vectorize,float64,int64,uint8,guvectorize,uint32


pygame.font.init()
global myfont
myfont = pygame.font.SysFont('Sans Sherif', 50)
clock = pygame.time.Clock()
width=1500
height=1124
print('Resolution : '+str(width)+ " " + str(height))
sca=1
screen = pygame.display.set_mode((width*sca,height*sca))
clock = pygame.time.Clock()
update,done=1,False

def v(a):
    return np.array(a,dtype=np.float64)

def tex(st,h,w=0):
    textsurface = myfont.render(str(st), True, (0, 0, 0))
    screen.blit(textsurface,(w,h))

start = 0
end = 25
dx = 0.1
graphx = np.arange(0,end+dx,dx,dtype=np.float64)

scale =10
xscale = width/scale/np.max(graphx)

dt = -graphx[0]+graphx[1]
print(xscale)




########HW
concentrated_loads = [[9,-20]]#xlocation,strength
distributed_loads = [[0,25,-3.2]] #xstart,xend,strenght/meter
t_loads = [] #a1,a2 b, w0

moments = [] #start, lb/m





#concentrated_loads = []


#discontinuity funcs



DF = [
    
        
    ]
#w0, a, pow ,b=1
#as in: factor, xloc, ^power
DF.append([ 41.0 , 0 , 0])
DF.append([ 59.0 , 20 , 0])
#DF.append([ 19.0 , 0 , 0])
#DF.append([ 41.000000000000014 , 20 , 0])
for t in t_loads:
    DF.append([t[3],t[0],2,t[2]])
    DF.append([-t[3],t[1],2,t[2]])
    DF.append([-t[3],t[1],1])

for l in concentrated_loads:
    DF.append([l[1],l[0],0])

for l in distributed_loads:
    DF.append([l[2],l[0],1])
    DF.append([-l[2],l[1],1])

for m in moments:
    DF.append([m[1],m[0],-1])

print("Discontinuity function",DF)


def integral_factor(x):
    i = 1
    f = 1
    while i<=x:
        f*=i
        i+=1
    return f

def DiscFunc(x,f,integ,pr=False):
    ins = x > f[1]
    resultzero=False
    if (f[2]+integ)<0:
        resultzero=True
        #return x[ins]*0
    b=1
    if len(f)>3:
        b = f[3]
    IF = integral_factor(f[2]+integ)
    
    if pr:
        print('w',f[0]/b/IF,'*(x-',f[1],')^',(f[2]+integ))
    if resultzero:
        return x[ins]*0
    return f[0]/b/IF*(x[ins]-f[1])**(f[2]+integ)

def fW(x):
    res = x*0
    for f in DF:
        
        ins = x > f[1]
        #print("W ",'at x=',f[1],'  ',f[1])
        res[ins] += DiscFunc(x,f,-1,True)
        
    return res

def fV(x):
    res = x*0
    for f in DF:
        
        ins = x > f[1]
        res[ins] += DiscFunc(x,f,0)
        
    return res
    
def fM(x,mode = 0):
    
    res = x*0
    for f in DF:
        ins = x > f[1]
        res[ins] += DiscFunc(x,f,1)
    
    return res
class Constants:
    def __init__(self):
        self.Dis = 0
        self.Dis2 = 0
C = Constants()
C.Dis = 0.
C.Dis2 = 0.


def fDD(x):
    
    res = x*0+C.Dis
    for f in DF:
        ins = x > f[1]
        res[ins] += DiscFunc(x,f,2)
    #res = inte(0,x,fM,dt)+Dis
    return(res)
    
def fD(x):
    res = x*0+C.Dis*x+C.Dis2
    for f in DF:
        ins = x > f[1]
        res[ins] += DiscFunc(x,f,3)
    return(res)


################set deflection at zero at point using deflection derivative function#########
# test1 = np.array([0])
# test2 = np.array([4])
# print('Deflection at ',test1,'is',fD(test1))
# print('Deflection at ',test2,'is',fD(test2))

# while fD(test1) < fD(test2):
#     Dis-=1
#     print(Dis,fD(test1),fD(test2))

# print('Deflection at ',test1,'is',fD(test1))
# print('Deflection at ',test2,'is',fD(test2))
    
# #Dis2 = -fD(test1)
# def f2(x):
#     return inte(0,x,fM,dt)

# print('the Constant added to the deflection angle was ',Dis)
# print('Deflection at ',test1,'is',fD(test1))
# print('Deflection at ',test2,'is',fD(test2))
# print('the Constant added to deflection was ',Dis2)
    
arrow = vec([
    [0,0],
    [1,1],
    [.5,1],
    [.5,2],
    [-.5,2],
    [-.5,1],
    [-1,1],
    [0,0],
    ])/4
arrow2 = np.roll(vec([
    [.20,0],
    [1,1],
    [.5,1],
    [.5,2],
    [.5,2.6],
    [0,2],
    [-.5,1],
    [-1,1],
    [.2,0],
    ])/4,1,1)*vec2(.7,.3)+vec2(-.2,-.15)

def drawbeam():
    h= 100
    pygame.draw.lines(screen,(0,0,0),False,vec([[0,0],[width,0]])+vec2(0,h),2)
    global myfont
    myfont = pygame.font.SysFont('Sans Sherif', 25)
    for l in concentrated_loads:
        pygame.draw.lines(screen,(0,0,0),False,2*arrow*scale*l[1]+vec2(l[0]*xscale*scale,h),2)
        if l[0]*xscale*scale<width-100:
        
            tex(str(l[1])+'lb',h,l[0]*xscale*scale)
        else:
            tex(str(l[1])+'lb',h,l[0]*xscale*scale-60)
    for l in distributed_loads:
        stx=l[0]*xscale*scale
        endx = (l[1]-l[0])*xscale*scale
        
        pygame.draw.rect(screen,(0,0,0),[stx,h-30,endx,30],1)
        
        for x in range(l[0],l[1],1):
            x+=.5
            pygame.draw.lines(screen,(0,0,0),False,2*arrow*scale*l[2]+vec2(x*xscale*scale,h),2)
        tex(str(l[2])+'lb/ft',h,l[0]*xscale*scale)
    for m in moments:
        pygame.draw.lines(screen,(0,0,0),False,(arrow2)*scale*m[1]+vec2(m[0]*xscale*scale,h),2)
        pygame.draw.lines(screen,(0,0,0),False,(-arrow2)*scale*m[1]+vec2(m[0]*xscale*scale,h),2)
        tex(str(m[1])+'lb*ft',h,m[0]*xscale*scale)



class Lines:
    def recalc(self):
        YW = fW(graphx)
        YV = fV(graphx)
        YM = fM(graphx)
        YDD = fDD(graphx)
        
        YD = fD(graphx)
        
        
        
        S=[
            scale / np.max(abs(YV)),
            scale / np.max(abs(YM)),
            scale / np.max(abs(YDD)),
            scale / np.max(abs(YD)),
            scale / np.max(abs(YW))
        ]
        
        for x in range(len(S)):
            if S[x]+1 == S[x]:
                S[x] = 0
        print(S)
        self.YW=YW
        self.YV=YV
        self.YM = YM
        self.YDD = YDD
        self.YD = YD
        self.V = np.column_stack((graphx*xscale,-YV*S[0]))*scale
        self.M = np.column_stack((graphx*xscale,-YM*S[1]))*scale
        self.DD = np.column_stack((graphx*xscale,-YDD*S[2]))*scale
        self.D = np.column_stack((graphx*xscale,-YD*S[3]))*scale
        self.W = np.column_stack((graphx*xscale,-YW*S[4]))*scale
    def __init__(self):
        self.recalc()
    

lines = Lines()
#YD -= YD[YD.shape[0]/2]


def calc_reactions(r1,r2):
    fnet = fV(np.array([end+.01],dtype=np.float64))[0]
    print('Fnet: ',fnet)
    endmoment = fM(np.array([end+.0],dtype=np.float64))[0]
    endx = end
    #### (endx-r1)*p1+(endx-r2)*p2 = endmoment
    #### (1)*p1 + (1)*p2 = fnet
    A = np.array([[endx-r1,endx-r2],
        [1,1]])
    B = np.array([[endmoment],[fnet]])
    
    reactions=inv(A).dot(B)
    #print(inv(A).dot(B))
    #DF.append([l[1],l[0],0])#xlocation,strength
    print('DF.append([',reactions[0][0],',',r1,',','0])')
    print('DF.append([',reactions[1][0],',',r2,',','0])')
    
def calc_constants(r1,r2):#places where deflection should be zero
    test1 = np.array([r1])
    test2 = np.array([r2])
    def1 = fD(test1)
    def2 = fD(test2)
    print('deflections',def1,def2)
    
    C.Dis = (def1-def2)/(-r1+r2)
    
    print('C1 = ',C.Dis[0])
    print('C2 = ',-fD(test1)[0])
    C.Dis2 = -fD(test1)[0]
    lines.recalc()
    
    

calc_reactions(0,20)
calc_constants(0,20)

def calc_slope(p):
    test = v([p])
    slopeEI = fDD(test)
    print('slopeEI',slopeEI)
    E = 29000
    I=340
    unitfactor = 12
    print('slope',slopeEI*unitfactor**2/E/I)

def calc_deflection(p):
    test = v([p])
    deflEI = fD(test)
    print('deflectionEI',deflEI)
    E = 29000
    I=340
    unitfactor = 12
    print('deflection',deflEI*unitfactor**3/E/I)

calc_slope(end)
calc_deflection(6.5*2)

while not done:
    screen.fill((250,250,250))
    
    
    
    #drawbeam()
    
    myfont = pygame.font.SysFont('Sans Sherif', 50)
    X= int(pygame.mouse.get_pos()[0]/scale/xscale/np.max(graphx)*graphx.shape[0])
    
    
    tex(str(graphx[X])+' ft',0)
    
    pygame.draw.lines(screen,(0,0,0),False,vec([[0,0],[0,height]])+vec2(X*scale*xscale*np.max(graphx)/graphx.shape[0],0),2)
    
    h=100

    pygame.draw.lines(screen,(255,000,00),False,lines.W+vec2(0,h),4)
    pygame.draw.lines(screen,(255,200,200),False,vec([[0,0],[width,0]])+vec2(0,h),2)
    tex('force',h-50)
    tex(str(lines.YW[X])+' lb',h)
    
    h=350

    pygame.draw.lines(screen,(255,000,00),False,lines.V+vec2(0,h),4)
    pygame.draw.lines(screen,(255,200,200),False,vec([[0,0],[width,0]])+vec2(0,h),2)
    tex('shear V',h-50)
    tex(str(lines.YV[X])+' lb',h)
    
    h=600

    pygame.draw.lines(screen,(0,255,0),False,lines.M+vec2(0,h),4)
    pygame.draw.lines(screen,(200,255,200),False,vec([[0,0],[width,0]])+vec2(0,h),2)
    tex('bending moment M',h-50)
    tex(str(lines.YM[X])+' lb*ft',h)
    
    h=850
    
    
    pygame.draw.lines(screen,(0,255,0),False,lines.DD+vec2(0,h),4)
    pygame.draw.lines(screen,(200,255,200),False,vec([[0,0],[width,0]])+vec2(0,h),2)
    tex('Deflection derivative',h-50)
    tex(str(lines.YDD[X])+' lb*ft*ft',h)
    
    h=1000
    

    pygame.draw.lines(screen,(0,255,0),False,lines.D+vec2(0,h),4)
    pygame.draw.lines(screen,(200,255,200),False,vec([[0,0],[width,0]])+vec2(0,h),2)
    tex('Deflection * EI',h-50)
    tex(str(lines.YD[X])+' lb*ft*ft*ft',h)
    
    # h = 750
    # tex('no lable',h-50)
    # Y = f2(graphx)
    # lines = np.column_stack((graphx*xscale,-Y*1))
    # pygame.draw.lines(screen,(0,0,255),False,lines*scale+vec2(0,h),4)
    # pygame.draw.lines(screen,(200,200,255),False,vec([[0,0],[width,0]])+vec2(0,h),2)
    # tex(Y[X],h)
    
    
    pygame.display.flip()
    clock.tick(90)
    
    
    
    for ev in pygame.event.get():
        if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    done=True
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mousedown=True
        if ev.type == pygame.MOUSEBUTTONUP:
            mousedown=False