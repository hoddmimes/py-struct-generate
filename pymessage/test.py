from msg.generated.SubMessage import SubMessage as SubMessage
from msg.generated.TestMessage import TestMessage as TestMessage
from msg.encoder import Encoder as Encoder
from msg.decoder import Decoder as Decoder
import importlib



def createSubMessage( boolValue: bool, longValue:int, strValue: str ) -> SubMessage:
    m = SubMessage()
    m.setSubString( strValue )
    m.setSubLong( longValue )
    m.setSubBool( boolValue )
    return m

def test():
    buffer = bytearray(300)
    ba1 = "abcdefghij".encode("utf-8")
    ba2 = "123456789".encode('utf-8')
    buffer[0:len(ba1)] = ba1
    buffer[len(ba1):len(ba1)+len(ba2)] = ba2

    print( str( buffer ))


def main():
    test()
    submsgs = []
    for i in range(3):
        submsgs.append( createSubMessage(True, (12345678900 + i), "sub message " + str(i)))

    int_lst = [1,2,3,4]
    str_lst = ['ett','two','three','four']
    tstmsg = TestMessage()
    tstmsg.setSubMsgs( submsgs)
    tstmsg.setIntArray( int_lst )
    tstmsg.setIntValue( 42 )
    tstmsg.setStrValue('test message')
    tstmsg.setStringArray(str_lst)
    tstmsg.setEndValue(999)

    print( tstmsg.toString())

    data = tstmsg.encode()
    print( str(data))

    xmsg = TestMessage()
    xmsg.decode( data )
    print( xmsg.toString())

if __name__ == '__main__':
    main()