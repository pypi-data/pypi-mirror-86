#!/usr/bin/env python
## @package ca: EPICS-CA interface module for Python.
"""
CA modlue : EPICS-CA interface module for Python.
This module provide a  version of EPICS-CA and Python interface.
It users C module _ca. _ca module basically maps C-API in EPICS ca library into python. Interface between ca.py and _ca module is  subject for change. You should not depend on it. API in ca.py will be preserved in future releases as much as possible.
Author: Noboru Yamamoto, KEK, JAPAN. -2007.
$Revision: b4d07ff54edb $
"""
__version__ = "$Revision: b4d07ff54edb $"
# $Source: /opt/epics/R314/modules/soft/kekb/python/PythonCA-dev/_ca_kek.py $
#
try:
    import signal
except:
    print ("signal module is not avaialble")

from sys import version_info
import time
import atexit
import math

# Force thread module to call PyEval_InitThread in it.
import threading
threading.Thread().start()

# import binary module
import _ca

# version from _ca314.cpp
version=_ca.version
__version__ = "{version:s}".format(version=version)
revision=_ca.revision
release=_ca.release
hg_release=_ca.hg_release
ca_version=_ca.ca_version

# some constants for EPICS channel Access library
from cadefs import *
from caError import *


if version_info >= (3,):
    def printfn(x):
        print(x)
else:
    from printfn import printfn

#export pend_xxx routines for global operation
pendio =_ca.pendio
pend_io=_ca.pendio
pend_event=_ca.pend_event
poll=_ca.poll
poll_event=_ca.poll
flush_io=_ca.flush
flush=_ca.flush
test_io=_ca.test_io # test_io retunrs 42 for IODONE , 43 for IOINPROGRESS
add_fd_registration=_ca.add_fd_registration

#Error Object
error=_ca.error
shutdown=_ca.__ca_task_exit

#private dictionary for Get/Put functions

__ca_dict={}
#__ca_dict_lock=thread.allocate_lock()
__ca_dict_lock=threading.Lock()
_channel__debug=False

class channel(object):
    """
    a channel object for EPICS Channel Access.

    It does not have direct connection
    to channel object in C-library for EPICS Channel Access. 
    for creation just supply channel name to connect
    """
    dbr_types=(
        DBR_NATIVE, # default type
        DBR_STRING, DBR_CHAR, DBR_FLOAT,
        DBR_SHORT, #/* same as DBR_INT */
        DBR_ENUM, DBR_LONG, DBR_DOUBLE,
        DBR_TIME_STRING, DBR_TIME_CHAR, DBR_TIME_FLOAT,
        DBR_TIME_SHORT, #:/* same as DBR_TIME_INT */
        DBR_TIME_ENUM, DBR_TIME_LONG, DBR_TIME_DOUBLE,
        DBR_CTRL_CHAR, DBR_CTRL_LONG,
        DBR_CTRL_ENUM, DBR_CTRL_DOUBLE
        )

    def __init__(self, name, cb=None,noflush=False):
        if not cb : cb=self.update_info
        if name == "":
            raise ValueError( name)
        self.name=name
        self.field_type = None
        self.element_count = None
        self.puser = None
        self.conn_state = -1
        self.hostname = None
        self.raccess = None
        self.waccess = None
        self.sevr=None
        self.ts=None
        self.status=None
        self.evid=[]
        self.autoEvid=None
        self.__callbacks={}
        self.cbstate=None
        self.updated=False
        self.val=None
        self.oval=None
        self.ctrl=None
        self.chid=_ca.search(name,cb)
        if not noflush:
            self.flush()

    def clear(self):
        if self.chid:
            self.clear_monitor()
            self.flush()
            _ca.clear(self.chid)
            self.flush()
        self.chid=None
 
    def __del__(self):
        self.clear()

    def wait_conn(self, wait=20, dt=0.05):
        n=0
        self.pend_event(dt)
        self.poll()
        while not self.isConnected():
            self.pend_event(dt)
            n=n+1
            if (n > wait ) :
                raise  ECA_BADCHID("%s %d"%(self.name,n))
                return -1
        
    def get(self,cb=None,Type=DBR_NATIVE, count=0, type=DBR_NATIVE, type_=DBR_NATIVE):
        try:
            if not self.isConnected():
                raise ECA_BADCHID(self.name)
        except:
            raise ECA_BADCHID(self.name)
        if (Type == DBR_NATIVE):
            if not(type == DBR_NATIVE):
                Type=type
            elif not(type_ == DBR_NATIVE):
                Type=type_
        rType=max(Type,type,type_)
        if rType not in self.dbr_types:
            raise TypeError( rType)
        if not cb: cb=self.update_val

        self.cbstate=None
        self.updated=False
        try:
            _ca.get(self.chid, cb, Type, count)
        finally:
            pass

    def put(self,*val,**kw):
        """
        channel.put(valu) will put scalar value to channel. You may need to call channel.flush()
        
        """
        if  val == () :
            printfn ("No value(s) to put")
        else:
            if 'cb' in kw :
                cb=kw['cb']
            else:
                cb=None
            #self.__lock.acquire()
            if 'dtype' in kw :
                dtype=kw['dtype']
            elif 'Type' in kw :
                dtype=kw['Type']
            elif 'type_' in kw :
                dtype=kw['type_']
            elif 'type' in kw :
                dtype=kw['type']
            else:
                dtype=DBR_NATIVE

            try:
                _ca.put(self.chid, val, self.val, cb, dtype)
            finally:
                pass

    def add_instance_method(self, func, name=None):
        """
        arguments: func, name
        register func as an instance method of self.
        name of func will be used if name is not give as an argument.
        
        """
        from types import MethodType

        assert callable(func)
        # func : (self, args)
        if (name is None):
            name=self.name
        setattr(self, name, MethodType(func,self,channel))
        
    def put_and_notify(self,*val,**kw):
        if 'cb' in kw :
            cb=kw['cb']
        else:
            cb=None # ca_put_array_callback does not return value.
        if ('dtype' in kw):
            dtype=kw['dtype']
        elif ('Type' in kw):
            dtype=kw['Type']
        elif ('type_' in kw):
            dtype=kw['type_']
        elif ('type' in kw):
            dtype=kw['type']
        else:
            dtype=DBR_NATIVE

        if( val == ()):
            printfn ("No value(s) to put")
        else:
            #self.__lock.acquire()
            try:
                _ca.put(self.chid,val,self.val,cb, dtype)
            finally:
                #self.__lock.release()
                pass

    def monitor(self,callback=None,count=0,evmask=(DBE_VALUE|DBE_ALARM)):
        """
        A callback routine will be called with 
        a tuple (value, severity, status, timestamp, [control]) 
        as the first argument.
        def ch_cb(valstat): # as fuction
            ....
        """
        if(not callback):
            raise PyCa_NoCallback
        if (self.conn_state != 2):
            #printfn( self.name,self.get_info())
            raise ECA_BADCHID(self.name)

        self.update_info()
        if (self.field_type == DBR_NATIVE):
            #printfn( self.name,self.get_info())
            raise ECA_BADTYPE(self.name)
        self.evid.append(_ca.monitor(self.chid, callback, count, evmask))
        self.__callbacks[self.evid[-1]]=callback
        return self.evid[-1]
    
    def __clear_event(self,evid):
        if(__debug): printfn(("clearing evid:",evid))
        _ca.clear_monitor(evid)
        del self.__callbacks[evid]
         
    def clear_monitor(self,evid=None):
        if(evid):
            if ( evid in self.evid):
                self.__clear_event(evid)
                i=self.evid.index(evid)
                del self.evid[i]
        else:
            for evid in self.evid:
                self.__clear_event(evid) 
            self.evid=[]

    def autoUpdate(self):
        if self.autoEvid == None:
            self.monitor(self.update_val)
            self.autoEvid=self.evid[-1]
        self.flush()
        
    def clearAutoUpdate(self):
        if self.autoEvid != None:
            self.clear_monitor(self.autoEvid)
            self.autoEvid=None
        self.flush()
        
    def pendio(self,tmo=0.001):
        v=_ca.pendio(float(tmo))
        return v

    def pend_io(self,tmo=0.001):
        v=_ca.pendio(float(tmo))
        return v

    def pend_event(self,tmo=0.001):
        v=_ca.pend_event(float(tmo))
        return v

    def poll(self):
        _ca.poll()
            
    def flush(self,wait=0.001):
        v=_ca.flush(wait)
        return v

    def update_val(self,valstat=None):
        if (valstat == None):
            raise caError("No value")
        #self.__lock.acquire()
        try:
            self.oval=self.val
            self.val=valstat[0]
            self.sevr=valstat[1]
            self.status=valstat[2]
            self.cbstate=1
            try:
                self.ts=valstat[3]
            except:
                pass
            try:
                self.ctrl=valstat[4]
            except:
                pass
        finally:
            #self.__lock.release()
            self.updated=True
            pass

    def clear_cbstate(self):
        #self.__lock.acquire()
        self.cbstate=None
        #self.__lock.release()
        
    def state(self):
        self.get_info()
        return (self.conn_state - ch_state.cs_conn)

    def ca_status(self):
        return _ca.status(self.chid)

    def v42_ok(self):
        return _ca.ca_v42_ok(self.chid)

    def isNeverConnected(self):
        self.get_info()
        return (self.conn_state == ch_state.cs_never_conn)

    def isConnected(self):
        self.get_info()
        return (self.conn_state == ch_state.cs_conn)

    def isPreviouslyConnected(self):
        self.get_info()
        return (self.conn_state == ch_state.cs_prev_conn)

    def isDisonnected(self):
        self.get_info()
        return (self.conn_state == ch_state.cs_prev_conn)
    
    def isClosed(self):
        self.get_info()
        return (self.conn_state == ch_state.cs_closed)
    
    def get_info(self):
        """
        update channel status information. return channel staus as a tuple.
        """
        #self.__lock.acquire()
        try:
            info=_ca.ch_info(self.chid)
            (self.field_type, self.element_count, self.puser,
             self.conn_state, self.hostname, self.raccess,
             self.waccess) = info
        finally:
            #self.__lock.release()
            pass
        return info

    def update_info(self):
        """
        Just update channel status information. No return value. 
        """
        self.get_info()

    def fileno(self):
        """returns socket number used to connect.Scoket id is shared by
        channels which are connected to the same IOC.
        It became obsolete in EPICS 3.14 version of Python-CA.
        You need to use fd_register function. But you may not need it anyway in multi-thread environment.
        """
        return _ca.fileno(self.chid)

# convenient functions
# you need to call Clear() function before stopping Python, otherwise it cause coredump. 2009/2/11 NY
# -> ClearAll() call is  registered as an atexit function.

def __Ch(name,tmo=0.01):
    if isinstance(name,(bytes,str)):
        if ((name in __ca_dict)):
            ch=__ca_dict[name]
        else:
            try:
                ch=channel(name)
                ch.wait_conn()
            except:
                raise ECA_BADCHID(name)
            tmo=20*tmo
            __ca_dict_lock.acquire()
            try:
                __ca_dict[name]=ch
            finally:
                __ca_dict_lock.release()
        if( ch.state() != 0):
            ch.wait_conn(10)
        return ch
    else:
        raise ECA_BADTYPE(name)

def Info(name = "",tmo=0.01):
    """
    returns a tuple as channel information.
    tuple format=(field_type, element_count, puser argument,
                  connection_status, hostname:port,
                  read access mode, write access mode)
    """
    ch=__Ch(name,tmo=tmo)
    return ch.get_info()

def ClearAll():
    for name in list(__ca_dict.keys()):
        Clear(name)

# __ca_dict should be cleared before Stopping Python
atexit.register(ClearAll)

def Clear(name= ""):
    if isinstance(name,(bytes,str)):
        __ca_dict_lock.acquire()
        try:
            if ((name in __ca_dict)):
                ch=__ca_dict[name]
                del __ca_dict[name]
                ch.clear()
                del ch
            else:
                __ca_dict_lock.release()
                raise ECA_BADTYPE(name)
        finally:
            __ca_dict_lock.release()
    else:
        raise ECA_BADTYPE(name)

def Get(name="",count=0,Type=DBR_NATIVE,tmo=0.01,maxtmo=3):
    """
    Get value from a channel "name".
    """
    ch=__Ch(name,tmo)
    def CB(vals,ch=ch):
        ch.update_val(vals)
    ch.get(cb=CB,Type=Type,count=count)
    ch.flush()
    while not ch.updated:
        time.sleep(tmo)
        maxtmo -=tmo
        if maxtmo <=0:
            raise caError("No get response")
    return ch.val

def GetChannel(name="",tmo=0.01):
    """
    Get channel object from a channel "name".
    """
    ch=__Ch(name,tmo)
    return ch

def Put_and_Notify(name,val=None,cb=None,dtype=DBR_NATIVE):
    """
    Convenient function:Put_and_Notify 

    calls put_and_notify with callback. 
    If callback is None, then just put data to a channel.
    """
    ch=__Ch(name,tmo=0.1)
    ch.put_and_notify(val,cb=cb,dtype=dtype)
    ch.flush()
    return ch.val

# define synonym
Put=Put_and_Notify

def Put_and_Notify_Array(name,val,cb=None,dtype=DBR_NATIVE):
    """
    put array test version : not tested with string arrays yet
    2007.8.30 T. Matsumoto
    """
    ch=__Ch(name,tmo=0.1)
    ch.put_and_notify(*val,**dict(cb=cb,dtype=dtype))
    ch.flush()
    return ch.val

# define synonym
Put_Array=Put_and_Notify_Array
                
def Monitor(name,cb=None,evmask=(DBE_VALUE|DBE_ALARM)):
    """
    monitor channel of given name and print its value and status.
    callback function can be specified. Callback function should take two arguments, channel object and monitored value.
    def cb(ch, val):
        < describe your task with channel ch and value>
    note that this API is diffrent from the callback for channle.monitor().
    """
    ch=__Ch(name,tmo=0.1)
    if not cb:
        def myCB(val,ch=ch):
            printfn((ch.name,":",val[0],val[1],val[2],TS2Ascii(val[3])))
    else:
        def myCB(val, ch=ch, cb=cb):
            cb(ch,val)
            
    ch.clear_monitor()
    evid=ch.monitor(myCB,evmask=evmask)
    ch.flush()
    return evid

def ClearMonitor(name,evid=None):
    ch=__Ch(name,tmo=0.1)
    try:
        ch.clear_monitor(evid)
        return
    except:
        raise ECA_BADCHID(name)
#
def isIODone():
    if _ca.test_io()== 42:
        return 1
    else:
        return 0
#
# syncronus group class
# Author: N.Yamamoto 
# Date: May 27.1999 (first version)
# 2009/03/03 : serious bug in get/put was fixed. NY
# now it should work
# 2018/01/05 : __init__ accept channel/channel name  object/list
#              add also accept these.

class SyncGroup(object):
    """
    sg_array_get/sg_put/sg_array_put are not implemented yet.
    ca_sg_delte may be used in __del__ method.
    """
    def __init__(self, *chs):
        self.gid=_ca.sg_create()
        self.chs={}
        if chs:
            self.add(chs)

    def __iter__(self):
        """
        sg object can be used in for-loop, etc.
        """
        return iter(self.chs)

    def values(self):
        """
        return a list of values for each registered channels.
        """
        return (c.val for c in self.chs)
    
    def _add(self,ch):
        """
        an utility function:add channel object
        """
        assert(isinstance(ch, channel))
        if(ch not in self.chs):
            self.chs[ch]=0
        
    def add(self, chs):
        """
        chs: list of channel objects
             or list of channel names
        """
        if isinstance(chs, channel): # chs is 
            self._add(chs)
            return
        elif isinstance(chs,str): # chs is a string
            ch=channel(chs)
            ch.flush()
            ch.wait_conn()
            self._add(ch)
            return
        try: # assuming that chs is a iterable of strings or channel objects.
            for ch in chs:
                if isinstance(ch, str ):
                    ch=channel(ch)
                    ch.flush()
                    ch.wait_conn()
                self._add(ch)
        except:
            raise RuntimeError("Invalid input")

    def test(self):
        return _ca.sg_test(self.gid)

    def reset(self):
        return _ca.sg_reset(self.gid)

    def wait(self,tmo=1.0):
        return _ca.sg_block(self.gid, float(tmo))

    def block(self,tmo=1.0):
        return _ca.sg_block(self.gid, float(tmo))

    def put(self,ch, *value, **kw):
        Type=kw.get("Type",
                    kw.get("dtype",
                           DBR_NATIVE))
        if (ch in self.chs):
            self.chs[ch]=_ca.sg_put(self.gid, ch.chid,
                        self.chs[ch], value , Type)

    def get(self,ch):
        if (ch in self.chs):
            self.chs[ch]=_ca.sg_get(self.gid,
                                    ch.chid, self.chs[ch])
        else:
            raise IndexError("channels {} is not registered to SyncGroup".format(ch.name))

    def stat(self):
        _ca.sg_stat(self.gid)
        
    def convert(self,ch):
        if (ch in self.chs):
            val=_ca.ca_convert(ch.chid, self.chs[ch])
            ch.update_val(val[0])
            
    def convertAll(self):
        for ch in self.chs:
            val=_ca.ca_convert(ch.chid, self.chs[ch])
            ch.update_val(val[0])
            
    def requestAll(self):
        for ch in self.chs:
            self.chs[ch] =_ca.sg_get(self.gid,
                                     ch.chid, self.chs[ch])

    def GetAll(self,tmo=1.0):
        """
        request new values for all registered channels.
        It also shows an example of get-wait(block)-convert usage.
        """
        self.reset()
        self.requestAll()
        flush()
        st=self.wait(tmo)
        if st == 0:
            self.convertAll()
        else:
            raise caError("CA_SG time out")

# TimeStamp utilities
# time.gmtime(631152000.0)=(1990, 1, 1, 0, 0, 0, 0, 1, 0) # i.e. EPICS TS EPOCH
#
__EPICS_TS_EPOCH=631152000.0

def TS2Ascii(ts):
    tstr=time.ctime(ts+__EPICS_TS_EPOCH)
    nsstr=".%03d"%(math.modf(ts + __EPICS_TS_EPOCH)[0]*1000)
    return tstr[:-5]+nsstr+tstr[-5:]

def TS2time(ts):
    return time.localtime(ts+__EPICS_TS_EPOCH)

def TS2UTC(ts):
    return (ts+__EPICS_TS_EPOCH)
