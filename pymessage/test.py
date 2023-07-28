from msg.generated.SubMessage import SubMessage as SubMessage
from msg.generated.TestMessage import TestMessage as TestMessage




def createSubMessage( boolValue: bool, longValue:int, strValue: str ) -> SubMessage:
    m = SubMessage()
    m.setSubString( strValue )
    m.setSubLong( longValue )
    m.setSubBool( boolValue )
    return m


def main():

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

    print('########## Print instansiated TestMessage ###########')
    print( tstmsg.toString())

    data = tstmsg.encode()
    print('\n\n########## Print encoded bytearray of the TestMessage ###########')
    print( str(data))
    print('decoded message length: ' + str(len(data)) + 'bytes')

    xmsg = TestMessage()
    xmsg.decode( data )
    print('\n\n########## Print decoded bytearray of the TestMessage ###########')
    print( xmsg.toString())

if __name__ == '__main__':
    main()