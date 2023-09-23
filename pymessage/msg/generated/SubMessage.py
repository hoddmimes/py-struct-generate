
from pymessage.msg.messageif import MessageBase
from pymessage.msg.messages import MessageAux
from pymessage.msg.codec import Decoder
from pymessage.msg.codec import Encoder
from io import StringIO

            
class SubMessage( MessageBase ):

    def __init__(self):
        
        self.classModule = "pymessage.msg.generated.SubMessage"
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
    