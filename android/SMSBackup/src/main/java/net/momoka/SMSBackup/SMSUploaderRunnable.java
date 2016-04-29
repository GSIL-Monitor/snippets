package net.momoka.SMSBackup;

import android.util.Log;

public class SMSUploaderRunnable implements Runnable {

    private static final String TAG = SMSUploaderRunnable.class.toString();

    static final int UPLOAD_STATE_FAILED = -1;
    static final int UPLOAD_STATE_STARTED = 0;
    static final int UPLOAD_STATE_COMPLETED = 1;


    private SMSTask mTask;

    public SMSUploaderRunnable (SMSTask task) {
        mTask = task;
    }

    public void run () {

        int size = mTask.messages.size();
        Log.d(TAG, Integer.toString(size));
    }
}
