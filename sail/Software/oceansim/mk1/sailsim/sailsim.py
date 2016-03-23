from math import pi, sin, cos, radians, degrees, atan2, hypot
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import Fog
from panda3d.core import DirectionalLight
from panda3d.core import AmbientLight

from noise import Noise3D

 
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
 
        # Disable the camera trackball controls.
        self.disableMouse()
        
        self.tm = 0 #s
        self.dTm = 0.5 # time between each re-check of conditions
        self.lastTm = 0 #s
        self.xpos = 0 #m
        self.ypos = 0 #m
        self.tilesize = 0
        self.heading = 0 #degrees
        self.speed = 0 #m per second
        self.heel = 0 #degrees
        self.pitch = 0 #degrees
        self.sheet, self.sheetMin, self.sheetMax = 0, 5, 100 #degrees
        self.hike = 10 # abritrary scale
        self.rudder, self.rudderMin, self.rudderMax = 0, -pi/2, pi/2 #arbitrary scale
        self.sPot, self.sPotMin, self.sPotMax = 4, 0, 50 #abitrary scale would be set by calibration procedure
        self.Iturn, self.wt = 30,0.0 #rate of turn degrees/second
        self.lastXtile = -1
        self.lastYtile = -1
        self.wDirMin, self.wDirMax = 1.0, 1.25
        self.wStrMin, self.wStrMax = 3, 6
 
        self.sailInfo = [[1.00,2.16,3.50,4.95,6.06,6.76,7.00,6.76,6.06,4.95,3.50,1.81,0.0],[pi,0.6*pi,0.54*pi,0.58*pi,0.6*pi,0.95*pi,pi,1.05*pi,1.1*pi,1.25*pi,1.4*pi,1.45*pi,1.49*pi],[0,1,2,3,3,3,3,3,3,4,4,4,4]]
        self.rudderInfo = [[0.01, 0.03, 0.06, 0.08, 0.1, 0.11], [pi,0.52*pi,0.55*pi,0.6*pi, 0.7*pi, 0.95*pi]]
        
        self.noiseDir = Noise3D(128, 1/32.0, 5)
        self.noiseStr = Noise3D(128, 1/32.0, 5, 7)
 
        dlight = DirectionalLight('my dlight')
#       dlight.setShadowCaster(True,512,512)
        dlnp = render.attachNewNode(dlight)
        dlnp.setHpr(160,-30,0)
        alight = AmbientLight('alight')
        alnp = render.attachNewNode(alight)

        self.seaRoot = render.attachNewNode("Sea Root")
 
        for i in range(-5,6):
            for j in range(-5,6):
                sea = self.loader.loadModel("water.egg")
                sea.setScale(15, 15, 15)
                sea.reparentTo(self.seaRoot)
                if (self.tilesize == 0):
                    t1,t2 = sea.getTightBounds()
                    self.tilesize = t2.getX() - t1.getX() #sea tiles have to be square
                sea.setPos(i*self.tilesize, j*self.tilesize, 0)            

        self.subsurface = self.loader.loadModel("subsurface.egg")
        self.subsurface.setScale(50,50,50)
        self.subsurface.reparentTo(self.render)

        self.horizon = self.loader.loadModel("horizon.egg")
        self.horizon.setScale(20,20,12)
        self.horizon.setHpr(0,0,180)
        self.horizon.setPos(0,0,160)
        self.horizon.reparentTo(self.subsurface)
        
        self.hull = self.loader.loadModel("hull.egg")
        self.hull.setScale(5,5,5)
        self.hull.setHpr(180,0,0)
        self.hull.reparentTo(self.render)
        self.hull.setLight(dlnp)
        self.hull.setLight(alnp)
#       self.hull.setShaderAuto()

        self.boom = self.loader.loadModel("boom.egg")
        self.boom.setScale(0.2,0.4,0.2)
        self.boom.reparentTo(self.hull)
        self.boom.setPos(0.02,0.0,0.75)
        self.boom.setHpr(0,0,0)
        self.boom.setLight(dlnp)
        self.boom.setLight(alnp)
        
        self.sail = []
        for i in range(5):
            self.sail.append(self.loader.loadModel("sail"+str(i)+".egg"))
            self.sail[i].setScale(5,5,5)
            self.sail[i].setPos(0,2.5,2.6) # this is the correct height to be seen, put them under the water when not in use!
            self.sail[i].setHpr(90,0,0)
            self.sail[i].reparentTo(self.boom)
            
        
        self.burgee = self.loader.loadModel("burgee.egg")
        self.burgee.setScale(0.1,0.1,0.1)
        self.burgee.setPos(0.0,0.4,0.35)
        self.burgee.reparentTo(self.hull)
        self.burgee.setLight(dlnp)
        
        self.tiller = self.loader.loadModel("boom.egg")
        self.tiller.setScale(0.1,0.2,0.1)
        self.tiller.reparentTo(self.hull)
        self.tiller.setPos(0.02,2.2,0.4)
        
        
        self.mark = self.loader.loadModel("mark.egg")
        self.mark.setPos(0,150,-0.5)
        self.mark.setScale(0.7,0.7,0.7)
        self.mark.reparentTo(self.render)
        self.mark.setLight(dlnp)
        self.mark.setLight(alnp)
        
        colour = (0.6,0.6,0.9)
        expfog = Fog("Scene-wide exponential Fog object")
        expfog.setColor(*colour)
        expfog.setExpDensity(0.02)
        self.seaRoot.setFog(expfog)
        base.setBackgroundColor(*colour)

        self.accept('arrow_left', self.turnLeft)
        self.accept('arrow_right', self.turnRight)
        self.accept('arrow_up', self.goFaster)
        self.accept('arrow_down', self.goSlower)
 
        # Add the moveCameraTask and updateVariables procedure to the task manager.
        self.taskMgr.add(self.moveCameraTask, "MoveCameraTask")
        self.taskMgr.doMethodLater(self.dTm, self.updateVariables, "UpdateVariables")



    #motion control
    def turnLeft(self):
#       self.heading = (self.heading + 5) % 360
        if (self.rudder < self.rudderMax):
            self.rudder += 0.02
       
    def turnRight(self):
#       self.heading = (self.heading - 4.867) % 360
        if (self.rudder > self.rudderMin):
            self.rudder -= 0.02
        
    def goFaster(self):
         if (self.sPot > self.sPotMin):
            self.sPot -= 1
        
    def goSlower(self):
        if (self.sPot < self.sPotMax):
            self.sPot += 1
    
    # Define a procedure to move the camera, boat and subsurface; also retile the sea
    def moveCameraTask(self, task):
        if (self.lastTm == 0):
            self.lastTm = task.time
        angleRadians = radians(self.heading)
        self.xpos -= self.speed * sin(angleRadians) * (task.time - self.lastTm) * 3
        self.ypos += self.speed * cos(angleRadians) * (task.time - self.lastTm) * 3
        self.camera.setPos(self.xpos, self.ypos, 3)
        self.heading += self.wt * (task.time - self.lastTm)
        self.camera.setHpr(self.heading, 0, 0)
        self.subsurface.setPos(self.xpos, self.ypos, -0.1)
        self.hull.setPos(self.xpos - 12*sin(angleRadians), self.ypos + 12*cos(angleRadians), 0.0)
        self.hull.setHpr(self.heading - 180, self.pitch, self.heel)
        self.boom.setHpr(self.sheet, 0, 0)
        # check if gone over a tile boundry and refresh tiles
        newXtile = int(self.xpos/self.tilesize) * self.tilesize
        newYtile = int(self.ypos/self.tilesize) * self.tilesize
        if (newXtile != self.lastXtile or newYtile != self.lastYtile):
            xOff = -1* int(2*sin(angleRadians))
            yOff = int(2*cos(angleRadians))
            self.seaRoot.setPos(newXtile + xOff*self.tilesize, newYtile + yOff*self.tilesize, 0)
            self.lastXtile = newXtile
            self.lastYtile = newYtile
        self.lastTm = task.time
        return task.cont
    
    # manage the physics of winds and forces
    def updateVariables(self, task):
        self.tiller.setHpr(180-degrees(self.rudder),0,0)
        self.sheet = interpolate([self.sheetMin, self.sheetMax], self.sPot, self.sPotMin, self.sPotMax) * (1 if (self.sheet >= 0) else -1)
        wDir = interpolate([self.wDirMin, self.wDirMax],self.noiseDir.generate((int(self.xpos/8))%128, (int(self.ypos/8))%128, self.tm%128), -1.0, 1.0)
        wStr = interpolate([self.wStrMin, self.wStrMax],self.noiseStr.generate((int(self.xpos/8))%128, (int(self.ypos/8))%128, self.tm%128), -1.0, 1.0)
        v1 = sin(wDir - radians(self.heading))*wStr
        v2 = cos(wDir - radians(self.heading))*wStr + self.speed
        wDirRel = atan2(v1, v2)
        wStrRel = hypot(v1, v2)
        if (wDirRel > pi):
            wDirRel = wDirRel - 2*pi
        self.burgee.setHpr(degrees(wDirRel),0,0)
        if (abs(wDirRel) < abs(radians(self.sheet))): # flogging sail
            self.sheet = degrees(wDirRel)
        angAtt = wDirRel - radians(self.sheet)
        if (self.sheet > 0 and wDirRel < 0): 
            angAtt += 2*pi
        if (self.sheet < 0 and wDirRel > 0): 
            angAtt -= 2*pi
        if (abs(angAtt) > 3.0): #gybe
            self.sheet *= -1
        area = interpolate(self.sailInfo[0], abs(angAtt), 0, pi)
        LDangle = interpolate(self.sailInfo[1], abs(angAtt), 0, pi)
        sailEgg = int(interpolate(self.sailInfo[2], abs(angAtt), 0, pi))
        for i in range(5):
            self.sail[i].setPos(0,2.5,-20)
        self.sail[sailEgg].setPos(0,2.5,2.6)
        F = 0.5*wStrRel*wStrRel*area*cos(radians(self.heel))
        Fheel = F*sin(wDirRel - LDangle*(1 if (wDirRel > 0) else -1))
        self.heel = Fheel/10
        Fdrive = F*cos(wDirRel - LDangle*(1 if (wDirRel > 0) else -1))
#       print Fheel, Fdrive

        rWt = radians(self.wt)
#       rudderRel = atan2(self.speed, 0.5*rWt) - self.rudder
        rudderRel = atan2(1.0*rWt,self.speed) - self.rudder
        rArea = interpolate(self.rudderInfo[0], abs(rudderRel), 0, self.rudderMax)
        rLDangle = interpolate(self.rudderInfo[1], abs(rudderRel), 0, self.rudderMax)
        rF = 10*self.speed*self.speed*rArea
        rFdrag = -rF*cos(rLDangle)
        rFturn = rF*sin(rLDangle)*(1 if (rudderRel > 0) else -1)
        
        hullDrag = 2*self.speed*self.speed*(1 if (self.speed > 0) else -1)
        
        acc = (Fdrive - rFdrag - hullDrag)/100
        self.speed += acc*self.dTm
        if (self.speed < -0.5):
            self.speed = -0.5
            
        #TODO the height up the mast for turning force needs to be a static var
        wtDot = (-rFturn - 50*rWt*rWt*(1 if (rWt > 0) else -1) - Fdrive*0.25*sin(radians(self.heel)))/self.Iturn
        self.wt += degrees(wtDot*self.dTm)
 
#       print "rudder=%0.2f rLDangle=%0.2f rudderRel=%0.2f wt==%0.10f rFturn=%0.10f wtDot=%0.10f rArea=%0.2f" % (self.rudder,rLDangle,rudderRel, self.wt, rFturn, wtDot, rArea)
        print "speed=%0.2f LDangle=%0.2fpi cos(heel)=%0.2f F=%0.2f drive=%0.2f rudder drag=%0.2f hull drag=%0.2f wDirRel=%0.2f angAtt=%0.2f wStrRel=%0.2f" % (self.speed, LDangle/pi, cos(self.heel), F, Fdrive, rFdrag, hullDrag, degrees(wDirRel), degrees(angAtt), wStrRel)
        self.tm += self.dTm
        return task.again


def interpolate(valList, valIn, valMin, valMax):
    n = len(valList)
    val = (float)(valIn - valMin)/(valMax - valMin)*(n - 1.0)
    i = int(val)
    if (val <= 0):
        return valList[0]
    elif (val >= (n-1)):
        return valList[n-1]
    else:
        return (valList[i] + (valList[i+1] - valList[i])*(val - i))
 
app = MyApp()
app.run()
