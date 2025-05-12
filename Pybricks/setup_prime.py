# pybricks blocks file:{"blocks":{"languageVersion":0,"blocks":[{"type":"blockGlobalSetup","id":"bjK,wS1MYO7aiYkFSwd{","x":55,"y":30,"deletable":false,"next":{"block":{"type":"variables_set_prime_hub","id":"5*I7CuD#@Z~3}`ZzI_*|","extraState":{"optionLevel":0},"fields":{"VAR":{"id":"jJIkyz1^UOv,0qf6Q`S+"}},"next":{"block":{"type":"variables_set_motor","id":"(G-lhvGC+uAIVa|~kXB{","fields":{"VAR":{"id":"-OI,UL5eEDd:vDO%.#-Y"}},"inputs":{"PORT":{"shadow":{"type":"blockParametersPort","id":"59M3JO=1)[ox64^KJ|Uj","fields":{"NAME":"A"}}},"POSITIVE_DIRECTION":{"shadow":{"type":"blockParametersDirection","id":"QV@,39$9rq#WF#-kP`-d","fields":{"SELECTION":"Direction.COUNTERCLOCKWISE"}}}},"next":{"block":{"type":"variables_set_motor","id":"Dy~3Y0eGNs/L7m~H%T,x","fields":{"VAR":{"id":"NUbNwM_q?/@UPdYS!8m8"}},"inputs":{"PORT":{"shadow":{"type":"blockParametersPort","id":"ju5ud?oEGmi77[,^(`E?","fields":{"NAME":"B"}}},"POSITIVE_DIRECTION":{"shadow":{"type":"blockParametersDirection","id":"K%8udHT.*6+QPq#_-r|`","fields":{"SELECTION":"Direction.CLOCKWISE"}}}},"next":{"block":{"type":"variables_set_drive_base","id":"#:T?t]]1vdW(+FeoOTcp","fields":{"VAR":{"id":"LkTwuGXLXu]hC7+Wg?X:"}},"inputs":{"VAR":{"shadow":{"type":"variables_get_motor_device","id":"[ucwr!sZ~jFp;DGc$0),","fields":{"VAR":{"id":"-OI,UL5eEDd:vDO%.#-Y","name":"left","type":"Motor"}}}},"VAR2":{"shadow":{"type":"variables_get_motor_device","id":"M9=#QDv!{x+aM/!1VBPg","fields":{"VAR":{"id":"NUbNwM_q?/@UPdYS!8m8","name":"right","type":"Motor"}}}},"VALUE0":{"shadow":{"type":"unit_distance","id":"KaXz9ZLrCIZD#_m^P^z%","fields":{"VALUE0":56}}},"VALUE1":{"shadow":{"type":"unit_distance","id":"i;x]pSK$fU@Fcqb4vOxO","fields":{"VALUE0":128}}}},"next":{"block":{"type":"variables_set_color_sensor","id":"^?Q}DaPW%veoE3=l?fo.","extraState":{"optionLevel":0},"fields":{"VAR":{"id":"U2_?qyHq_INY{.=:`m1B"}},"inputs":{"PORT":{"shadow":{"type":"blockParametersPort","id":"ud}k^]HX!.p/d-tbD$.Q","fields":{"NAME":"C"}}}},"next":{"block":{"type":"variables_set_ultrasonic_sensor","id":"gbPED?S1N[[a;6CqQ}}#","fields":{"VAR":{"id":"_:7l{4g%UcU+n2tR7,9`"}},"inputs":{"PORT":{"shadow":{"type":"blockParametersPort","id":"EN)I6F!#MQm%e!|~N~[D","fields":{"NAME":"D"}}}}}}}}}}}}}}}}},{"type":"blockGlobalStart","id":"3tJe|AWl0baN(wH9a$@.","x":55,"y":398,"deletable":false,"next":{"block":{"type":"blockComment","id":"eF.DzpHhz;5t({^k}B_n","fields":{"FIELDNAME":"Drive in a square."},"next":{"block":{"type":"blockFlowRepeat","id":"*BGeXb5Brkv2ECFPq7V.","inputs":{"TIMES":{"shadow":{"type":"blockMathNumber","id":"dSg0jHf!tiqLZV.t40]C","fields":{"NUM":4}}},"DO":{"block":{"type":"blockDriveBaseDrive2","id":",us6a!s#%NH#%i+lqwu,","extraState":{"optionLevel":2},"fields":{"METHOD":"DRIVEBASE_DRIVE_STRAIGHT"},"inputs":{"VAR":{"shadow":{"type":"variables_get_drive_base_device","id":"I4A.Xn{`N{#U]XfD7ssS","fields":{"VAR":{"id":"LkTwuGXLXu]hC7+Wg?X:","name":"robot","type":"DriveBase"}}}},"ARG0":{"shadow":{"type":"unit_distance","id":"ORt0z%5nN66C_7Yf53%w","fields":{"VALUE0":250}}},"ARG1":{"shadow":{"type":"parameters_stop_4","id":"]!=D)mUF3J1^vWazf[5H","fields":{"VALUE":"Stop.HOLD"}}}},"next":{"block":{"type":"blockDriveBaseDrive2","id":"Ic`qQoUHfd#U6$=eHKTJ","extraState":{"optionLevel":3},"fields":{"METHOD":"DRIVEBASE_DRIVE_TURN"},"inputs":{"VAR":{"shadow":{"type":"variables_get_drive_base_device","id":";N*CU[(*ME)N[Dp}MO,o","fields":{"VAR":{"id":"LkTwuGXLXu]hC7+Wg?X:","name":"robot","type":"DriveBase"}}}},"ARG0":{"shadow":{"type":"unit_angle","id":"x_i:ONnLq#Bs^$k22ag,","fields":{"VALUE0":90}}},"ARG1":{"shadow":{"type":"parameters_stop_4","id":"o9/KZ;IyFY~:*)SVdS/{","fields":{"VALUE":"Stop.HOLD"}}}}}}}}}}}}}}]},"variables":[{"name":"red","id":"PEdMV`y{f+/2bEqDNOT3","type":"ColorDef"},{"name":"orange","id":"8}O+)b^Kit?DH(eQc2DO","type":"ColorDef"},{"name":"yellow","id":"#1l3o=F,iI%WixF26%Ar","type":"ColorDef"},{"name":"green","id":"M_nB=k[Zdc=C~x]A2yx2","type":"ColorDef"},{"name":"cyan","id":"^Eh.^IzGcS:zTvnN3HZw","type":"ColorDef"},{"name":"blue","id":"l,Gi`v5:9h~@sC/XCK7.","type":"ColorDef"},{"name":"violet","id":"*s^*~Z*r=JO=h:4~^w@p","type":"ColorDef"},{"name":"magenta","id":"P$[C))1K+DQ|6bGt20)2","type":"ColorDef"},{"name":"white","id":":60`%,Y4d+y)p[*pn;pA","type":"ColorDef"},{"name":"none","id":"Spc!cR2SN`j[jNx/tX6k","type":"ColorDef"},{"name":"color","id":"U2_?qyHq_INY{.=:`m1B","type":"ColorSensor"},{"name":"robot","id":"LkTwuGXLXu]hC7+Wg?X:","type":"DriveBase"},{"name":"distance","id":"_:7l{4g%UcU+n2tR7,9`","type":"UltrasonicSensor"},{"name":"left","id":"-OI,UL5eEDd:vDO%.#-Y","type":"Motor"},{"name":"right","id":"NUbNwM_q?/@UPdYS!8m8","type":"Motor"},{"name":"hub","id":"jJIkyz1^UOv,0qf6Q`S+","type":"PrimeHub"}],"info":{"type":"pybricks","version":"1.3.2"}}
from bluepad import BluePad
from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import ColorSensor, Motor, UltrasonicSensor
from pybricks.robotics import DriveBase
from pybricks.tools import wait
# from pupremote_hub import PUPRemoteHub


# Set up all devices.
hub = PrimeHub()
color = ColorSensor(Port.C)
distance = UltrasonicSensor(Port.D)
left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right = Motor(Port.B, Direction.CLOCKWISE)

# instantiate bluepad
bp=BluePad(Port.F)
# bp=PUPRemoteHub(Port.F)


robot = DriveBase(left, right, 56, 128)


# The main program starts here.
# Drive in a square.
# for count in range(4):
#     robot.straight(250)
#     robot.turn(90)
hub.display.char("A")
wait(2000)

hub.display.pixel(1, 2)
wait(2000)
