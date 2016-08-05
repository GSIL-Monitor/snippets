package net.momoka;

import java.text.NumberFormat;
import java.util.Collection;

import org.ahocorasick.trie.Token;
import org.ahocorasick.trie.Trie;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Hello world!
 *
 */
public class App {

    private static final Logger LOGGER = LoggerFactory.getLogger(App.class);

    public static int main(String[] args) throws Exception {

        Trie trie = new Trie().removeOverlaps();

        trie.addKeyword("判断");
        trie.addKeyword("判断经匹配");

        String test = "判断经匹配后的分词路径是否唯一";

        Collection<Token> tokens = trie.tokenize(test);

        for (Token token : tokens) {
            if (!token.isMatch()) {
                LOGGER.info(token.getFragment());
            }
        }

        LOGGER.debug("{}", "11,,,,,".replaceAll(",+", ""));

        Long ts = new Long(System.currentTimeMillis());
        ts /= 1000;

        LOGGER.debug("{}", ts.toString());

        Runtime runtime = Runtime.getRuntime();

        NumberFormat format = NumberFormat.getInstance();

        StringBuilder sb = new StringBuilder();
        long maxMemory = runtime.maxMemory();
        long allocatedMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();

        sb.append("free memory: " + format.format(freeMemory / 1024) + "<br/>");
        sb.append("allocated memory: " + format.format(allocatedMemory / 1024) + "<br/>");
        sb.append("max memory: " + format.format(maxMemory / 1024) + "<br/>");
        sb.append("total free memory: " + format.format((freeMemory + (maxMemory - allocatedMemory)) / 1024) + "<br/>");

        LOGGER.debug(sb.toString());
        return 0;
    }
}
