import com.hoddmimes.transformer.Transform;

public class PyTransform {

    public static void main( String[] args )
    {

        if (isStartedFromJar()) {
            if ((args.length != 2) || (args[0].compareToIgnoreCase("-xml") != 0)) {
                System.out.println("usage: PyTransform -xml \"<message-definition-source-file>.xml\"");
                System.out.println("     args: " + args.length);
                for (int i = 0; i < args.length; i++) {
                    System.out.println("       arg: " + i + " value: " + args[i]);
                }
                System.exit(0);
            }
        }

        Transform tTransform = new Transform();
        tTransform.parseParameters( args  );
        try {
            tTransform.transform();
        }
        catch( Exception e) {
            // Exception are signaled where they happen
        }
    }

    private static boolean isStartedFromJar()
    {
       String tResource =  PyTransform.class.getResource("PyTransform.class").toString();
       return tResource.startsWith("jar");
    }
}
