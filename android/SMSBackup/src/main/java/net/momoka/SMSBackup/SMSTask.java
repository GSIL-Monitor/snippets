package net.momoka.SMSBackup;

import android.text.TextUtils;
import android.util.Log;
import android.widget.TextView;

import java.lang.ref.WeakReference;
import java.lang.ref.SoftReference;
import java.security.MessageDigest;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.ArrayList;

public class SMSTask {

    private static final String TAG = SMSTask.class.toString();

    private static SMSManager sManager;

    private WeakReference<TextView> mTextWeakRef;

    public List<SMSMessage> messages;

    public SMSTask() {
        sManager = SMSManager.getIntance();
        messages = new ArrayList<SMSMessage>();
    }

    void handleLoadState(int state) {

        Log.d(TAG, "handleLoadState");

        int outState;
        switch(state) {
            case SMSLoaderRunnable.LOAD_STATE_COMPLETED:
                outState = SMSManager.LOAD_COMPLETED;
                break;
            case SMSLoaderRunnable.LOAD_STATE_FAILED:
                outState = SMSManager.LOAD_FAILED;
                break;
            default:
                outState = SMSManager.LOAD_STARTED;
                break;
        }
        handleState(outState);
    }

    void handleUploadState(int state) {

        Log.d(TAG, "handleUploadState");

        int outState;
        switch(state) {
            case SMSUploaderRunnable.UPLOAD_STATE_COMPLETED:
                outState = SMSManager.UPLOAD_COMPLETED;
                break;
            case SMSUploaderRunnable.UPLOAD_STATE_FAILED:
                outState = SMSManager.UPLOAD_FAILED;
                break;
            default:
                outState = SMSManager.UPLOAD_STARTED;
                break;
        }

        handleState(outState);
    }

    void handleState(int state) {
        sManager.handleState(this, state);
    }

    public void initTask(TextView textView) {
        mTextWeakRef = new WeakReference<TextView>(textView);
    }

    public TextView getTextView() {
        if (null != mTextWeakRef) {
            return mTextWeakRef.get();
        }
        return null;
    }

    public void parseMessages() {
        for (SMSMessage message: messages) {
            _parseMessage(message);
        }
    }

    private void _parseMessage(SMSMessage message) {

        StringBuilder sb = null;
        List<String> keys = new ArrayList<String>();
        List<String> values = new ArrayList<String>();
        String value = null;
        String payload = null;

        for (String key: message.value.keySet()) {
            if ("_id".equals(key)) continue;
            keys.add(key);
        }

        Collections.sort(keys);
        // Log.d(TAG, TextUtils.join("||", keys));
        for (String key: keys) {
            if ("_version".equals(key)) {
                value = Constants.DATA_VERSION;
            }
            else {
                value = message.value.get(key);
            }
            values.add(value);
        }

        payload = TextUtils.join("||", values);
        // Log.d(TAG, payload);

        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            md.update(payload.getBytes("UTF-8"));
            byte[] digest = md.digest();
            sb = new StringBuilder();
            for (byte b : digest) {
                sb.append(String.format("%02x", b & 0xff));
            }
            String hexDigest = sb.toString();
            // Log.d(TAG, hexDigest);
            message.value.put("_hash", hexDigest);
        }
        catch (Exception e) {

        }
    }

}
