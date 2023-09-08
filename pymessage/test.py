import importlib

from msg.generated.test_messages import SubMessage, TestMessage
from msg.messageif import MessageBase


def createSubMessage(bool_value: bool, long_value:int, str_value: str) -> SubMessage:
    m = SubMessage()
    m.sub_string = str_value
    m.sub_long = long_value
    m.sub_bool = bool_value
    return m


def main():

    submsgs = []
    for i in range(3):
        submsgs.append( createSubMessage(bool_value=True, long_value=(12345678900 + i), str_value="sub message " + str(i)))

    int_lst = [1,2,3,4]
    str_lst = ['ett','two','three','four']
    tstmsg = TestMessage()
    tstmsg.sub_msgs = submsgs
    tstmsg.int_array = int_lst
    tstmsg.int_value = 42
    tstmsg.str_value = 'test message'
    tstmsg.string_array = str_lst
    tstmsg.end_value = 999

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