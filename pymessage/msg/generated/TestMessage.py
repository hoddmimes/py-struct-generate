
from msg.messageif import MessageBase
from msg.messages import MessageAux
from msg.decoder import Decoder
from msg.encoder import Encoder
from io import StringIO

            
        # Add XML defined imports
        
from msg.generated.SubMessage import SubMessage as SubMessage
class TestMessage( MessageBase ):

    def __init__(self):
        self.className = "msg.generated.TestMessage"
        
        self.intValue: int
        self.strValue: str
        self.stringArray: list
        self.intArray: list
        self.subMsgs: list
        self.endValue: int
    def setIntValue( self, value: int ):
        self.intValue = value

    def getIntValue( self ) -> int:
        return self.intValue
    def setStrValue( self, value: str ):
        self.strValue = value

    def getStrValue( self ) -> str:
        return self.strValue
    def setStringArray( self, value: list ):
        self.stringArray = value

    def getStringArray( self ) -> list:
        return self.stringArray
    def setIntArray( self, value: list ):
        self.intArray = value

    def getIntArray( self ) -> list:
        return self.intArray
    def setSubMsgs( self, value: list ):
        self.subMsgs = value

    def getSubMsgs( self ) -> list:
        return self.subMsgs
    def setEndValue( self, value: int ):
        self.endValue = value

    def getEndValue( self ) -> int:
        return self.endValue

    def toBytes(self) -> bytearray:
       return self.encode()

        
    def encode(self) -> bytearray:
        _encoder = Encoder()
        _encoder.addString( self.className )

        
        # Encode Attribute: intValue Type: int List: false
        _encoder.addInt( self.intValue )
        # Encode Attribute: strValue Type: str List: false
        _encoder.addString( self.strValue )
        # Encode Attribute: stringArray Type: str List: true
            # Encode str list
        MessageAux.addStringList( _encoder, self.stringArray  )
        # Encode Attribute: intArray Type: int List: true
            # Encode int list
        MessageAux.addIntList( _encoder, self.intArray  )
        # Encode Attribute: subMsgs Type: SubMessage List: true
        MessageAux.addMessageList( _encoder, self.subMsgs)
        # Encode Attribute: endValue Type: int List: false
        _encoder.addInt( self.endValue )
        return _encoder.get_bytes()


        
    def decode( self, buffer: bytearray):
        _decoder = Decoder( buffer )
        self.className = _decoder.getString()
        
        #Decode Attribute: intValue Type:int List: false
        self.intValue = _decoder.getInt()
        
        #Decode Attribute: strValue Type:str List: false
        self.strValue = _decoder.getString()
        
        #Decode Attribute: stringArray Type:str List: true
        self.stringArray = MessageAux.getStringList( _decoder )
        #Decode Attribute: intArray Type:int List: true
        self.intArray = MessageAux.getIntList( _decoder )
        #Decode Attribute: subMsgs Type:SubMessage List: true
        self.subMsgs = MessageAux.getMessageList( _decoder )
        #Decode Attribute: endValue Type:int List: false
        self.endValue = _decoder.getInt()
        

    def _blanks( self, _indent ) -> str:
        if _indent == 0:
          return ""
        else:
          return "                                             "[:_indent]

    def toString(self, _indent: int = 0 ) -> str:
        _buffer: StringIO = StringIO()
        
        _buffer.write(self._blanks( _indent ) + "intValue : " + str( self.intValue) + "\n")
        _buffer.write(self._blanks( _indent ) + "strValue : " + str( self.strValue) + "\n")
        _buffer.write(self._blanks( _indent ) + "stringArray : " + str( self.stringArray) + "\n")
        _buffer.write(self._blanks( _indent ) + "intArray : " + str( self.intArray) + "\n")
        if self.subMsgs is None:
           _buffer.write(self._blanks( _indent ) + "subMsgs : None \n")
        else:
                    
           _buffer.write(self._blanks( _indent ) + "subMsgs : \n")
           _idx = 0
           for _m in self.subMsgs:
                _idx += 1;
                _buffer.write( self._blanks( _indent + 2 ) + "[" + str(_idx) +"] \n" )
                _buffer.write( _m.toString( _indent + 4) + "\n") 
        _buffer.write(self._blanks( _indent ) + "endValue : " + str( self.endValue) + "\n")
        return _buffer.getvalue()

    def __str__(self) ->str:
        return self.toString()
    