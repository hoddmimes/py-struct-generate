# py-struct-generate
Utility for generating Python serializable message classes 

This utility is able to generate Python serializable message classes based upon XML definitions.
A simple _message_ definition could like. 

```
<Messages>
    <Message name="SubMessage" >
	   <Attribute name="subBool" type="bool"/>
	   <Attribute name="subString" type="str"/>
	   <Attribute name="subLong" type="long"/>
	</Message>

	<Message name="TestMessage">
		<Imports>
			<Import path="msg.generated" msgClass="SubMessage"/>
		</Imports>
		<Attribute name="intValue" type="int"/>
		<Attribute name="strValue" type="str"/>
		<Attribute name="stringArray" type="str" list="[]"/>
		<Attribute name="intArray" type="int" list="[]"/>
		<Attribute name="subMsgs" type="SubMessage" list="[]"/>
		<Attribute name="endValue" type="int"/>
	</Message>
<Messages>
```

The java program ./transform/src/main/java/PyTransform take one argument pointing 
at the XML defintions. The program will generate Python message corsponding message classes.

The simple defintions above are found in the directory [./transform/xml](https://github.com/hoddmimes/py-struct-generate/tree/main/transform/xml) 
and can be used to generate test message classes.

To generate you may execute the PyTransform program with the following command 
_**given that your working directory is ./transform**_

```
java -jar ../libs/pymessage-1.0.jar -xml ./xml/TestMessagesFileSet.xml 
```

The generated is found in the directory ./pymessage/net/generated/

- [SubMessage.py](https://github.com/hoddmimes/py-struct-generate/blob/main/pymessage/msg/generated/SubMessage.py)
- [TestMessage.py](https://github.com/hoddmimes/py-struct-generate/blob/main/pymessage/msg/generated/TestMessage.py)

Generated message classes can be generated in a single module file or one file per message class. The behaviour is 
controlled be the definitions in the program XML definition file. E.g.
```
<?xml version="1.0" encoding="UTF-8"?>
<MessageFiles>
	<MessageFile  file="./xml/TestMessage.xml" outPath="../pymessage/msg/generated/" package="msg.generated" allInOneFile="True"/>
</MessageFiles>
```

The parameter *__allInOneFile__* defines if generated message classes should be placed in separated modules files or 
a single file. In case all generated message classes are placed in one file, the name of the file will be equal to the
XML filename defining the message classes.

There is also trivial test program that illustrates how to use generated message classes
[./pymessage/test.py](https://github.com/hoddmimes/py-struct-generate/blob/main/pymessage/test.py)


_The rest is in the source._

