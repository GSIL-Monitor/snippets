package net.momoka;

import java.lang.reflect.Type;
import java.util.Map;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JSON {

    private static Logger logger = LoggerFactory.getLogger(JSON.class);

    public static void main(String[] args) {
        Gson gson = new Gson();

        Type type = new TypeToken<Map<String, String>>() {
        }.getType();

        Map<String, String> in = gson.fromJson("{\"hello\": \"world\"}", type);

        logger.info(in.toString());
        logger.info(in.get("hello"));
    }
}
