import java.io.*;
import java.util.*;

public class PseduowordListGenerator {

    public static void main(String[] args) throws Exception {

        if (args.length != 3) {
            System.out.println("usage: java PseduowordListGenerator " +
                               "input-pseudowords.txt " +
                               "excluded-pseduosenses.txt " +
                               "output-dir/");
            return;
        }

        Map<Integer,List<Pseudoword>> polysemyToPseudowords
            = new HashMap<Integer,List<Pseudoword>>();
        Set<String> excludedPseudosenses = new HashSet<String>();
        // Keeps track of how many senses each word has, which is needed in the
        // case that we exclude certain words in order to keep the correct
        // distribution
        int[] pseudowordsPerPolysemy = new int[1000];
            

        // Read in the excluded list of pseudosenses
        BufferedReader br = new BufferedReader(new FileReader(args[1]));
        for (String line = null; (line = br.readLine()) != null; ) {
            excludedPseudosenses.add(line);
        }
        br.close();
        
        // Read in the pseudowords, remove those with excluded psuedosenses
        br = new BufferedReader(new FileReader(args[0]));
        next_word:
        for (String line = null; (line = br.readLine()) != null; ) {
            String[] arr = line.split("\\s+");
            if (arr[0].replaceAll("[<>]", "").length() == 0)
                continue;
            for (int i = 1; i < arr.length - 1; ++i) {
                if (excludedPseudosenses.contains(arr[i]))
                    continue next_word;
            }

            int n = arr.length - 2;
            pseudowordsPerPolysemy[n]++;
            List<Pseudoword> pwords = polysemyToPseudowords.get(n);
            if (pwords == null) {
                pwords = new ArrayList<Pseudoword>();
                polysemyToPseudowords.put(n, pwords);
            }
            String[] arr2 = line.split("\t");
            double conf = Double.parseDouble(arr2[1]);
            pwords.add(new Pseudoword(conf, arr2[0]));
        }
        br.close();
        
        double total = 0;
        for (int i : pseudowordsPerPolysemy)
            total += i;
        
        for (Map.Entry<Integer,List<Pseudoword>> e : polysemyToPseudowords.entrySet()) {
            // System.out.printf("%s -> %d pseudowords%n", e.getKey(), e.getValue().size());
            List<Pseudoword> l = e.getValue();
            Collections.sort(l);
        }
        File outputDir = new File(args[2]);
        
        // Sample as best we can 
        for (int size = 100; size <= 1000; size += 100) {
            StringBuilder lines = new StringBuilder();
            int num = 0;
            for (int poly = 2; poly < 40; ++poly) {
                List<Pseudoword> pwords = polysemyToPseudowords.get(poly);
                if (pwords == null)
                    continue;
                int words = pseudowordsPerPolysemy[poly];
                int n = (int)(Math.round((words / total) * size));
                num += n;
                //System.out.printf("For %d words, %d have polysemy %d%n", size, n, poly);
                for (int i = 0; i < n; ++i)
                    lines.append(pwords.get(i).text).append('\n');
            }
            PrintWriter pw = new PrintWriter(
                new File(outputDir, "psuedowords." + num + "-count.txt"));
            pw.println(lines);
            pw.close();
        }
    }

    static class Pseudoword implements Comparable<Pseudoword> {
        final double conf;
        final String text;
        public Pseudoword(double conf, String text) {
            this.conf = conf;
            this.text = text;
        }

        public int compareTo(Pseudoword p) {
            return Double.compare(conf, p.conf);
        }
    }
        
}
