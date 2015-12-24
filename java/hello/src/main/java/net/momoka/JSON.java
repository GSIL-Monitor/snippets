package net.momoka;

import java.util.regex.Pattern;

import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class JSON {

    private static final Logger logger = LoggerFactory.getLogger(JSON.class);

    private static final Pattern SPACE = Pattern.compile(" ");

    private static final String orig =
        "{\"date\": \"2015-12-24 00:00:00\", \"data\": {\"user_id\": 1234567890}, \"flag\": \"middleware\"}";

    public static void main(String[] args) {

        Object _ = JSONValue.parse(orig);
        JSONObject obj = (JSONObject) _;

        if (!obj.containsKey("flag")) {
            logger.warn("no flag from input");
            return;
        }

        String action = obj.get("flag").toString();
        String date =
            SPACE.split(obj.get("date").toString())[0].replace("-", "");

        _ = obj.get("data");
        JSONObject data = (JSONObject) _;
        Long userId = Long.parseLong(data.get("user_id").toString());

        logger.info(action);
        logger.info(date);
        logger.info(userId.toString());

    }
}
