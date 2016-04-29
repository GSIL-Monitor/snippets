package net.momoka.SMSBackup;

import java.util.ArrayList;
import java.util.concurrent.*;
import java.util.List;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.widget.TextView;

public class SMSManager {

    static final int LOAD_FAILED = -1;
    static final int LOAD_STARTED = 1;
    static final int LOAD_COMPLETED = 2;
    static final int UPLOAD_FAILED = 3;
    static final int UPLOAD_STARTED = 4;
    static final int UPLOAD_COMPLETED = 5;

    private static Context mContext = null;

    private static final String TAG = SMSManager.class.toString();

    private static final int KEEP_ALIVE_TIME = 1;

    private static final int CORE_POOL_SIZE = 1;

    private static final int MAXIMUM_POOL_SIZE = 1;

    private static final TimeUnit KEEP_ALIVE_TIME_UNIT;

    private static SMSManager sInstance;

    private static List<SMSMessage> messages;

    /* status */
    private static Boolean loading = false;
    private static Boolean uploading = false;

    private final BlockingQueue<Runnable> mLoadQueue;
    private final BlockingQueue<Runnable> mUploadQueue;

    private final ThreadPoolExecutor mLoadThreadPool;
    private final ThreadPoolExecutor mUploadhreadPool;

    private Handler mHandler;

    static {
        KEEP_ALIVE_TIME_UNIT = TimeUnit.SECONDS;

        sInstance = new SMSManager();
    }

    private SMSManager() {

        mLoadQueue = new LinkedBlockingQueue<Runnable>();
        mUploadQueue = new LinkedBlockingQueue<Runnable>();

        mLoadThreadPool = new ThreadPoolExecutor(CORE_POOL_SIZE, MAXIMUM_POOL_SIZE,
                KEEP_ALIVE_TIME, KEEP_ALIVE_TIME_UNIT, mLoadQueue);

        mUploadhreadPool = new ThreadPoolExecutor(CORE_POOL_SIZE, MAXIMUM_POOL_SIZE,
                KEEP_ALIVE_TIME, KEEP_ALIVE_TIME_UNIT, mUploadQueue);

        mHandler = new Handler(Looper.getMainLooper()) {

            @Override
            public void handleMessage(Message inputMessage) {

                SMSTask task = (SMSTask) inputMessage.obj;
                TextView localTextView = null;

                if (null != task) {
                    localTextView = task.getTextView();
                }

                switch (inputMessage.what) {

                    case LOAD_STARTED:
                        if (null != localTextView) {
                            localTextView.setText("loading...");
                        }
                        break;
                    case LOAD_COMPLETED:
                        if (null != localTextView) {
                            localTextView.setText("load complete");
                        }
                        messages = task.messages;
                        sInstance.startUpload(localTextView);
                        break;
                    case UPLOAD_STARTED:
                        if (null != localTextView) {
                            localTextView.setText("load complete");
                        }
                        break;
                    case UPLOAD_COMPLETED:
                        if (null != localTextView) {
                            localTextView.setText("load complete");
                        }
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


    /*
     * this will NOT run on UI thread
     */
    public void handleState(SMSTask task, int state) {

        switch (state) {
            default:
                mHandler.obtainMessage(state, task).sendToTarget();
        }
    }

    public static void startLoad(TextView textView) {
        if (loading) {
            return;
        }

        textView.setText("loading...");

        // TODO: cache loaded messages

        loading = true;
        SMSTask task = new SMSTask();
        task.initTask(textView);
        SMSLoaderRunnable runnable = new SMSLoaderRunnable(task);
        runnable.setContext(mContext);
        sInstance.mLoadThreadPool.execute(runnable);
    }

    public static void startUpload(TextView textView) {
        if (uploading) {
            return;
        }
        textView.setText("uploading");

        uploading = true;

        SMSTask task = new SMSTask();
        task.initTask(textView);
        task.messages = messages;

        SMSUploaderRunnable runnable = new SMSUploaderRunnable(task);

        sInstance.mUploadhreadPool.execute(runnable);
    }

}
