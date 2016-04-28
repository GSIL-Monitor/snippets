package net.momoka.SMSBackup;

import android.text.TextUtils;
import android.util.Log;

import java.security.MessageDigest;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;

public class SMSTask {

    private static final String TAG = SMSTask.class.toString();

    private static SMSManager sManager;

    public List<Map<String, String>> messages;

    public SMSTask() {
        sManager = SMSManager.getIntance();
        messages = new ArrayList<Map<String, String>>();
    }

    void handleLoadState(int state) {
        // TODO:

        handleState(state);
    }

    void handleState(int state) {
        sManager.handleState(this, state);
    }

    public void parseMessages() {
        for (Map<String, String> message: messages) {
            _parseMessage(message);
        }
    }

    private void _parseMessage(Map<String, String> message) {

        StringBuilder sb = null;
        List<String> keys = new ArrayList<String>();
        List<String> values = new ArrayList<String>();
        String value = null;
        String payload = null;

        for (String key: message.keySet()) {
            if ("_id".equals(key)) continue;
            keys.add(key);
        }

        Collections.sort(keys);
        Log.d(TAG, TextUtils.join("||", keys));
        for (String key: keys) {
            if ("_version".equals(key)) {
                value = Constants.DATA_VERSION;
            }
            else {
                value = message.get(key);
            }
            values.add(value);
        }

        payload = TextUtils.join("||", values);
        Log.d(TAG, payload);

        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(payload.getBytes("UTF-8"));
            byte[] digest = md.digest();
            sb = new StringBuilder();
            for (byte b : digest) {
                sb.append(String.format("%02x", b & 0xff));
            }
            String hexDigest = sb.toString();
            Log.d(TAG, hexDigest);
        }
        catch (Exception e) {

        }
    }

}
