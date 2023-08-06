from .device import Device, _name_attr, GROUP
from . import trk
from .motor import Motor
from . import keys as K
from .interface import Int16, nodealiasproperty, kjoin
from .manager import Manager # see at the end of file
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
# RPC error
@_name_attr
class RPC_ERROR(trk.RPC_ERROR):
    txt = {
        # add more rpc error description here if necessary @_name_attr takes care of the ones in master class
    }

### ##############
# errors
@_name_attr
class ERROR(trk.ERROR):
    txt = {
        # add more  error description here if necessary @_name_attr takes care of the ones in master class
    }


### ##############
# errors
@_name_attr
class AXIS:
    ALL_AXIS = 0
    AXIS1 = 1
    AXIS2 = 2



### ############# 
# Mode 
@_name_attr
class MODE:
    ENG   = 0 
    OFF   = 1
    AUTO  = 2
    group = {
        ENG		: GROUP.ENG,
        OFF	    : GROUP.STATIC,
        AUTO	: GROUP.TRACKING,
    }
#  _       _             __                
# (_)_ __ | |_ ___ _ __ / _| __ _  ___ ___ 
# | | '_ \| __/ _ \ '__| |_ / _` |/ __/ _ \
# | | | | | ||  __/ |  |  _| (_| | (_|  __/
# |_|_| |_|\__\___|_|  |_|  \__,_|\___\___|

class AdcStatInterface(Device.StatInterface):
    ERROR = ERROR
    MODE = MODE
    SUBSTATE = SUBSTATE
    @nodealiasproperty("track_mode_txt", ["track_mode"])
    def track_mode_txt(self, track_mode):
        return self.MODE.txt.get(track_mode, "UNKNOWN")
        
    
    
    
class AdcCfgInterface(Device.CfgInterface):
    # we can define the type to parse value directly on the class by annotation
    pass

# redefine the Method interface to include the proper description of the RpcError
class AdcRpcNode(Device.RpcInterface.RpcNode):
    RPC_ERROR = RPC_ERROR

class AdcRpcInterface(Device.RpcInterface):
    RpcNode = AdcRpcNode
    RPC_ERROR = RPC_ERROR
    ##
    # the type of rpcMethod argument can be defined by annotation
    # All method args types must be defined in a tuple
    rpcMoveAbs :  (Int16, float, float)
    rpcMoveRel :  (Int16, float, float)
    rpcMoveAngle: (float,)
    rpcMoveVel:   (Int16, float,)
    rpcStartTrack : (float,)
    
#      _            _          
#   __| | _____   _(_) ___ ___ 
#  / _` |/ _ \ \ / / |/ __/ _ \
# | (_| |  __/\ V /| | (_|  __/
#  \__,_|\___| \_/ |_|\___\___|
#
class Adc(Device,trk.Trk):
    SUBSTATE = SUBSTATE
    MODE = MODE 
    ERROR = ERROR 
    
    RpcInterface  = AdcRpcInterface
    StatInterface = AdcStatInterface
    CfgInterface  = AdcCfgInterface
    
    def __init__(self, *args, **kwargs):
        super(Adc, self).__init__(*args, **kwargs)
        
        axes = self._config['ctrl_config'].get('axes', [])
        motors = []
        for axis in axes:
            axis_conf = self._config[axis]
            name = axis_conf.get('prefix', None)
            motors.append(Motor.from_config(axis_conf['cfgfile'], axis, key=kjoin(self.key, name)) )
        self.motors = motors    
    
    @property
    def motor1(self):
        return self.motors[0]
    
    @property
    def motor2(self):
        return self.motors[1]
    
    def connect(self):
        """ Connect all opc-ua client to servers """
        super(Adc, self).connect()
        for m in self.motors:
            m.connect()
    
    def disconnect(self):
        """ Disconnect client frmo their servers """
        super(Adc, self).disconnect()
        for m in self.motors:
            m.disconnect()
        
    def get_configuration(self):
        """  return a node/value pair dictionary ready to be uploaded 
        
        The node/value dictionary represent the device configuration. 
        """
        cfg_dict = {}
        for m in self.motors:
            cfg_dict.update( m.get_configuration() )
        
        config = self._config 
        
        ctrl_config = config.get(K.CTRL_CONFIG, {})  
        # just update what is in ctrl_config, except axes      
        cfg_dict.update( {self.cfg.get_node(k):v for k,v in ctrl_config.items() if k not in ["axes"]} ) 
        return cfg_dict
    
    def stop(self):
        """ Stop all ADC motions """
        self.rpc.rpcStop.rcall()
    
    def start_track(self, angle=0.0):
        """ Start tracking (AUTO mode)
        
        Args:
            angle (float, optional): target angle default = 0.0
        """
        self.rpc.rpcStartTrack.rcall(angle)
    
    def move_angle(self, angle=0.0):
        """ Move to angle  (OFF mode)
        
        Args:
            angle (float, optional): target angle default = 0.0
        """
        self.rpc.rpcMoveAngle.rcall(angle)
    
    def move_abs(self, axis, pos, vel):
        """ Move one or all motor to an absolute  position 
        
        Args:
            axis (int): 0 for all motors 1 for axis 1 and 2 for axis 2
            pos (float): target absolute position 
            vel (float): target velocity 
        """
        self.rpc.rpcMoveAbs.rcall(axis, pos, vel)
    
    def move_rel(self, axis, pos, vel):
        """ Move one or all motor to an relative position 
        
        Args:
            axis (int): 0 for all motors 1 for axis 1 and 2 for axis 2
            pos (float): target relative position 
            vel (float): target velocity 
        """
        self.rpc.rpcMoveRel.rcall(axis, pos, vel)
    

    def move_vel(self, axis, vel):
        """ Move one or all motor in velocity 
        
        Args:
            axis (int): 0 for all motors 1 for axis 1 and 2 for axis 2
            vel (float): target velocity 
        """
        self.rpc.rpcMoveVel.rcall(axis, vel)
    

    
Manager.record_new_device_type('Adc', Adc)


Manager.record_cfg_template('Adc', """{name}:
  type: Adc
  interface: Softing
  identifier: PLC1                            # OPCUA Object Identifier
  prefix: MAIN_FAST.adc                       # TO BE UPDATED OPCUA attribute prefix
  simulated: false
  ignored: false
  address: {address}
  simaddr: opc.tcp://134.171.57.209:4840       # Simulation address
  mapfile: "{cfg_dir}/mapAdc.yml"      # TO BE UPDATED
  fits_prefix: "ADC1"
  ctrl_config:
    latitude:              -0.429833092
    longitude:             1.228800386
    axes: ['adc1_motor1', 'adc1_motor2']

  adc1_motor1:
      prefix: "motor1"
      cfgfile: "{cfg_dir}/adc1Motor1.yml" # TO BE UPDATED
  adc1_motor2:
      prefix: "motor2"
      cfgfile: "{cfg_dir}/adc1Motor2.yml" # TO BE UPDATED
""")

