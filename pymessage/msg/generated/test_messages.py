
from msg.messageif import MessageBase
from msg.messages import MessageAux
from msg.codec import Decoder
from msg.codec import Encoder
from io import StringIO
            
class SubMessage( MessageBase ):

    def __init__(self):
        
        self.classModule = "msg.generated.test_messages"
        self.className = "SubMessage"
        
        self._sub_bool: bool
        self._sub_string: str
        self._sub_long: int
    @property
    def sub_bool(self) -> bool:
        return self._sub_bool

    @sub_bool.setter
    def sub_bool(self, value: bool):
            self._sub_bool = value
        
    @property
    def sub_string(self) -> str:
        return self._sub_string

    @sub_string.setter
    def sub_string(self, value: str):
            self._sub_string = value
        
    @property
    def sub_long(self) -> int:
        return self._sub_long

    @sub_long.setter
    def sub_long(self, value: int):
            self._sub_long = value
        

    def toBytes(self) -> bytearray:
       return self.encode()

        
    def encode(self) -> bytearray:
        _encoder = Encoder()
        _encoder.addString(self.classModule)
        _encoder.addString(self.className)

        
        # Encode Attribute: sub_bool Type: bool List: false
        _encoder.addBool( self._sub_bool )
        # Encode Attribute: sub_string Type: str List: false
        _encoder.addString( self._sub_string )
        # Encode Attribute: sub_long Type: long List: false
        _encoder.addLong( self._sub_long )
        return _encoder.buffer


        
    def decode( self, buffer: bytearray):
        _decoder = Decoder( buffer )
        self.classModule = _decoder.getString()
        self.className = _decoder.getString()
        
        #Decode Attribute: sub_bool Type:bool List: false
        self._sub_bool = _decoder.getBool()
        
        #Decode Attribute: sub_string Type:str List: false
        self._sub_string = _decoder.getString()
        
        #Decode Attribute: sub_long Type:long List: false
        self._sub_long = _decoder.getLong()
        

    def _blanks( self, _indent ) -> str:
        if _indent == 0:
          return ""
        else:
          return "                                             "[:_indent]

    def toString(self, _indent: int = 0 ) -> str:
        _buffer: StringIO = StringIO()
        
        _buffer.write(self._blanks( _indent ) + "sub_bool : " + str( self.sub_bool) + "\n")
        _buffer.write(self._blanks( _indent ) + "sub_string : " + str( self.sub_string) + "\n")
        _buffer.write(self._blanks( _indent ) + "sub_long : " + str( self.sub_long) + "\n")
        return _buffer.getvalue()

    def __str__(self) ->str:
        return self.toString()
    
class TestMessage( MessageBase ):

    def __init__(self):
        
        self.classModule = "msg.generated.test_messages"
        self.className = "TestMessage"
        
        self._int_value: int
        self._str_value: str
        self._string_array: list
        self._int_array: list
        self._sub_msgs: list
        self._end_value: int
    @property
    def int_value(self) -> int:
        return self._int_value

    @int_value.setter
    def int_value(self, value: int):
            self._int_value = value
        
    @property
    def str_value(self) -> str:
        return self._str_value

    @str_value.setter
    def str_value(self, value: str):
            self._str_value = value
        
    @property
    def string_array(self) -> list:
        return self._string_array

    @string_array.setter
    def string_array(self, value: list):
        self._string_array = value
        
    @property
    def int_array(self) -> list:
        return self._int_array

    @int_array.setter
    def int_array(self, value: list):
        self._int_array = value
        

    @property
    def sub_msgs(self) -> list:
        return self._sub_msgs

    @sub_msgs.setter
    def sub_msgs(self, value: list):
        self._sub_msgs = value


        
    @property
    def end_value(self) -> int:
        return self._end_value

    @end_value.setter
    def end_value(self, value: int):
            self._end_value = value
        

    def toBytes(self) -> bytearray:
       return self.encode()

        
    def encode(self) -> bytearray:
        _encoder = Encoder()
        _encoder.addString(self.classModule)
        _encoder.addString(self.className)

        
        # Encode Attribute: int_value Type: int List: false
        _encoder.addInt( self._int_value )
        # Encode Attribute: str_value Type: str List: false
        _encoder.addString( self._str_value )
        # Encode Attribute: string_array Type: str List: true
            # Encode str list
        MessageAux.addStringList( _encoder, self._string_array  )
        # Encode Attribute: int_array Type: int List: true
            # Encode int list
        MessageAux.addIntList( _encoder, self._int_array  )
        # Encode Attribute: sub_msgs Type: SubMessage List: true
        MessageAux.addMessageList( _encoder, self._sub_msgs)
        # Encode Attribute: end_value Type: int List: false
        _encoder.addInt( self._end_value )
        return _encoder.buffer


        
    def decode( self, buffer: bytearray):
        _decoder = Decoder( buffer )
        self.classModule = _decoder.getString()
        self.className = _decoder.getString()
        
        #Decode Attribute: int_value Type:int List: false
        self._int_value = _decoder.getInt()
        
        #Decode Attribute: str_value Type:str List: false
        self._str_value = _decoder.getString()
        
        #Decode Attribute: string_array Type:str List: true
        self._string_array = MessageAux.getStringList( _decoder )
        #Decode Attribute: int_array Type:int List: true
        self._int_array = MessageAux.getIntList( _decoder )
        #Decode Attribute: sub_msgs Type:SubMessage List: true
        self._sub_msgs = MessageAux.getMessageList( _decoder )
        #Decode Attribute: end_value Type:int List: false
        self._end_value = _decoder.getInt()
        

    def _blanks( self, _indent ) -> str:
        if _indent == 0:
          return ""
        else:
          return "                                             "[:_indent]

    def toString(self, _indent: int = 0 ) -> str:
        _buffer: StringIO = StringIO()
        
        _buffer.write(self._blanks( _indent ) + "int_value : " + str( self.int_value) + "\n")
        _buffer.write(self._blanks( _indent ) + "str_value : " + str( self.str_value) + "\n")
        _buffer.write(self._blanks( _indent ) + "string_array : " + str( self.string_array) + "\n")
        _buffer.write(self._blanks( _indent ) + "int_array : " + str( self.int_array) + "\n")
        if self.sub_msgs is None:
           _buffer.write(self._blanks( _indent ) + "sub_msgs : None \n")
        else:
                    
           _buffer.write(self._blanks( _indent ) + "sub_msgs : \n")
           _idx = 0
           for _m in self.sub_msgs:
                _idx += 1;
                _buffer.write( self._blanks( _indent + 2 ) + "[" + str(_idx) +"] \n" )
                _buffer.write( _m.toString( _indent + 4) + "\n") 
        _buffer.write(self._blanks( _indent ) + "end_value : " + str( self.end_value) + "\n")
        return _buffer.getvalue()

    def __str__(self) ->str:
        return self.toString()
    