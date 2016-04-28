package net.momoka.SMSBackup;

import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.content.Context;

public class SMSManager {

    static final int LOAD_FAILED = -1;
    static final int LOAD_STARTED = 0;
    static final int LOAD_COMPLETED = 1;

    private static Context mContext = null;

    private static final String TAG = SMSManager.class.toString();

    private static final int KEEP_ALIVE_TIME = 1;

    private static final int CORE_POOL_SIZE = 1;

    private static final int MAXIMUM_POOL_SIZE = 1;

    private static final TimeUnit KEEP_ALIVE_TIME_UNIT;

    private static SMSManager sInstance;

    private static Boolean loading = false;

    private final BlockingQueue<Runnable> mLoadQueue;

    private final ThreadPoolExecutor mLoadThreadPool;

    private Handler mHandler;

    static {
        KEEP_ALIVE_TIME_UNIT = TimeUnit.SECONDS;

        sInstance = new SMSManager();
    }

    private SMSManager() {

        mLoadQueue = new LinkedBlockingDeque<Runnable>();

        mLoadThreadPool = new ThreadPoolExecutor(CORE_POOL_SIZE, MAXIMUM_POOL_SIZE,
                KEEP_ALIVE_TIME, KEEP_ALIVE_TIME_UNIT, mLoadQueue);

        mHandler = new Handler(Looper.getMainLooper()) {

            @Override
            public void handleMessage(Message inputMessage) {

                SMSTask task = (SMSTask) inputMessage.obj;
                Log.d(TAG, task.toString());
                Log.d(TAG, Integer.toString(inputMessage.what));
                task.parseMessages();

                switch (inputMessage.what) {
                    case LOAD_COMPLETED:
                        Log.d(TAG, "sms loaded");
                        loading = false;
                    default:
                        super.handleMessage(inputMessage);
                }
            }
        };
    }

    public static SMSManager getIntance() {
        return sInstance;
    }

    public static void setContext(Context context) {
        mContext = context;
    }


    public void handleState(SMSTask task, int state) {
        switch (state) {
            default:
                mHandler.obtainMessage(state, task).sendToTarget();
        }
    }

    public static void startLoad() {
        if (loading) {
            return;
        }

        // TODO: cache loaded messages

        loading = true;
        SMSLoaderRunnable runnable = new SMSLoaderRunnable(new SMSTask());
        runnable.setContext(mContext);
        sInstance.mLoadThreadPool.execute(runnable);
    }

}
