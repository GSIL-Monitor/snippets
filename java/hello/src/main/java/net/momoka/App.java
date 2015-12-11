package net.momoka;

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

        return 0;
    }
}
