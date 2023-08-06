from .device import Device, _name_attr, GROUP
from . import trk
from .motor import Motor, axis_type
from . import keys as K
from .manager import Manager # see at the end of file
from .interface import Int16, nodealiasproperty
from .tools import upload

#                      _              _   
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __|
# | (_| (_) | | | \__ \ || (_| | | | | |_ 
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|
# 

##### ############
# SUBSTATE
@_name_attr
class SUBSTATE(trk.SUBSTATE):
    pass
### ##############
# errors
@_name_attr
class RPC_ERROR(trk.RPC_ERROR):
    txt = {
        # add more rpc error description here if necessary
    }

### ##############
# RPC error
@_name_attr
class ERROR(trk.ERROR):
    txt = {
        # add more rpc error description here if necessary
    }

### ############# 
# Mode 
@_name_attr
class MODE:
    ENG		= 0
    STAT	= 1
    SKY		= 2
    ELEV	= 3
    USER	= 4
    group = {
        ENG		: GROUP.ENG,
        STAT	: GROUP.STATIC,
        SKY		: GROUP.TRACKING,
        ELEV	: GROUP.TRACKING,
        USER	: GROUP.TRACKING,
    }
    
def mode_parser(mode):
    if isinstance(mode, str):
        if mode not in ['SKY', 'ELEV']:
            raise ValueError('tracking mode must be one of SKY or ELEV got %r'%mode)
        mode = getattr(MODE,mode)
    return Int16(mode)

#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class DrotStatInterface(Device.StatInterface):
    ERROR = ERROR
    MODE = MODE
    SUBSTATE = SUBSTATE
    
    @nodealiasproperty("track_mode_txt", ["track_mode"])
    def track_mode_txt(self, track_mode):
        return self.MODE.txt.get(track_mode, "UNKNOWN")
    
class DrotCfgInterface(Device.CfgInterface):
    # we can define the type to parse value directly on the class by annotation
    axis_type : axis_type

# redefine the Method interface to include the proper description of the RpcError
class DrotRpcNode(Device.RpcInterface.RpcNode):
    RPC_ERROR = RPC_ERROR

class DrotRpcInterface(Device.RpcInterface):
    RpcNode = DrotRpcNode
    RPC_ERROR = RPC_ERROR
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All method args types must be defined in a tuple
    rpcMoveAbs    : (float, float)
    rpcMoveRel    : (float, float)
    rpcMoveAngle  : (float,)
    rpcMoveVel    : (float,)
    rpcStartTrack : (mode_parser, float)
    
#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
class Drot(Motor,trk.Trk):
    SUBSTATE = SUBSTATE
    MODE = MODE 
    ERROR = ERROR
    
    RpcInterface  = DrotRpcInterface
    StatInterface = DrotStatInterface
    CfgInterface  = DrotCfgInterface
    
    def start_track(self, mode, angle=0.0):
        """ Start drot tracking 
        
        Args:
            mode (int, str): tracking mode. Int constant defined in Drot.MODE.SKY, Drot.MODE.ELEV
                             str 'SKY' or 'ELEV' is also accepted
            angle (float): paSky or paPupil depending of the mode
        """
        self.rpc.rpcStartTrack.rcall(mode, angle)
    
    def move_angle(self, angle=0.0):
        """ Move drot to angle in STAT mode """
        self.rpc.rpcMoveAngle.rcall(angle)
    
    def move_abs(self, pos, vel):
        """ Move the drot to an absolute position in ENG mode 
        
        Args:
            pos (float): absolute position
            vel (float):   target velocity for the movement
        """
        self.rpc.rpcMoveAbs.rcall(pos, vel)
    
    def move_rel(self, pos, vel):
        """ Move the drot to a relative position in ENG mode 
        
        Args:
            pos (float): relative position
            vel (float): target velocity for the movement
        """
        self.rpc.rpcMoveRel.rcall(pos, vel)
    
    def move_vel(self, vel):
        """ move drot in velocity 
        
        Args:
           vel (float): target velocity
        """
        self.rpc.rpcMoveVel.rcall( vel)
    
    def stop(self):
        """ Stop drotator motion """
        self.rpc.rpcStop.rcall()
    
Manager.record_new_device_type('Drot', Drot)

Manager.record_cfg_template('Drot', """{name}:
  type: Drot
  interface: Softing
  identifier: PLC1                             # OPCUA Object Identifier
  prefix: MAIN_FAST.drot1                       # TO BE UPDATED OPCUA attribute prefix
  simulated: false
  ignored: false
  address: {address}
  simaddr: opc.tcp://134.171.57.209:4840       # Simulation address
  mapfile: "{cfg_dir}/mapDrot.yml"     # TO BE UPDATED 
  fits_prefix: "DROT1"
  ctrl_config:
    latitude:              -0.429833092
    longitude:             1.228800386
    velocity:              3.0
    min_pos:               -359
    max_pos:               359.0
    axis_type:             CIRCULAR
    active_low_lstop:      false
    active_low_lhw:        false
    active_low_ref:        true
    active_low_index:      false
    active_low_uhw:        true
    active_low_ustop:      false
    brake:                 false
    low_brake:             false
    low_inpos:             false
    backlash:              0.0
    tout_init:             30000
    tout_move:             120000
    tout_switch:           10000
  initialisation:
      sequence: ['FIND_LHW', 'FIND_UHW', 'CALIB_ABS', 'END']
      FIND_LHW:
         value1: 4.0
         value2: 4.0
      FIND_UHW:
         value1: 4.0
         value2: 4.0
      CALIB_ABS:
         value1: 0.0
         value2: 0.0
      END:
         value1: 0.0
         value2: 0.0
  positions:
     posnames: ['ON', 'OFF']
     tolerance: 1                              # Tolerance in UU
     ON: 30
     OFF: 100
""")

