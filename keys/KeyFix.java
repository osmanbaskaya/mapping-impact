import java.io.*;
import java.util.*;

public class KeyFix {

    public static void main(String[] args) throws Exception {
        if (args.length != 4) {
            System.out.println("usage: java KeyFix " + 
                               "in-1.key in-2.key fixed-1.key fixed2.key");
            return;
        }

        File inKey1 = new File(args[0]);
        File inKey2 = new File(args[1]);
        File outKey1 = new File(args[2]);
        File outKey2 = new File(args[3]);


        Map<String,Map<String,String>> k1_docToInstToRest = 
            read(inKey1);

        Map<String,Map<String,String>> k2_docToInstToRest = read(inKey2);
        
        Set<String> docs = new LinkedHashSet<String>(k2_docToInstToRest.keySet());
        docs.addAll(k1_docToInstToRest.keySet());

        PrintWriter pw1 = new PrintWriter(outKey1);
        PrintWriter pw2 = new PrintWriter(outKey2);

        for (String doc : docs) {
            // Load the instance labels for this document (i.e., pseudoword)
            Map<String,String> k1_instToRest = k1_docToInstToRest.get(doc);
            Map<String,String> k2_instToRest = k2_docToInstToRest.get(doc);
            
            Set<String> insts = new LinkedHashSet<String>();
            if (k1_instToRest != null)
                insts.addAll(k1_instToRest.keySet());
            if (k2_instToRest != null)
                insts.addAll(k2_instToRest.keySet());
            
            Map<String,String> instToRemapped =
                new HashMap<String,String>();
            for (String inst : insts) {
                String rem = String.format("%05d", instToRemapped.size());
                instToRemapped.put(inst, rem);
            }

            if (k1_instToRest != null) {
                for (Map.Entry<String,String> e : k1_instToRest.entrySet()) {
                    pw1.println(doc + " " + instToRemapped.get(e.getKey())
                                + " " + e.getValue());
                }
            }
            if (k2_instToRest != null) {
                for (Map.Entry<String,String> e : k2_instToRest.entrySet()) {
                    pw2.println(doc + " " + instToRemapped.get(e.getKey())
                                + " " + e.getValue());
                }
            }
        }
        pw1.close();
        pw2.close();
    }
     
    static Map<String,Map<String,String>> read(File f) throws Exception {

        Map<String,Map<String,String>> docToInstToRest = 
            new LinkedHashMap<String,Map<String,String>>(979*1000);


        BufferedReader br = new BufferedReader(new FileReader(f));
        for (String line = null; (line = br.readLine()) != null; ) {
            int i = line.indexOf(' ');
            int j = line.indexOf(' ', i + 1);
            String doc = line.substring(0, i);
            String inst = line.substring(i+1, j);
            String rest = line.substring(j+1);

            Map<String,String> instToRest = docToInstToRest.get(doc);
            if (instToRest == null)  {
                instToRest = new HashMap<String,String>();
                docToInstToRest.put(doc, instToRest);
            }
            instToRest.put(inst, rest);
        }
        return docToInstToRest;
    }

}
