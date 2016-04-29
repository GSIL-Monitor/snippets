package net.momoka.SMSBackup;

import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.os.Process;
import android.util.Log;

import java.util.HashMap;
import java.util.Map;

public class SMSLoaderRunnable implements Runnable {

    private static final String TAG = SMSLoaderRunnable.class.toString();

    static Context mContext = null;
    static final int LOAD_STATE_FAILED = -1;
    static final int LOAD_STATE_STARTED = 0;
    static final int LOAD_STATE_COMPLETED = 1;

    final SMSTask mTask;

    @Override
    public void run() {

        android.os.Process.setThreadPriority(Process.THREAD_PRIORITY_BACKGROUND);

        mTask.handleLoadState(LOAD_STATE_STARTED);

        StringBuilder sb;
        String sortOrder;
        int limit = 10;
        int offset = 0;
        int cnt = 0;
        int i = 0;

        // TODO: error handling: LOAD_STATE_FAILED

        SMSMessage message = null;

        for ( ;; ) {

            Thread.interrupted();

            sb = new StringBuilder();

            sb.append("date DESC ");
            sb.append("LIMIT " + Integer.toString(limit));
            sb.append(" OFFSET " + Integer.toString(offset));

            sortOrder = sb.toString();


            Cursor cursor = mContext.getContentResolver().query(
                    Uri.parse("content://sms/inbox"), null, null, null, sortOrder);
            if (cursor.moveToFirst()) {
                do {
                    cnt++;
                    // Log.d(TAG, "== begin " + Integer.toString(cnt) + "th message ==");

                    message = new SMSMessage();
                    for(i = 0; i < cursor.getColumnCount(); i++) {
                        message.value.put(cursor.getColumnName(i), cursor.getString(i));
                    }

                    // Log.d(TAG, message.toString());
                    mTask.messages.add(message);

                } while (cursor.moveToNext());
                offset += limit;
            } else {
                Log.w(TAG, "no sms in inbox!");
                cursor.close();
                break;
            }
            cursor.close();
        }

        Log.d(TAG, String.format("loaded %d messages", cnt));
        Log.d(TAG, "sms all read!");

        mTask.handleLoadState(LOAD_STATE_COMPLETED);
        Thread.interrupted();
    }

    public static void setContext(Context context) {
        mContext = context;
    }

    public SMSLoaderRunnable(SMSTask task) {
        mTask = task;
    }
}
