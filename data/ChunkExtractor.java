import java.io.*;
import java.net.*;
import java.util.*;
import edu.mit.jwi.*;
import edu.mit.jwi.item.*;


public class ChunkExtractor {

    static final int CHUNK_SIZE = 200;

    public static void main(String[] args) throws Exception {

        // Example command line:
        //
        // java -cp jwi_2.3.0.jar:. ChunkExtractor pseudowords.979-count.txt \
        //     /usr/local/share/WordNet-3.1/dict/cntlist keys/ chunks/
        if (args.length != 4) {
            System.out.println("java ChunkExtractor "
                               + "pseudowords.txt "
                               + "semcor-freqs.txt "
                               + "key-dir/ " 
                               + "output-dir/ "
                               );
            return;
        }

        File pwordFile = new File(args[0]);
        File freqFile = new File(args[1]);
        File instDir = new File(args[2]);
        File outputDir = new File(args[3]);

        Random rand = new Random();

        // Change as necessary
        String path = "/usr/local/share/WordNet-3.0/dict";
        URL url = null;
        try{ url = new URL("file", null, path); } 
        catch(MalformedURLException e){ e.printStackTrace(); }
        if(url == null) return;
        
        // construct the dictionary object and open it
        IDictionary dict = new edu.mit.jwi.Dictionary(url);
        dict.open();

        Map<String,List<String>> pwords = 
            new HashMap<String,List<String>>();

        Map<String,Integer> senseToFreq = 
            new HashMap<String,Integer>();

        Map<String,Map<String,List<String>>> wordToSenseToKeyLines = 
            new HashMap<String,Map<String,List<String>>>();

        Set<String> allSenses = new HashSet<String>();
        
        BufferedReader br = new BufferedReader(new FileReader(pwordFile));
        for (String line = null; (line = br.readLine()) != null; ) {
            String[] arr = line.split(" ");
            String word = arr[0].replaceAll("[<>]","");
            String[] senses = Arrays.copyOfRange(arr, 1, arr.length);
            pwords.put(word, new ArrayList<String>(Arrays.asList(senses)));
            allSenses.addAll(Arrays.asList(senses));
        }
        br.close();

        br = new BufferedReader(new FileReader(freqFile));
        for (String line = null; (line = br.readLine()) != null; ) {
            String[] arr = line.split(" ");
            int freq = Integer.parseInt(arr[0]);
            String key = arr[1];
            senseToFreq.put(key, freq);
        }
        br.close();

        // Due to having keys with too few instances per sense
        Set<String> badPwords = new HashSet<String>();

        for (String pword : pwords.keySet()) {
            Map<String,List<String>> senseToKeyLines
                = new HashMap<String,List<String>>();

            br = new BufferedReader(new FileReader(new File(instDir, pword + ".key")));
            for (String line = null; (line = br.readLine()) != null; ) {
                int i = line.indexOf(' ');
                String inst = line.substring(i + 1);
                String sense = line.split(" ")[2];
                List<String> keyLines = senseToKeyLines.get(sense);
                if (keyLines == null) {
                    keyLines = new ArrayList<String>(1000);
                    senseToKeyLines.put(sense, keyLines);
                }
                keyLines.add(inst);
            }
            for (Map.Entry<String,List<String>> e : senseToKeyLines.entrySet()) {
                if (e.getValue().size() != 1000) {
                    // throw new Error(pword + ": missing lines for " + e.getKey()
                    //                 + ": " + e.getValue().size());
                    badPwords.add(pword);
                }
            }
            wordToSenseToKeyLines.put(pword, senseToKeyLines);           
        }
        br.close();

        System.out.println("removing bad pseudowords: " + badPwords);
        wordToSenseToKeyLines.keySet().removeAll(badPwords);
        pwords.keySet().removeAll(badPwords);



        // Compute the average SemCor frequencie
        int[][] semCorFreqSums = new int[40][40];
        for (int i = 2; i < 40; ++i)
            semCorFreqSums[i] = new int[i];

        System.out.println("Computing avg SemCor freqs");        
        Iterator<IIndexWord> nIter = dict.getIndexWordIterator(POS.NOUN);
        while (nIter.hasNext()) {
            IIndexWord idxWord = nIter.next();
            List<IWordID> wordIDs = idxWord.getWordIDs();
            if (wordIDs.size() < 2)
                continue;
            int[] freqs = semCorFreqSums[wordIDs.size()];

            for (int i = 0; i < wordIDs.size(); ++i) {
                IWordID id = wordIDs.get(i);
                IWord word = dict.getWord(id);
                ISenseKey key = word.getSenseKey();
                Integer freq = senseToFreq.get(key.toString());
                if (freq != null)
                    freqs[i] += freq;
            }
        }
        System.out.println("Finished computing avg SemCor freqs");

        int numSensesTotal = 0;
        int numSemCorInstancesTotal = 0;
        Map<String,Integer> pwordToNumInsts = new HashMap<String,Integer>();
        

        // Write the SemCor and Hybrid distributions
        for (Map.Entry<String,List<String>> e : pwords.entrySet()) {

            String pword = e.getKey();
            List<String> psenses = e.getValue();
            IIndexWord idxWord = dict.getIndexWord(pword, POS.NOUN);
            List<IWordID> wordIDs = idxWord.getWordIDs();
            List<String> senseKeys = new ArrayList<String>();

            Map<String,List<String>> senseToKeyLines
                = wordToSenseToKeyLines.get(pword);

            for (int i = 0; i < wordIDs.size(); ++i) {
                IWordID id = wordIDs.get(i);
                IWord word = dict.getWord(id);
                ISenseKey key = word.getSenseKey();
                senseKeys.add(key.toString());
            }
            
            if (psenses.size() != senseKeys.size()) {
                throw new Error(psenses + "\t+\t" + senseKeys);
            }

            int[] freqs = new int[psenses.size()];

            numSensesTotal += psenses.size();

            double max = 0;
            for (int i = 0; i < senseKeys.size(); ++i) {
                Integer freq = senseToFreq.get(senseKeys.get(i));
                if (freq == null) {
                    // System.out.println("no freq for " + senseKeys.get(i) + "?");
                }
                else {
                    if (freq > max)
                        max = freq;
                    freqs[i] = freq;
                }
            }
            
            // EDGE CASE: the lemma was never seen in WordNet
            if (max == 0) {
                // System.out.printf("Edge case: %s has no SemCor frequencies%n", pword);
                // Assume "uniform" probability across all senses
                freqs = semCorFreqSums[senseKeys.size()];
                for (int f : freqs)
                    if (f > max)
                        max = f;
            }

            // System.out.printf("SemCor freqs for %s: %s%n", pword, 
            //                   Arrays.toString(freqs));
            int numInsts = 0;

            int[] numToUsePerChunk = new int[freqs.length];
            for (int i = 0; i < freqs.length; ++i) {
                int total = (int)((freqs[i] / max) * CHUNK_SIZE);
                numSemCorInstancesTotal += total;
                numToUsePerChunk[i] = total;
                numInsts += total;
            }
            pwordToNumInsts.put(pword, numInsts);

            // System.out.printf("SemCor instances per chunk for %s: %s%n", pword, 
            //                   Arrays.toString(numToUsePerChunk));

            
            for (int chunk = 0; chunk < 5; ++chunk) {
                File f = new File(outputDir, pword + ".chunk" + chunk + ".semcor.key");
                PrintWriter pw = new PrintWriter(f);
                for (int i = 0; i < psenses.size(); ++i) {
                    String sense = psenses.get(i);
                    List<String> instances = senseToKeyLines.get(sense);
                    int numToUse = numToUsePerChunk[i];
                    for (int j = 0; j < numToUse; ++j) {
                        // System.out.printf("%s/%s chunk-%d, total:%d inst:%d%n",
                        //                   pword, sense, chunk,
                        //                   numToUse, j + chunk * CHUNK_SIZE);
                        pw.println(pword + " " + 
                                   instances.get(j + chunk * CHUNK_SIZE));
                    }
                }
                pw.close();
            }

            // Hybrid: First add half the number that would be predicted by the SemCor distq
            int sum = 0;
            numToUsePerChunk = new int[freqs.length];
            for (int i = 0; i < freqs.length; ++i) {
                int total = (int)((freqs[i] / max) * CHUNK_SIZE) / 2;
                numToUsePerChunk[i] = total;
                sum += total;
            }

            // Then add the remaining instances as a uniform distribution
            int uniformBonus = sum / psenses.size();
            for (int i = 0; i < freqs.length; ++i) {
                numToUsePerChunk[i] += uniformBonus;
            }

            // System.out.printf("Hybrid freqs for %s: %s%n", pword, 
            //                   Arrays.toString(numToUsePerChunk));
            
            for (int chunk = 0; chunk < 5; ++chunk) {
                File f = new File(outputDir, pword + ".chunk" + chunk + ".hybrid.key");
                PrintWriter pw = new PrintWriter(f);
                for (int i = 0; i < psenses.size(); ++i) {
                    String sense = psenses.get(i);
                    List<String> instances = senseToKeyLines.get(sense);
                    int numToUse = numToUsePerChunk[i];
                    for (int j = 0; j < numToUse; ++j) {
                        pw.println(pword + " " + 
                                   instances.get(j + chunk * CHUNK_SIZE));
                    }
                }
                pw.close();
            }
        }
    
        // Write the unform and random distribution
        int avgPerSense = numSemCorInstancesTotal / numSensesTotal;
        System.out.printf("Writing uniform and random key, using %d " +
                          "instances per sense%n", avgPerSense);

        for (Map.Entry<String,List<String>> e : pwords.entrySet()) {

            String pword = e.getKey();
            List<String> psenses = e.getValue();
            Map<String,List<String>> senseToKeyLines
                = wordToSenseToKeyLines.get(pword);

            int numToUse = 
                // avgPerSense; // if you want to use the average
                pwordToNumInsts.get(pword) / psenses.size(); // exact same as SemCor

            // Uniform
            for (int chunk = 0; chunk < 5; ++chunk) {
                File f = new File(outputDir, pword + ".chunk" + chunk + ".uniform.key");
                PrintWriter pw = new PrintWriter(f);
                for (int i = 0; i < psenses.size(); ++i) {
                    String sense = psenses.get(i);
                    List<String> instances = senseToKeyLines.get(sense);
                    for (int j = 0; j < numToUse; ++j) {
                        pw.println(pword + " " + 
                                   instances.get(j + chunk * CHUNK_SIZE));
                    }
                }
                pw.close();
            }

            // Random
            int total = numToUse * psenses.size();
            Set<String> used = new HashSet<String>();
            for (int chunk = 0; chunk < 5; ++chunk) {
                int chunkSize = total;
                List<String> randInstances = new ArrayList<String>();
                do {
                    String sense = psenses.get(rand.nextInt(psenses.size()));
                    List<String> instances = senseToKeyLines.get(sense);
                    String inst = instances.get(chunk * CHUNK_SIZE + 
                                                rand.nextInt(CHUNK_SIZE));
                    if (!used.contains(inst)) {
                        randInstances.add(inst);
                        used.add(inst);
                    }
                } while (randInstances.size() < chunkSize);

                Collections.sort(randInstances);

                File f = new File(outputDir, pword + ".chunk" + chunk + ".random.key");
                PrintWriter pw = new PrintWriter(f);
                for (String inst : randInstances) {
                    pw.println(pword + " " + inst);
                }
                pw.close();
            }
        }      
    }
}
