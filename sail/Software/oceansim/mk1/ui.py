from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "window-title BoatSim")
loadPrcFileData("", "fullscreen 0") # Set to 1 for fullscreen
loadPrcFileData("", "win-size 1200 760")
loadPrcFileData("", "win-origin 600 10")

import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.task.Task import Task
from pandac.PandaModules import TransparencyAttrib

import math
from pandac.PandaModules import ClockObject
FPS = 30
globalClock = ClockObject.getGlobalClock()
globalClock.setMode(ClockObject.MLimited)
globalClock.setFrameRate(FPS)



# Add some text
bk_text = "BoatSim V0.01\n Test"
InfoBlock = OnscreenText(text = bk_text, pos = (0.95,-0.5), scale = 0.07,fg=(0,0,0,1),shadow=(1,1,1,1),align=TextNode.ARight,mayChange=1)



def within_360 (self,dirtion):
  """normalises an angle to between 0 and 360"""
  dirtion = dirtion % 360  # modulus of a -ve number gives a positive result, so -10 mod 360 gives 350 % means mod
  return dirtion
     
# Callback function to set text

 
# Create a frame
#frame = DirectFrame(text = "main", scale = 0.001)
# Add button

 
# Create 4 buttons
#button_1 = DirectButton(text="+1",scale=0.1,pos=(-.3,.6,0), command=incBar,extraArgs = [1])
#button_10 = DirectButton(text="+10",scale=0.1,pos=(0,.6,0), command=incBar,extraArgs = [10])
#button_m1 = DirectButton(text="-1",scale=0.1,pos=(0.3,.6,0), command=incBar,extraArgs = [-1])
#button_m10 = DirectButton(text="-10",scale=0.1,pos=(0.6,.6,0), command=incBar,extraArgs = [-10])

wind_dir = 0

def RudderAngleChange():
  RudderAngleText.setText("Rudder Angle %.2f" % RudderAngleSlider['value'] )
  boat.boat_rudder_angle = RudderAngleSlider['value']

RudderAngleSlider = DirectSlider(range=(-45,45),scale=0.4, value=0, pos = (-1.1,0,0), pageSize=3, command=RudderAngleChange) 
RudderAngleText = OnscreenText(text = "5", pos = (-1.3,.1), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ALeft,mayChange=1)  


def WindSpeedChange():
  WindSpeedText.setText("Wind spd %.2f" % WindSpeedSlider['value'] )
  boat.wind_abs_speed = WindSpeedSlider['value']
    
 
WindSpeedSlider = DirectSlider(range=(0,10),scale=0.4, value=5, pos = (-1.1,0,-.2), pageSize=3, command=WindSpeedChange) 
WindSpeedText = OnscreenText(text = "5", pos = (-1.3,-.1), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ALeft,mayChange=1)  

def WindDirChange():
  boat.wind_abs[1] = WindDirSlider['value']
  WindDirText.setText("Wind dir %.2f" % WindDirSlider['value'])
  #print WindDirSlider['value'], wind_dir
 
WindDirSlider = DirectSlider(range=(0,360),scale=0.4, value=90, pos = (-1.1,0,-.4), pageSize=3, command=WindDirChange) 
WindDirText = OnscreenText(text = "5", pos = (-1.3,-.3), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ALeft,mayChange=1)  


def CourseChange():
  CourseText.setText("Sail Angle %.2f" % CourseSlider['value'] )
  
#  hull.setPos(-1, CourseSlider['value'], .05)    
 

CourseSlider = DirectSlider(range=(-180,180),scale=0.4, value=0, pos = (-1.1,0,-.6), pageSize=3, command=CourseChange) 
CourseText = OnscreenText(text = "5", pos = (-1.3,-.5), scale = 0.07,fg=(1,0.5,0.5,1),align=TextNode.ALeft,mayChange=1) 

position = 0
def Simulate_Boat(self):
  dt = globalClock.getDt()  

  sail_front.setHpr(0,0,(  -1 * boat.Sail_1_rel_angle   ))
  sail_back.setHpr(0,0,( -1 * boat.Sail_2_rel_angle ))
#  print dt
  boat.run_physics(dt)
  pot_pos_tuple = tuple(boat.boat_position)
  hull.setPos(pot_pos_tuple)
  
#  hull.setHpr(( -1 * boat.boat_orientation[0]  ) , 90, -90)
  hull.setH(-1 * boat.boat_orientation[0])
  hull.setR(-1 * boat.boat_orientation[1])
       
  wind_indicator.setPos(pot_pos_tuple) 
  wind_indicator.setHpr(( -1 * boat.wind_rel[1]+90),-90,0)        

  wind_force_indicator.setPos(pot_pos_tuple) 
  wind_force_indicator.setHpr(( -1 * boat.sail_1_force_dir +90 ),-90,0) 
    
  CameraHolder.setPos(pot_pos_tuple)     
#  camera.setPos(0, -4 + boat.boat_position_x, 2.0)    
  camera.lookAt(hull) 
  velocity_vector = math.degrees(math.atan2(boat.boat_velocity[0],boat.boat_velocity[1]))
  speed = math.hypot(boat.boat_velocity[0],boat.boat_velocity[1])
  InfoBlock.setText("Speed %.2f M/s %.2f kts \n Velocity Vector %.2f \n Hull Direction %.2f \n AoA 1: %.2f 1: %.2f \n Sail Force 1: %.2f 2: %.2f" % (speed,speed*1.94384,velocity_vector,boat.boat_orientation[0],0,0,0,0))
  return Task.cont

def Set_Camera(self):
  camera.setPos(4, -4, 2.0)
  camera.lookAt(0.0, 0.0, 0.0)
  return Task.cont  
  
#scene2 = loader.loadModel("environment")
#scene2.reparentTo(render)
#scene2.setPos(-8, 42, 0)


hull = loader.loadModel("models/hull.x")
hull.setScale(0.001, 0.001, 0.001) 


hull.reparentTo(render)
hull.setPos(0, 0, 0)
hull.setHpr(0,90,-90)
hull.setColor(0,128,128,128)

sail_front = loader.loadModel("models/sail_centered.x")
sail_front.reparentTo(hull)
sail_front.setColor(128,128,128,128)
sail_front.setPos(-400,0,-0)

sail_back = loader.loadModel("models/sail_centered.x")
sail_back.reparentTo(hull)
sail_back.setColor(128,128,128,128)
sail_back.setPos(00,0,-0)

#plight = AmbientLight('my plight')
#plight.setColor(VBase4(0.12, 0.12, 0.12, 1))
#plnp = render.attachNewNode(plight)
#render.setLight(plnp)

#light2 = PointLight('pointlight')
#plnp2 = render.attachNewNode(light2)
#plnp2.setPos(20,2,2)
#render.setLight(plnp2)


# Run the tutorial
class boat_simulator:
  """This will simulate a boat... hopefully"""
  boat_mass = 10 #kg
  boat_rotational_inertia = [10,0,0] #FIXME, wild assed guess
  
  boat_force_matrix = [0,0,0]
  boat_acceleration_matrix = [0,0,0]  
  boat_velocity = [0,0,0]
  boat_position = [-1,0,0.05] # x , y , z
  
  boat_torque_matrix = [0,0,0]  
  boat_rotational_acceleration_matrix = [0,0,0]    
  boat_rotational_velocity = [0,0,0]
  boat_orientation = [0,0,0]
  
  force_list = []
  torque_list = []  
  
  wind_abs_dir = 90
  wind_abs_vel = 5  
  wind_abs=[5,90]
#  wind_rel_dir = 90
#  wind_rel_vel = 0
  wind_rel= [0,90] #mag,direction
  
  Sail_1_rel_angle = 0 #angle to the world
  Sail_1_rel_angle = 0 #angle to the boat hull
  Sail_1_AoA = 0       #angle to the air flow over the boat hull
  sail_1_force_dir = 0 #resultant force direction, world referenced

  Sail_2_abs_angle = 0
  Sail_2_rel_angle = 0
  Sail_2_AoA = 0
  sail_2_force_dir = 0 

  boat_rudder_angle = 0
  
  wing_CD_lookup = []
  wing_CD_lookup.append((0,0,0.0067))
  wing_CD_lookup.append((1,0.11,0.0068))
  wing_CD_lookup.append((2,0.22,0.007))
  wing_CD_lookup.append((3,0.33,0.0075))
  wing_CD_lookup.append((4,0.44,0.0083))
  wing_CD_lookup.append((5,0.55,0.0097))
  wing_CD_lookup.append((6,0.66,0.0108))
  wing_CD_lookup.append((7,0.77,0.0118))
  wing_CD_lookup.append((8,0.88,0.0128))
  wing_CD_lookup.append((9,0.9598,0.0144))
  wing_CD_lookup.append((10,1.0343,0.0159))
  wing_CD_lookup.append((11,1.0749,0.0175))
  wing_CD_lookup.append((12,1.039,0.0195))
  wing_CD_lookup.append((13,0.8737,0.0216))
  wing_CD_lookup.append((14,0.6284,0.0236))
  wing_CD_lookup.append((15,0.4907,0.117))
  wing_CD_lookup.append((16,0.4696,0.21))
  wing_CD_lookup.append((17,0.5195,0.23))
  wing_CD_lookup.append((18,0.5584,0.252))
  wing_CD_lookup.append((19,0.6032,0.274))
  wing_CD_lookup.append((20,0.6474,0.297))
  wing_CD_lookup.append((21,0.6949,0.32))
  wing_CD_lookup.append((22,0.7446,0.344))
  wing_CD_lookup.append((23,0.7948,0.369))
  wing_CD_lookup.append((24,0.8462,0.394))
  wing_CD_lookup.append((25,0.8984,0.42))
  wing_CD_lookup.append((26,0.9506,0.446))
  wing_CD_lookup.append((27,1.0029,0.473))
  wing_CD_lookup.append((28,0.98825,0.489166666666667))
  wing_CD_lookup.append((29,0.9736,0.505333333333333))
  wing_CD_lookup.append((30,0.915,0.57))
  wing_CD_lookup.append((31,0.9325,0.599166666666667))
  wing_CD_lookup.append((32,0.95,0.628333333333333))
  wing_CD_lookup.append((33,0.9675,0.6575))
  wing_CD_lookup.append((34,0.985,0.686666666666667))
  wing_CD_lookup.append((35,1.02,0.745))
  wing_CD_lookup.append((36,1.02916666666667,0.774166666666667))
  wing_CD_lookup.append((37,1.03833333333333,0.803333333333333))
  wing_CD_lookup.append((38,1.0475,0.8325))
  wing_CD_lookup.append((39,1.05666666666667,0.861666666666667))
  wing_CD_lookup.append((40,1.075,0.92))
  wing_CD_lookup.append((41,1.06391666666667,0.945833333333333))
  wing_CD_lookup.append((42,1.05283333333333,0.971666666666667))
  wing_CD_lookup.append((43,1.04175,0.9975))
  wing_CD_lookup.append((44,1.03066666666667,1.02333333333333))
  wing_CD_lookup.append((45,1.0085,1.075))
  wing_CD_lookup.append((46,1.01375,1.09833333333333))
  wing_CD_lookup.append((47,1.019,1.12166666666667))
  wing_CD_lookup.append((48,1.02425,1.145))
  wing_CD_lookup.append((49,1.0295,1.16833333333333))
  wing_CD_lookup.append((50,1.04,1.215))
  wing_CD_lookup.append((51,1.0275,1.23666666666667))
  wing_CD_lookup.append((52,1.015,1.25833333333333))
  wing_CD_lookup.append((53,1.0025,1.28))
  wing_CD_lookup.append((54,0.99,1.30166666666667))
  wing_CD_lookup.append((55,0.965,1.345))
  wing_CD_lookup.append((56,0.95,1.36583333333333))
  wing_CD_lookup.append((57,0.935,1.38666666666667))
  wing_CD_lookup.append((58,0.92,1.4075))
  wing_CD_lookup.append((59,0.905,1.42833333333333))
  wing_CD_lookup.append((60,0.875,1.47))
  wing_CD_lookup.append((61,0.856666666666667,1.4875))
  wing_CD_lookup.append((62,0.838333333333333,1.505))
  wing_CD_lookup.append((63,0.82,1.5225))
  wing_CD_lookup.append((64,0.801666666666667,1.54))
  wing_CD_lookup.append((65,0.765,1.575))
  wing_CD_lookup.append((66,0.745833333333333,1.59))
  wing_CD_lookup.append((67,0.726666666666667,1.605))
  wing_CD_lookup.append((68,0.7075,1.62))
  wing_CD_lookup.append((69,0.688333333333333,1.635))
  wing_CD_lookup.append((70,0.65,1.665))
  wing_CD_lookup.append((71,0.6275,1.67666666666667))
  wing_CD_lookup.append((72,0.605,1.68833333333333))
  wing_CD_lookup.append((73,0.5825,1.7))
  wing_CD_lookup.append((74,0.56,1.71166666666667))
  wing_CD_lookup.append((75,0.515,1.735))
  wing_CD_lookup.append((76,0.490833333333333,1.7425))
  wing_CD_lookup.append((77,0.466666666666667,1.75))
  wing_CD_lookup.append((78,0.4425,1.7575))
  wing_CD_lookup.append((79,0.418333333333333,1.765))
  wing_CD_lookup.append((80,0.37,1.78))
  wing_CD_lookup.append((81,0.345,1.78333333333333))
  wing_CD_lookup.append((82,0.32,1.78666666666667))
  wing_CD_lookup.append((83,0.295,1.79))
  wing_CD_lookup.append((84,0.27,1.79333333333333))
  wing_CD_lookup.append((85,0.22,1.8))
  wing_CD_lookup.append((86,0.195,1.8))
  wing_CD_lookup.append((87,0.17,1.8))
  wing_CD_lookup.append((88,0.145,1.8))
  wing_CD_lookup.append((89,0.12,1.8))
  wing_CD_lookup.append((90,0.07,1.8))
  wing_CD_lookup.append((91,0.0466666666666667,1.79666666666667))
  wing_CD_lookup.append((92,0.0233333333333333,1.79333333333333))
  wing_CD_lookup.append((93,0,1.79))
  wing_CD_lookup.append((94,-0.0233333333333333,1.78666666666667))
  wing_CD_lookup.append((95,-0.07,1.78))
  wing_CD_lookup.append((96,-0.095,1.775))
  wing_CD_lookup.append((97,-0.12,1.77))
  wing_CD_lookup.append((98,-0.145,1.765))
  wing_CD_lookup.append((99,-0.17,1.76))
  wing_CD_lookup.append((100,-0.22,1.75))
  wing_CD_lookup.append((101,-0.245,1.74166666666667))
  wing_CD_lookup.append((102,-0.27,1.73333333333333))
  wing_CD_lookup.append((103,-0.295,1.725))
  wing_CD_lookup.append((104,-0.32,1.71666666666667))
  wing_CD_lookup.append((105,-0.37,1.7))
  wing_CD_lookup.append((106,-0.393333333333333,1.68916666666667))
  wing_CD_lookup.append((107,-0.416666666666667,1.67833333333333))
  wing_CD_lookup.append((108,-0.44,1.6675))
  wing_CD_lookup.append((109,-0.463333333333333,1.65666666666667))
  wing_CD_lookup.append((110,-0.51,1.635))
  wing_CD_lookup.append((111,-0.529166666666667,1.62166666666667))
  wing_CD_lookup.append((112,-0.548333333333333,1.60833333333333))
  wing_CD_lookup.append((113,-0.5675,1.595))
  wing_CD_lookup.append((114,-0.586666666666667,1.58166666666667))
  wing_CD_lookup.append((115,-0.625,1.555))
  wing_CD_lookup.append((116,-0.643333333333333,1.54))
  wing_CD_lookup.append((117,-0.661666666666667,1.525))
  wing_CD_lookup.append((118,-0.68,1.51))
  wing_CD_lookup.append((119,-0.698333333333333,1.495))
  wing_CD_lookup.append((120,-0.735,1.465))
  wing_CD_lookup.append((121,-0.7525,1.44583333333333))
  wing_CD_lookup.append((122,-0.77,1.42666666666667))
  wing_CD_lookup.append((123,-0.7875,1.4075))
  wing_CD_lookup.append((124,-0.805,1.38833333333333))
  wing_CD_lookup.append((125,-0.84,1.35))
  wing_CD_lookup.append((126,-0.851666666666667,1.32916666666667))
  wing_CD_lookup.append((127,-0.863333333333333,1.30833333333333))
  wing_CD_lookup.append((128,-0.875,1.2875))
  wing_CD_lookup.append((129,-0.886666666666667,1.26666666666667))
  wing_CD_lookup.append((130,-0.91,1.225))
  wing_CD_lookup.append((131,-0.915833333333333,1.20166666666667))
  wing_CD_lookup.append((132,-0.921666666666667,1.17833333333333))
  wing_CD_lookup.append((133,-0.9275,1.155))
  wing_CD_lookup.append((134,-0.933333333333333,1.13166666666667))
  wing_CD_lookup.append((135,-0.945,1.085))
  wing_CD_lookup.append((136,-0.945,1.05833333333333))
  wing_CD_lookup.append((137,-0.945,1.03166666666667))
  wing_CD_lookup.append((138,-0.945,1.005))
  wing_CD_lookup.append((139,-0.945,0.978333333333334))
  wing_CD_lookup.append((140,-0.945,0.925))
  wing_CD_lookup.append((141,-0.939166666666667,0.896666666666667))
  wing_CD_lookup.append((142,-0.933333333333333,0.868333333333333))
  wing_CD_lookup.append((143,-0.9275,0.84))
  wing_CD_lookup.append((144,-0.921666666666667,0.811666666666667))
  wing_CD_lookup.append((145,-0.91,0.755))
  wing_CD_lookup.append((146,-0.9,0.725))
  wing_CD_lookup.append((147,-0.89,0.695))
  wing_CD_lookup.append((148,-0.88,0.665))
  wing_CD_lookup.append((149,-0.87,0.635))
  wing_CD_lookup.append((150,-0.85,0.575))
  wing_CD_lookup.append((151,-0.831666666666667,0.549166666666667))
  wing_CD_lookup.append((152,-0.813333333333333,0.523333333333333))
  wing_CD_lookup.append((153,-0.795,0.4975))
  wing_CD_lookup.append((154,-0.776666666666667,0.471666666666667))
  wing_CD_lookup.append((155,-0.74,0.42))
  wing_CD_lookup.append((156,-0.726666666666667,0.403333333333333))
  wing_CD_lookup.append((157,-0.713333333333333,0.386666666666667))
  wing_CD_lookup.append((158,-0.7,0.37))
  wing_CD_lookup.append((159,-0.686666666666667,0.353333333333333))
  wing_CD_lookup.append((160,-0.66,0.32))
  wing_CD_lookup.append((161,-0.6625,0.305))
  wing_CD_lookup.append((162,-0.665,0.29))
  wing_CD_lookup.append((163,-0.6675,0.275))
  wing_CD_lookup.append((164,-0.67,0.26))
  wing_CD_lookup.append((165,-0.675,0.23))
  wing_CD_lookup.append((166,-0.704166666666667,0.215))
  wing_CD_lookup.append((167,-0.733333333333333,0.2))
  wing_CD_lookup.append((168,-0.7625,0.185))
  wing_CD_lookup.append((169,-0.791666666666667,0.17))
  wing_CD_lookup.append((170,-0.85,0.14))
  wing_CD_lookup.append((171,-0.823333333333333,0.125833333333333))
  wing_CD_lookup.append((172,-0.796666666666667,0.111666666666667))
  wing_CD_lookup.append((173,-0.77,0.0975))
  wing_CD_lookup.append((174,-0.743333333333334,0.0833333333333333))
  wing_CD_lookup.append((175,-0.69,0.055))
  wing_CD_lookup.append((176,-0.575,0.05))
  wing_CD_lookup.append((177,-0.46,0.045))
  wing_CD_lookup.append((178,-0.345,0.04))
  wing_CD_lookup.append((179,-0.23,0.035))
  wing_CD_lookup.append((180,0,0.025))

  def vector_add(vec_1,vec_2):
    """Adds 2 vectors, form of (Mag,Direction (in degrees))"""
    X1 = vec_1[0] * math.sin(math.radians(vec_1[1]))
    Y1 = vec_1[0] * math.cos(math.radians(vec_1[1]))    

    X2 = vec_2[0] * math.sin(math.radians(vec_1[2]))
    Y2 = vec_2[0] * math.cos(math.radians(vec_1[2]))    
  
    Total_X = X1 + X2
    Total_Y = Y1 + Y2    
    
    Magnitude = math.hypot(Total_X,Total_Y)
    Direction = math.degrees(math.atan2(Total_X,Total_Y))   
    return (Magnitude,Direction)
      
  def WingCDs(self,Angle_Of_Attack):    
    "Returns an interpolated value of the ([angle],[coefficent of lift],[coefficent of drag]) given the table from sandia for a 0012 aerofoil given the angle of attack in degrees"""
    def linear_interpolate_1D(input_angle,list_angle1,list_angle2,coef1,coef2):
     # diff_angle = list_angle2 - list_angle1
      diff_coef = coef2 - coef1
      result = (input_angle - list_angle1) / diff_coef + coef1
      return result
    
    Angle_Of_Attack = within_360(self,Angle_Of_Attack)  #convert angle to a 0-360 range

    Output_direction = 1   #used to invert the output force direction if angle is over 180 degrees, so we only need a 180deg table
    Return_Value = ()
    if Angle_Of_Attack > 180:
      Angle_Of_Attack = 180 - (Angle_Of_Attack - 180)  #aerofoil is symetrical so CD / CL for 170 degrees = 190 degrees, need to invert the sign of the output though
      Output_direction = -1
    else:
      Output_direction = 1

    Last_Angle = self.wing_CD_lookup[0] # populate the start angle
    for Search_Angle in self.wing_CD_lookup:     
      if (Search_Angle[0] == Angle_Of_Attack):
        #exact match, take it and bail
        Return_Value = Search_Angle
        break 
      if (Search_Angle[0] > Angle_Of_Attack):     
        #We have gone past the desired angle in the list so we need to interpolate between this one and the last one
        Return_Value = Search_Angle #FIXME, use the interpolator 
        break
    Return_Value_corrected = (Return_Value[0]* Output_direction,Return_Value[1] * Output_direction,Return_Value[2])
    return Return_Value_corrected 
    
  def sail_force(self,Sail_Abs_Angle,heel):
    """Give force on a sail, takes in world referenced sail angle"""
    if (self.wind_rel[0] > 0):  #no force with no wind speed
      Sail_Area = .2 #FIXME use the heel angle to reduce this
      AoA = within_360(0,(self.wind_rel[1] - Sail_Abs_Angle ))
      coefficents = self.WingCDs(AoA)
      #find boat velocity 
      
      
      lift = .5 * coefficents[1] * 1.225 * (self.wind_rel[0] ** 2) * Sail_Area 
      drag = .5 * coefficents[2] * 1.225 * (self.wind_rel[0] ** 2) * Sail_Area
      
      angle = math.degrees(math.atan(lift/drag))   #trig quadrants sorted by the coefficents
      angle_to_wind = angle
      angle = angle +  self.wind_rel[1] -180
      print "rel_wind_dir %.2f, abs_wind %.2f" % (self.wind_rel[1],self.wind_abs[1])
      force = math.hypot(lift,drag)
    else:
      angle=0
      force=0
      lift=0
      drag=0
      angle_to_wind=0
      coefficents = self.WingCDs(AoA)
      
    print "lift %.2f:%.2f drag %.2f:%.2f abs_angle %.2f angle_to_wind %.2f angle %.2f AoA %.2f Force %.2f" % (lift, coefficents[1],drag, coefficents[2],Sail_Abs_Angle,angle_to_wind,angle,AoA, force)    
	#print angle,force
    return (force,angle) 
  
  def process_forces(self):
    #print self.force_list
    boat_force_matrix = []
    total_force_X = 0
    total_force_Y = 0
    for force in self.force_list:
      Force_X = force[0] * math.sin(math.radians(force[1]))
      Force_Y = force[0] * math.cos(math.radians(force[1]))
      print "%-10s - Force X : %.2f Force Y %.2f    :   Force %.2f : Angle %.2f" % (force[2],Force_X ,Force_Y,force[0],force[1])
      total_force_X += Force_X
      total_force_Y += Force_Y      
    print "%-10s - Force X : %.2f Force Y %.2f " % ("Total",total_force_X ,total_force_Y)
    self.boat_force_matrix = [total_force_X ,total_force_Y,0]

  def process_accelerations(self):
    #f = ma f/m=a
    #print self.boat_force_matrix
    accel_X = self.boat_force_matrix[0] / self.boat_mass
    accel_Y = self.boat_force_matrix[1] / self.boat_mass    
    self.boat_acceleration_matrix = [accel_X,accel_Y,0]  
    print "accel" , self.boat_acceleration_matrix

  def process_velocities(self,dt):
    #f = ma f/m=a
    #print self.boat_force_matrix
    velocity_X = self.boat_velocity[0] + self.boat_acceleration_matrix[0] * dt
    velocity_Y = self.boat_velocity[1] + self.boat_acceleration_matrix[1] * dt
    self.boat_velocity = [velocity_X,velocity_Y,0]  
    print "velocity" , self.boat_velocity


  def process_motions(self,dt):  
    #s = ut + .5at^2
    dx = self.boat_velocity[0] * dt + .5 * self.boat_acceleration_matrix[0] * (dt * dt)
    dy = self.boat_velocity[1] * dt + .5 * self.boat_acceleration_matrix[1] * (dt * dt)    
    self.boat_position = [self.boat_position[0] + dx,self.boat_position[1] + dy,0.05] # x , y , z
    print "pos" , self.boat_position

  #def translate_world_XY_to_hull_aligned(self,X,Y)
    
  def generate_water_forces(self):  
      """Generates lift and drag from the keel, also makes the rudder, do rudder stuff"""
    #fake keel uses magic constants #FIXME
    #needs to take into account heel too #FIXME
      Keel_Area = 0.2
      Keel_Lift_Constant = 3
      Keel_Drag_Constant = .01
            
      if ((self.boat_velocity[0] != 0) & (self.boat_velocity[1] != 0)):
        velocity_vector = math.degrees(math.atan2(boat.boat_velocity[0],boat.boat_velocity[1])) - self.boat_orientation[0]
        speed = math.hypot(boat.boat_velocity[0],boat.boat_velocity[1])
        velocity_vector = within_360(0,velocity_vector)
        vel_side = speed * math.sin(math.radians(velocity_vector)) 
        vel_forward = speed * math.cos(math.radians(velocity_vector)) 

        lift = .5 * Keel_Lift_Constant * 1025 * (vel_side ** 2) * Keel_Area 
        drag = .5 * Keel_Drag_Constant * 1025 * (vel_forward ** 2) * Keel_Area 
        #bo = within_360(0,self.boat_orientation[0])
        if vel_side > 0:
          lift = lift * -1
        self.boat_orientation[1] = lift
        if vel_forward < 0:
          drag = drag * -2 #Add a bit extra drag for going backwards

#        if (self.boat_orientation[0] > 270)  & (self.boat_orientation[0] <= 360):
#          lift = lift * -1
          
        print "velocity_vector %.2f vel Side %.2f Vel Fwd %.2f lift %.2f drag  %.2f" % (velocity_vector,vel_side,vel_forward,lift,drag)
        self.force_list.append((lift,within_360(self,self.boat_orientation[0] + 90),"keel lift")) 
        self.force_list.append((drag,within_360(self,self.boat_orientation[0] - 180),"keel drag"))        

        #rudder stuff                 
        Rudder_Area = 0.5
        Rudder_Constant = .1
        Keel_Constant = 5
        Keel_Area = .01
#        Rudder_AoA = within_360(0,velocity_vector - self.boat_rudder_angle)
        rudder_torque = .5 * self.boat_rudder_angle * Rudder_Constant * 1025 * (vel_forward ** 2) * Rudder_Area 
        if (vel_forward < 0):
          rudder_torque = rudder_torque * -1
#        print "rudder AOA %.2f" % (Rudder_AoA)
        self.torque_list.append((rudder_torque,0,0,"rudder torque"))                
        keel_torque = (.5 * self.boat_rotational_velocity[0] * Keel_Constant * 1025 * (vel_forward ** 2) * Keel_Area) * -1
        self.torque_list.append((keel_torque,0,0,"keel torque"))   
        keel_torque_static = (.5 * self.boat_rotational_velocity[0] * Keel_Constant * 1025 * Keel_Area) * -1
        self.torque_list.append((keel_torque_static,0,0,"keel torque static"))         
  def process_torques(self,dt):
    #print self.force_list
    boat_torque_matrix = []
    boat_rotational_acceleration_matrix = []    
    Torque_A = 0
    #total_force_Y = 0
    for torque in self.torque_list:      
      print "%-10s - Torque A : %.2f B %.2f  C %.2f" % (torque[3],torque[0],torque[1],torque[2])
      Torque_A += torque[0]
   

    print "%-10s - Torque A : %.2f B %.2f  C %.2f" % ("Total", Torque_A,0,0)
    self.boat_torque_matrix = [Torque_A,0,0]
    self.torque_list = []
    #f/m=a
    self.boat_rotational_acceleration_matrix[0] = self.boat_torque_matrix[0]/self.boat_rotational_inertia[0]
    self.boat_rotational_velocity[0] = self.boat_rotational_velocity[0] + self.boat_rotational_acceleration_matrix[0] * dt
    self.boat_orientation[0] = self.boat_orientation[0] + (self.boat_rotational_velocity[0] * dt + .5 * self.boat_rotational_acceleration_matrix[0] * dt ** 2)

    
  def calculate_relative_wind(self):
      Speed_X = self.wind_abs[0] * math.sin(math.radians(self.wind_abs[1]))
      Speed_Y = self.wind_abs[0] * math.cos(math.radians(self.wind_abs[1]))
      Speed_X += self.boat_velocity[0]
      Speed_Y += self.boat_velocity[1]
      self.wind_rel[1] = math.degrees(math.atan2(Speed_X,Speed_Y))
      self.wind_rel[0] = math.hypot(Speed_X,Speed_Y)


    
  def run_physics(self,dt):
    #self.boat_position_x = self.boat_position_x + dt
    self.force_list = []
    torque_list = [] #not used
        
    self.wind_abs[1] = WindDirSlider['value'] 
    self.wind_abs[0] = WindSpeedSlider['value'] 
    self.calculate_relative_wind()

    

    self.Sail_1_rel_angle = CourseSlider['value']
    self.Sail_2_rel_angle = CourseSlider['value']
    
    self.Sail_1_abs_angle = self.Sail_1_rel_angle + self.boat_orientation[0] #+ 90
    self.Sail_2_abs_angle = self.Sail_2_rel_angle + self.boat_orientation[0] #+ 90
      
    #Sail_Angle_Of_Attack = within_360(self,self.sail_1_AOA)

    #print self.wind_rel[0]
    
    sail_force = self.sail_force(self.Sail_1_abs_angle,0)
    self.sail_1_force_dir = sail_force[1]
    #self.sail_force_dir = sail_force[0] #+WindDirSlider['value']
    self.force_list.append((sail_force[0],within_360(self,sail_force[1]),"Sail 1"))    
    self.force_list.append((sail_force[0],within_360(self,sail_force[1]),"Sail 2"))       
    

    #print "boat angle %.2f boat force %.2f" % (force_list[0][0],force_list[0][1])
    #self.boat_position[1] = self.boat_position[1] + dt * .5 * self.WingCDs(Sail_Angle_Of_Attack)[1]
    #print "Force Forward %.2f Force Sideways %.2f" % (sail_force[1] * math.cos(math.radians(sail_force[0])),(sail_force[1] * math.sin(math.radians(sail_force[0])) ))
    self.generate_water_forces()
    #self.generate_rudder_forces()
    self.process_forces()
    self.process_accelerations()
    self.process_velocities(dt)    
    self.process_motions(dt)
    self.process_torques(dt)
    #print self.boat_acceleration_matrix
    print "---------------------"
    #print self.WingCDs(Sail_Angle_Of_Attack),Sail_Angle_Of_Attack
    #print self.boat_position_x

    
boat = boat_simulator()    

CameraHolder = render.attachNewNode("CameraHolder")
CameraHolder.setPos(0, 0, 0)

camera.reparentTo(CameraHolder)


# set up a texture for (h by w) 8 bit gray scale image
#tex = Texture()
#tex.setup2dTexture("textures/water1-grid.jpg")

# set up a card to apply the numpy texture
cm = CardMaker("plane")
cm.setFrame(-100, 100, -100, 100)
plane = render.attachNewNode(cm.generate())
plane.setP(270)

tex = loader.loadTexture("textures/water1-grid.jpg")
plane.setTexture(tex)
texStage = TextureStage.getDefault()
plane.setTexScale(texStage, 40, 40)


wind_indicator_something = CardMaker("wind_indicator")
wind_indicator_something.setFrame(-1, 1, -1, 1)
wind_indicator = render.attachNewNode(wind_indicator_something.generate())
wind_indicator.setP(0)

tex = loader.loadTexture("textures/wind_dir.png")
wind_indicator.setTexture(tex)
texStage = TextureStage.getDefault()
wind_indicator.setTexScale(texStage, 1, 1)
wind_indicator.setTransparency(TransparencyAttrib.MAlpha)


wind_force_indicator_something = CardMaker("wind_force_indicator")
wind_force_indicator_something.setFrame(-1, 1, -1, 1)
wind_force_indicator = render.attachNewNode(wind_force_indicator_something.generate())
wind_force_indicator.setP(0)

tex = loader.loadTexture("textures/wind_force_dir.png")
wind_force_indicator.setTexture(tex)
texStage = TextureStage.getDefault()
wind_force_indicator.setTexScale(texStage, 1, 1)
wind_force_indicator.setTransparency(TransparencyAttrib.MAlpha)

render.setAntialias(AntialiasAttrib.MAuto)
  
gameTask = taskMgr.add(Simulate_Boat, "Simulate_Boat")
gameTask = taskMgr.add(Set_Camera, "Set_Camera")

base.run()

