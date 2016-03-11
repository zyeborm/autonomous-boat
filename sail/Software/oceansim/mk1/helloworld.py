from math import pi, sin, cos
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *

  
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
 
        # Disable the camera trackball controls.
        self.disableMouse()
        bk_text = "This is my Demo"
        textObject = OnscreenText(text = bk_text, pos = (0.95,-0.95), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ACenter,mayChange=1)
 
        # Load the environment model.
        self.scene = self.loader.loadModel("environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
 
        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
 
        # Load and transform the panda actor.
        self.pandaActor = Actor("panda-model",
                                {"walk": "panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")
 
        # Create the four lerp intervals needed for the panda to
        # walk back and forth.
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))
 
        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

        WindSpeedSlider = DirectSlider(range=(0,10),scale=0.2, value=5, pos = (-1.1,0,-.2), pageSize=3, command=WindSpeedChange) 
        WindSpeedText = OnscreenText(text = "5", pos = (-1.3,-.1), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ALeft,mayChange=1)  
         
        WindDirSlider = DirectSlider(range=(0,360),scale=0.2, value=90, pos = (-1.1,0,-.4), pageSize=3, command=WindDirChange) 
        WindDirText = OnscreenText(text = "5", pos = (-1.3,-.3), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ALeft,mayChange=1)  
         
        CourseSlider = DirectSlider(range=(0,360),scale=0.2, value=0, pos = (-1.1,0,-.6), pageSize=3, command=CourseChange) 
        CourseText = OnscreenText(text = "5", pos = (-1.3,-.5), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ALeft,mayChange=1) 
        

 
 






    
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont



app = MyApp()
def WindSpeedChange():
  WindSpeedText.setText("Wind spd %.2f" % WindSpeedSlider['value'] )
def WindDirChange():
  WindDirText.setText("Wind dir %.2f" % WindDirSlider['value'] )
def CourseChange():
  CourseText.setText("Course %.2f" % CourseSlider['value'] )
  
app.run()

