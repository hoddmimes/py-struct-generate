<xsl:stylesheet version="3.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:map="http://www.w3.org/2005/xpath-functions/map"
                xmlns:functx="http://www.functx.com"
                exclude-result-prefixes="map">


    <xsl:output method="text"/>
    <xsl:param name="outPath"/>
    <xsl:param name="corePackage"/>
    <xsl:param name="package"/>
    <xsl:param name="inputXml"/>
    <xsl:param name="inputXsl"/>
    <xsl:param name="comments"/>
    <xsl:param name="allInOneFile"/>

    <xsl:include href="functx-1.0.1.xsl"/>

    <xsl:variable name="singleFile">
        <xsl:call-template name="isSingleFile"/>
    </xsl:variable>

    <xsl:variable name="singleFileName">
        <xsl:call-template name="getXmlFileName"/>
    </xsl:variable>

    <!--  ============================================== -->
    <!--  				Define JAVA data types 			 -->
    <!--  ============================================== -->


    <xsl:variable name="TypeTableDefinitions">
        <DataTypes>
            <Type name="bool" type="bool" arrayEncoder="MessageAux.addBoolList" arrayDecoder="MessageAux.getBoolList" encoder="addBool" decoder="getBool" />
            <Type name="byte" type="int" arrayEncoder="MessageAux.addByteList" arrayDecoder="MessageAux.getByteList" encoder="addByte" decoder="getByte" />
            <Type name="short" type="int" arrayEncoder="MessageAux.addShortList" arrayDecoder="MessageAux.getShortList" encoder="addShort" decoder="getShort" />
            <Type name="int" type="int" arrayEncoder="MessageAux.addIntList" arrayDecoder="MessageAux.getIntList" encoder="addInt" decoder="getInt" />
            <Type name="long" type="int" arrayEncoder="MessageAux.addLongList" arrayDecoder="MessageAux.getLongList" encoder="addLong" decoder="getLong" />
            <Type name="double" type="float" arrayEncoder="MessageAux.addDoubleList" arrayDecoder="MessageAux.getDoubleList" encoder="addDouble" decoder="getDouble" />
            <Type name="str" type="str" arrayEncoder="MessageAux.addStringList" arrayDecoder="MessageAux.getStringList" encoder="addString" decoder="getString" />
            <Type name="byte[]" type="bytearray" arrayEncoder="MessageAux.addBytesList" arrayDecoder="MessageAux.getBytesList" encoder="addBytes" decoder="getBytes"/>
        </DataTypes>
    </xsl:variable>

    <xsl:variable name="typeTable" select="//$TypeTableDefinitions/DataTypes"/>






    <!--     ===================================================== -->
    <!--    Generate Java message objects for all messages defined -->
    <!--     ===================================================== -->

    <xsl:template match="/Messages">   <!-- <xsl:message>all-in-one-file: <xsl:value-of select="$allInOneFile"/> outpath: <xsl:value-of select="$outPath"/> xsl: <xsl:value-of select="$inputXsl"/> package: <xsl:value-of select="$package"/> comment: <xsl:value-of select="$comments"/> xml: <xsl:value-of select="$inputXml"/> </xsl:message> -->

        <xsl:if test="$singleFile = false()">
            <xsl:for-each select="Message">
                <xsl:variable name="file" select="concat('file://',$outPath,@name,'.py')"/>
                <xsl:result-document href="{$file}" method="text" omit-xml-declaration="yes" encoding="utf-8">
                    <xsl:apply-templates mode="generateMessage" select="."/>
                    <xsl:message>Created file <xsl:value-of select="$file"/></xsl:message>
                </xsl:result-document>
            </xsl:for-each>
        </xsl:if>

        <xsl:if test="$singleFile = true()">
            <xsl:variable name="file" select="concat('file://',$outPath,$singleFileName,'.py')"/>
            <xsl:result-document href="{$file}" method="text" omit-xml-declaration="yes" encoding="utf-8">
from <xsl:value-of select="$corePackage"/>.messageif import MessageBase
from <xsl:value-of select="$corePackage"/>.messages import MessageAux
from <xsl:value-of select="$corePackage"/>.decoder import Decoder
from msg.encoder import Encoder
from io import StringIO
            <xsl:for-each select="Message">
                <xsl:apply-templates mode="generateMessage" select="."/>
            </xsl:for-each>
            <xsl:message>Created file <xsl:value-of select="$file"/></xsl:message>
            </xsl:result-document>
        </xsl:if>
    </xsl:template>


    <xsl:template name="getXmlFileName">
        <xsl:analyze-string select="$inputXml"
                            regex="(.*/)?(\w+)\.xml$">
            <xsl:matching-substring>
                <xsl:value-of select="regex-group(2)"/>
            </xsl:matching-substring>
        </xsl:analyze-string>
    </xsl:template>

    <xsl:template name="isSingleFile">
        <xsl:if test="lower-case($allInOneFile) eq 'true'">
            <xsl:value-of select="true()"/>
        </xsl:if>
        <xsl:if test="lower-case($allInOneFile) eq 'false'">
            <xsl:value-of select="false()"/>
        </xsl:if>
    </xsl:template>


    <!--     ============================================== -->
    <!--     			      Import templates							   -->
    <!--     ============================================== -->

    <xsl:template mode="addImports" match="Imports">
        # Add XML defined imports
        <xsl:for-each select="Import">
            <xsl:if test="string-length(@path) &gt; 0">
from <xsl:value-of select="@path"/>.<xsl:value-of select="@msgClass"/> import <xsl:value-of select="@msgClass"/> as <xsl:value-of select="@msgClass"/></xsl:if>
            <xsl:if test="not(string-length(@path) &gt; 0)">
from <xsl:value-of select="@msgClass"/> import <xsl:value-of select="@msgClass"/> as <xsl:value-of select="@msgClass"/></xsl:if>
        </xsl:for-each>
    </xsl:template>





    <!--     ============================================== -->
    <!--     			      Generate Message Class	    -->
    <!--     ============================================== -->
    <xsl:template mode="generateMessage" match="Message">
        <xsl:param name="separateFile"/>

<xsl:if test="$singleFile = false()">
from <xsl:value-of select="$corePackage"/>.messageif import MessageBase
from <xsl:value-of select="$corePackage"/>.messages import MessageAux
from <xsl:value-of select="$corePackage"/>.decoder import Decoder
from <xsl:value-of select="$corePackage"/>.encoder import Encoder
from io import StringIO

            <xsl:apply-templates mode="addImports" select="../Imports"/>
            <xsl:apply-templates mode="addImports" select="./Imports"/>
</xsl:if>
class <xsl:value-of select="@name"/>( MessageBase ):

    def __init__(self):
        self.className = "<xsl:value-of select="$package"/>.<xsl:value-of select="@name"/>"
        <xsl:apply-templates mode="declareAttributes" select="."/>
        <xsl:apply-templates mode="declareGettersSetters" select="."/>
        <xsl:apply-templates mode="declareMessageIfMethods" select="."/>
        <xsl:apply-templates mode="applyCode" select="."/>
    </xsl:template>















    <!--     ============================================== -->
    <!--     			Declare Getter / Setters            -->
    <!--     ============================================== -->


    <xsl:template mode="declareGettersSetters" match="Message">
        <xsl:for-each select="Attribute">
            <xsl:variable name="dataType" select="@type"/>
            <xsl:if test="$typeTable/Type[@name=$dataType]">
                <xsl:apply-templates mode="declareNativeGetterSetter" select="."/>
            </xsl:if>
            <xsl:if test="not($typeTable/Type[@name=$dataType])">
                <xsl:apply-templates mode="declareMessageGetterSetter" select="."/>
            </xsl:if>

        </xsl:for-each>
    </xsl:template>




    <xsl:template mode="declareNativeGetterSetter" match="Attribute">

        <xsl:variable name="dataType" select="@type"/>
        <xsl:variable name="type" select="$typeTable/Type[@name=$dataType]/@type"/>

        <xsl:if test="@list">
    def set<xsl:value-of select="functx:capitalize-first (@name)"/>( self, value: list ):
        self.<xsl:value-of select="@name"/> = value

    def get<xsl:value-of select="functx:capitalize-first (@name)"/>( self ) -&gt; list:
        return self.<xsl:value-of select="@name"/>
        </xsl:if>

        <xsl:if test="not(@list)">
    def set<xsl:value-of select="functx:capitalize-first (@name)"/>( self, value: <xsl:value-of select="$type"/> ):
        self.<xsl:value-of select="@name"/> = value

    def get<xsl:value-of select="functx:capitalize-first (@name)"/>( self ) -&gt; <xsl:value-of select="$type"/>:
        return self.<xsl:value-of select="@name"/>
        </xsl:if>

    </xsl:template>


    <xsl:template mode="declareMessageGetterSetter" match="Attribute">
        <xsl:variable name="dataType" select="@type"/>

        <xsl:if test="@list">
    def set<xsl:value-of select="functx:capitalize-first (@name)"/>( self, value: list ):
        self.<xsl:value-of select="@name"/> = value

    def get<xsl:value-of select="functx:capitalize-first (@name)"/>( self ) -&gt; list:
        return self.<xsl:value-of select="@name"/>
        </xsl:if>

        <xsl:if test="not(@list)">
    def set<xsl:value-of select="functx:capitalize-first (@name)"/>( self, value: <xsl:value-of select="$dataType"/> ):
        self.<xsl:value-of select="@name"/> = value

    def get<xsl:value-of select="functx:capitalize-first (@name)"/>( self ) -&gt; <xsl:value-of select="$dataType"/>:
        return self.<xsl:value-of select="@name"/>
        </xsl:if>


    </xsl:template>

    <!--     ============================================== -->
    <!--     			Declare Message Attributes			-->
    <!--     ============================================== -->

    <xsl:template mode="declareAttributes" match="Message">
        <xsl:for-each select="Attribute">
                <xsl:variable name="dataType" select="@type"/>
                <xsl:if test="$typeTable/Type[@name=$dataType]">
                    <xsl:variable name="dType" select="$typeTable/Type[@name=$dataType]/@type"/>
        self.<xsl:value-of select="@name"/>: <xsl:if test="@list">list</xsl:if><xsl:if test="not(@list)"><xsl:value-of select="$dType"/></xsl:if></xsl:if>
                <xsl:if test="not($typeTable/Type[@name=$dataType])">
        self.<xsl:value-of select="@name"/>: <xsl:if test="@list">list</xsl:if><xsl:if test="not(@list)"><xsl:value-of select="@type"/></xsl:if></xsl:if>
        </xsl:for-each>

    </xsl:template>


    <!--     ============================================== -->
    <!--     			Apply code written in XSL very ugly -->
    <!--     ============================================== -->

    <xsl:template mode="applyCode" match="Message">
        <xsl:value-of select="code"/>
    </xsl:template>





    <!--     ============================================== -->
    <!--     			Declare MessageIf methods           -->
    <!--     ============================================== -->

    <xsl:template mode="declareMessageIfMethods" match="Message">
        <xsl:param name="msgPos"/>
        <xsl:apply-templates mode="declareMsgCodecMethods" select="."/>

    def _blanks( self, _indent ) -> str:
        if _indent == 0:
          return ""
        else:
          return "                                             "[:_indent]

    def toString(self, _indent: int = 0 ) -> str:
        _buffer: StringIO = StringIO()
        <xsl:for-each select="Attribute">
            <xsl:variable name="dataType" select="@type"/>
            <xsl:if test="$typeTable/Type[@name=$dataType]">
        _buffer.write(self._blanks( _indent ) + "<xsl:value-of select="@name"/> : " + str( self.<xsl:value-of select="@name"/>) + "\n")</xsl:if>
            <xsl:if test="not($typeTable/Type[@name=$dataType])">
        if self.<xsl:value-of select="@name"/> is None:
           _buffer.write(self._blanks( _indent ) + "<xsl:value-of select="@name"/> : None \n")
        else:
                    <xsl:if test="not(@list)">
           _buffer.write(self._blanks( _indent ) + "<xsl:value-of select="@name"/> : \n" + self.<xsl:value-of select="@name"/>.toString( _indent + 2) + "\n")</xsl:if>
                    <xsl:if test="@list">
           _buffer.write(self._blanks( _indent ) + "<xsl:value-of select="@name"/> : \n")
           _idx = 0
           for _m in self.<xsl:value-of select="@name"/>:
                _idx += 1;
                _buffer.write( self._blanks( _indent + 2 ) + "[" + str(_idx) +"] \n" )
                _buffer.write( _m.toString( _indent + 4) + "\n") </xsl:if></xsl:if>
        </xsl:for-each>
        return _buffer.getvalue()
    </xsl:template>





    <!--     ==================================================== -->
    <!--     			Declare MessageIf encode/decode methods               	  -->
    <!--     ==================================================== -->



    <xsl:template mode="declareMsgCodecMethods" match="Message">

    def toBytes(self) -> bytearray:
       return self.encode()

        <!-- ================= ENCODER ======================== -->
    def encode(self) -> bytearray:
        _encoder = Encoder()
        _encoder.addString( self.className )

        <xsl:for-each select="Attribute">
        # Encode Attribute: <xsl:value-of select="@name"/> Type: <xsl:value-of select="@type"/> List: <xsl:if test="@list">true</xsl:if><xsl:if test="not(@list)">false</xsl:if>

            <xsl:if test="@list">
                <xsl:apply-templates mode="encoderArray" select="."/>
            </xsl:if>
            <xsl:if test="not(@list)">
                <xsl:apply-templates mode="encoderSingle" select="."/>
            </xsl:if>
        </xsl:for-each>
        return _encoder.get_bytes()


        <!-- ================= DECODER ======================== -->
    def decode( self, buffer: bytearray):
        _decoder = Decoder( buffer )
        self.className = _decoder.getString()
        <xsl:for-each select="Attribute">
        #Decode Attribute: <xsl:value-of select="@name"/> Type:<xsl:value-of select="@type"/> List: <xsl:if test="@list">true</xsl:if><xsl:if test="not(@list)">false</xsl:if>
            <xsl:if test="@list">
                <xsl:apply-templates mode="decoderArray" select="."/></xsl:if>
            <xsl:if test="not(@list)">
                <xsl:apply-templates mode="decoderSingle" select="."/></xsl:if>
        </xsl:for-each>
    </xsl:template>


    <!-- ++++++++++++++++++++++++++++++++++++++++++
                               Decode methods
     ++++++++++++++++++++++++++++++++++++++++++++ -->


    <xsl:template mode="decoderSingle" match="Attribute">
        <xsl:variable name="dataType" select="@type"/>

        <xsl:if test="$typeTable/Type[@name=$dataType]">
        self.<xsl:value-of select="@name"/> = _decoder.<xsl:value-of select="$typeTable/Type[@name=$dataType]/@decoder"/>()
        </xsl:if>
        <xsl:if test="not($typeTable/Type[@name=$dataType])">
        self.<xsl:value-of select="@name"/> = _decoder.getMessage()
        </xsl:if>
    </xsl:template>


    <xsl:template mode="decoderArray" match="Attribute">
        <xsl:variable name="dataType" select="@type"/>

        <xsl:if test="$typeTable/Type[@name=$dataType]">
        self.<xsl:value-of select="@name"/> = <xsl:value-of select="$typeTable/Type[@name=$dataType]/@arrayDecoder"/>( _decoder )</xsl:if>
        <xsl:if test="not($typeTable/Type[@name=$dataType])">
        self.<xsl:value-of select="@name"/> = MessageAux.getMessageList( _decoder )</xsl:if>
    </xsl:template>


    <!-- +++++++++++++++++++++++++++++++++++++++++++++
                               Encoder methods
    ++++++++++++++++++++++++++++++++++++++++++++++++ -->


    <xsl:template mode="encoderArray" match="Attribute">
        <xsl:variable name="dataType" select="@type"/>

        <xsl:if test="$typeTable/Type[@name=$dataType]">
            # Encode <xsl:value-of select="$dataType"/> list
        <xsl:value-of select="$typeTable/Type[@name=$dataType]/@arrayEncoder"/>( _encoder, self.<xsl:value-of select="@name"/>  )</xsl:if>
        <xsl:if test="not($typeTable/Type[@name=$dataType])">
        MessageAux.addMessageList( _encoder, self.<xsl:value-of select="@name"/>)</xsl:if>
    </xsl:template>


    <xsl:template mode="encoderSingle" match="Attribute">
        <xsl:variable name="dataType" select="@type"/>

        <xsl:if test="$typeTable/Type[@name=$dataType]">
        _encoder.<xsl:value-of select="$typeTable/Type[@name=$dataType]/@encoder"/>( self.<xsl:value-of select="@name"/> )</xsl:if>
        <xsl:if test="not($typeTable/Type[@name=$dataType]) and not(@constantGroup)">
        _encoder.addMessage( self.<xsl:value-of select="@name"/> )</xsl:if>
    </xsl:template>


</xsl:stylesheet>
