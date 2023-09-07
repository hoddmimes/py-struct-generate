import importlib

from msg.generated.test_messages import SubMessage, TestMessage
from msg.messageif import MessageBase


def createSubMessage( boolValue: bool, longValue:int, strValue: str ) -> SubMessage:
    m = SubMessage()
    m.subString = strValue
    m.subLong = longValue
    m.subBool = boolValue
    return m


def main():

    submsgs = []
    for i in range(3):
        submsgs.append( createSubMessage(True, (12345678900 + i), "sub message " + str(i)))

    int_lst = [1,2,3,4]
    str_lst = ['ett','two','three','four']
    tstmsg = TestMessage()
    tstmsg.subMsgs = submsgs
    tstmsg.intArray = int_lst
    tstmsg.intValue = 42
    tstmsg.strValue = 'test message'
    tstmsg.stringArray = str_lst
    tstmsg.endValue = 999

    print('########## Print instansiated TestMessage ###########')
    print( tstmsg )

    data = tstmsg.encode()
    print('\n\n########## Print encoded bytearray of the TestMessage ###########')
    print( str(data))
    print('decoded message length: ' + str(len(data)) + 'bytes')

    xmsg = TestMessage()
    xmsg.decode( data )
    print('\n\n########## Print decoded bytearray of the TestMessage ###########')
    print( xmsg )

if __name__ == '__main__':
    main()