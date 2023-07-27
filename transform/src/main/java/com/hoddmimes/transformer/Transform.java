package com.hoddmimes.transformer;

import net.sf.saxon.s9api.*;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.InputSource;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;
import java.io.*;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.InvalidParameterException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Transform
{
    static final boolean cDegugTrace = false;
    static final SimpleDateFormat cSDF = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS");

    private final String mXSLFile = "Messages.xsl";

    private String mXslDir = "./xsl/";

    private boolean mComments = true; // Generate comments or not
    private String mSchemaDir = null;
    private String mSchemaOutputPath = ".";
    private String mWorkingDirectory;
    private String mAllInOneFile = "";

    private String mXmlDefinitionSourceFile = null;
    private List<MessageSourceFile> mMessageFiles = new ArrayList<>();
    private List<MessageSourceFile> mMessageFactoryFiles = new ArrayList<>();
    private List<MessageSourceFile> mMongoAuxFiles = new ArrayList<>();

    private String mAllMessages = null;

    public static void main( String[] pArgs ) {
        Transform tGenerator = new Transform();
        tGenerator.parseParameters( pArgs  );


        try {
            for( int i = 0; i < tGenerator.mMessageFiles.size(); i++) {
                tGenerator.transformMessageFile( tGenerator.mMessageFiles.get(i));
            }
        }
        catch( Exception e) {
            e.printStackTrace();
        }
    }


    private String getOutPath( String pPath ) {
        // Check if path is absolut or relative. If it is relative return the absolute path relative to the current
        // working directory otherwise return the absolute path
        Path p = Paths.get(pPath);
        if (p.isAbsolute()) {
            return pPath;
        }
        return mWorkingDirectory + pPath;
    }

    private void collectAllMessages() throws IOException{
       mAllMessages = this.mergeXMLFiles(true);
    }


    private void transformMessageFile( MessageSourceFile pSource) throws Exception
    {
        File tPath = new File( pSource.mXmlSourceFile );
        String tXmlSourcePath = tPath.getCanonicalFile().getParent().replace('\\','/');


        Processor processor = new Processor(false);
        XsltCompiler tCompiler = processor.newXsltCompiler();

        XsltExecutable stylesheet = tCompiler.compile(new XslFiles( mXslDir ).getXslStreamSource(mXSLFile));
        Serializer out = processor.newSerializer( System.out );
        out.setOutputProperty(Serializer.Property.METHOD, "text");
        out.setOutputProperty(Serializer.Property.INDENT, "no");


        Xslt30Transformer transformer = stylesheet.load30();
        Map<QName, XdmValue> tParameters = new HashMap<>();
        tParameters.put(new QName("outPath"), XdmValue.makeValue(getOutPath( pSource.mOutPath )));
        tParameters.put(new QName("package"), XdmValue.makeValue(pSource.mPackage ));
        tParameters.put(new QName("inputXml"), XdmValue.makeValue(pSource.mXmlSourceFile ));
        tParameters.put(new QName("inputXsl"),  XdmValue.makeValue(mXSLFile ));
        tParameters.put(new QName("inputXmlPath"), XdmValue.makeValue(tXmlSourcePath));
        tParameters.put(new QName("comments"), XdmValue.makeValue(mComments));
        tParameters.put(new QName("allInOneFile"), XdmValue.makeValue(pSource.mAllInOneFile));




        transformer.setStylesheetParameters( tParameters );
        transformer.transform(new StreamSource(new File(pSource.mXmlSourceFile)), out);

        /**

        TransformerFactory tFactory = TransformerFactory.newInstance();
        Transformer tTransformer = tFactory.newTransformer( new XslFiles( mXslDir ).getXslStreamSource(mXSLFile));


        tTransformer.transform(new StreamSource(new File(pSource.mXmlSourceFile)), new StreamResult(new NullStream()));
        **/
    }
    private String mergeXMLFiles(boolean pOmitXmlDeclararion) throws IOException{
        StringBuilder tStringBuilder = new StringBuilder();
        if (!pOmitXmlDeclararion) {
            tStringBuilder.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
        }
        tStringBuilder.append("<MessagesRoot>");
        boolean tAnyFileLoaded = false;
        for(int i = 0; i < mMessageFiles.size(); i++ ) {
            MessageSourceFile tSrc = mMessageFiles.get(i);
            tAnyFileLoaded = true;
            String tFileContents = readXMLFile( tSrc.mXmlSourceFile, tSrc.mPackage );
            tStringBuilder.append( tFileContents );
        }
        tStringBuilder.append("</MessagesRoot>");
        if (!tAnyFileLoaded) {
            return null;
        }
        //System.out.println( tStringBuilder.toString() );
        return tStringBuilder.toString();
    }

    private String getModulenameFromFilename( String pFilename ) {
        String tFilename = pFilename.replace("\\", "/");
        int tStart = (tFilename.lastIndexOf("/") < 0) ? 0 : tFilename.lastIndexOf("/") + 1;
        if (tFilename.lastIndexOf(".") > 0) {
            int tEnd = tFilename.lastIndexOf(".");
            return tFilename.substring(tStart, tEnd );
        } else {
            return tFilename.substring(tStart);
        }
    }
    private String readXMLFile( String pFilename, String pPackage ) throws IOException {
        InputStream tInputStream = null;

        tInputStream = new FileInputStream(pFilename);
        String tModule = getModulenameFromFilename( pFilename );
        String tString = new XslFiles( mXslDir ).convertStreamToString(tInputStream, true);
        tString = tString.replaceAll("<\\?[\\p{Print}]+\\?>", "");
        tString = tString.replaceAll("<Messages", "<Messages module=\"" + tModule +"\" package=\"" + pPackage + "\" ");
        return tString;

    }

    public void parseParameters( String[] pArgs )
    {

        // Find out what the current working directory is as absolute path
        String tCurrentPath = FileSystems.getDefault().getPath(".").toAbsolutePath().toString();
        this.mWorkingDirectory = (tCurrentPath.endsWith(".")) ? tCurrentPath.substring(0,tCurrentPath.length() - 1) : tCurrentPath;

        int i = 0;
        while( i < pArgs.length ) {
            if (pArgs[i].compareToIgnoreCase("-xml") == 0) {
                mXmlDefinitionSourceFile = pArgs[ i + 1 ].replace('\\','/');
                i++;
            }
            if (pArgs[i].compareToIgnoreCase("-xslDir") == 0) {
                mXslDir = pArgs[i + 1].replace('\\', '/');
                i++;
            }
            if (pArgs[i].compareToIgnoreCase("-comments") == 0) {
                mComments  = Boolean.parseBoolean( pArgs[ i + 1 ] );
                i++;
            }
            i++;
        }



        if (mXmlDefinitionSourceFile == null) {
            System.out.println("usage: Transform -xml <message-definition-source-file>.xml");
            System.exit(0);
        }

        Element tRoot = loadAndParseXml(mXmlDefinitionSourceFile).getDocumentElement();


        /**
         * Parse ordinary message file
         */
        NodeList tNodeList = tRoot.getElementsByTagName("MessageFile");
        if (tNodeList != null) {
            for( i = 0; i < tNodeList.getLength(); i++) {
                if (tNodeList.item(i).getNodeType() == Node.ELEMENT_NODE) {
                    Element tFileElement = (Element) tNodeList.item(i);
                    String tXmlFile = tFileElement.getAttribute("file");
                    String tOutPath =  tFileElement.getAttribute("outPath");
                    String tPackage = tFileElement.getAttribute("package");
                    String tAllInOneFile = tFileElement.getAttribute("allInOneFile");

                    boolean tDebugFlag = false;
                    if ((tFileElement.getAttribute("debug") != null) && (tFileElement.getAttribute("debug").length() > 0)) {
                        tDebugFlag = Boolean.parseBoolean(tFileElement.getAttribute("debug"));
                    }
                    mMessageFiles.add( new MessageSourceFile( tXmlFile, tOutPath, tPackage, tDebugFlag, tAllInOneFile ));
                }
            }
        }
    }

    public void transform() throws Exception{
        try {
            this.collectAllMessages();
        }
        catch( IOException e) {
            e.printStackTrace();
            throw new IOException("could not find all XML definition, reason: " + e.getMessage());
        }

        try {
            this.checkForMessageDuplicates();
        }
        catch( Exception e) {
            e.printStackTrace();
            throw new Exception("Invalid XML syntax, reason: " + e.getMessage());
        }

        try {
            for (int i = 0; i < this.mMessageFiles.size(); i++) {
                this.transformMessageFile(this.mMessageFiles.get(i));
            }

        } catch (Exception e) {
            e.printStackTrace();
            throw new Exception("XSL transformation failed, reason: " + e.getMessage());
        }
    }

    private  String elementToString(Element node) {
        StringWriter sw = new StringWriter();
        try {
            Transformer tTransformer = TransformerFactory.newInstance().newTransformer();
            tTransformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
            tTransformer.setOutputProperty(OutputKeys.INDENT, "no");
            tTransformer.transform(new DOMSource(node), new StreamResult(sw));
        } catch (TransformerException te) {
            te.printStackTrace();
        }
        return sw.toString();
    }

    private Document loadXMLFromString(String pXmlString) throws Exception
    {
        int idx = pXmlString.indexOf("<MessagesRoot>");
        if (idx > 0) {
            pXmlString = pXmlString.substring(idx);
        }


        DocumentBuilderFactory tFactory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = tFactory.newDocumentBuilder();
        InputSource tInputStream = new InputSource(new StringReader(pXmlString));
        return builder.parse(tInputStream);

    }


    private Document loadAndParseXml( String pXmlFilename ) {
        try {
            File tFile = new File( pXmlFilename );
            if (!tFile.exists()) {
                throw new InvalidParameterException("XML file \"" + tFile.getAbsolutePath() +"\" does not exists");
            }

            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            Document tDocument = db.parse(tFile);
            return tDocument;
        }
        catch( Exception e ) {
            e.printStackTrace();
        }
        return null;
    }

    private void checkForMessageDuplicates() throws IOException {
        try {
            Document tDoc = loadXMLFromString(mAllMessages);
            Element tRoot = tDoc.getDocumentElement();
            NodeList tMessageCollections = tRoot.getElementsByTagName("Messages");
            for (int i = 0; i < tMessageCollections.getLength(); i++) {
                Element tCollecton = (Element)tMessageCollections.item(i);
                Map<String,String> tMap = new HashMap<>();
                NodeList tMessages = tCollecton.getElementsByTagName("Message");
                for (int j = 0; j < tMessages.getLength(); j++) {
                    Element tMsg = (Element) tMessages.item(j);
                    String tMsgName = tMsg.getAttribute("name");
                    if (tMap.containsKey( tMsgName)) {
                       Exception e = new Exception("Duplicate message definition \"" + tMsgName + "\" in message file \"" +
                               tCollecton.getAttribute("module") + "\"");
                       e.printStackTrace();
                    } else {
                        tMap.put( tMsgName, tMsgName);
                    }
                    //System.out.println("Module: " + tCollecton.getAttribute("module") + "  Message: " + tMsg.getAttribute("name"));
                }
            }
        }
        catch( Exception e) {
            e.printStackTrace();
            throw new IOException("Invalid XML syntax, reason: " + e.getMessage());
        }
    }






    private static boolean isStartedFromJar()
    {
        String tResource =  Transform.class.getResource("Transform.class").toString();
        System.out.println("isStartedFromJar resource: " + tResource);
        return tResource.startsWith("jar");
    }


    class NullStream extends OutputStream
    {
        @Override
        public void write(byte[] b) throws IOException
        {
        }

        @Override
        public void write(byte[] b, int off, int len) throws IOException
        {
        }

        @Override
        public void flush() throws IOException
        {
        }

        @Override
        public void write(int b) throws IOException {
        }

        @Override
        public void close() throws IOException
        {
        }
    }

    static class DbMessage {
        String      mMessageName;
        boolean     mDbSupport;
        Element     mMsgElement;
        String      mExtensionMessageName;

        DbMessage( String pMsgName, String pExtentionMsgName, Element pMsgElement, boolean pDbSupport  ) {
            mDbSupport = pDbSupport;
            mMessageName = pMsgName;
            mMsgElement = pMsgElement;
            mExtensionMessageName = pExtentionMsgName;
        }
    }

    class MessageSourceFile
    {
        String 			mXmlSourceFile;
        String 			mOutPath;
        String 			mPackage;
        boolean			mDebug;

        String          mAllInOneFile;

        MessageSourceFile( String pXmlSourceFile, String pOutPath,  String pPackage, boolean pDebug, String pAllInOneFile )
        {
            mXmlSourceFile = pXmlSourceFile;
            mOutPath = pOutPath;
            mDebug = pDebug;
            mPackage = pPackage;
            mAllInOneFile = pAllInOneFile;
        }
    }
}
