package net.momoka.SMSBackup;

import android.Manifest;
import android.app.Activity;
import android.content.ContentValues;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.os.Looper;
import android.os.Message;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.os.Handler;

public class MainActivity extends Activity implements ActivityCompat.OnRequestPermissionsResultCallback {

    private static final String TAG = MainActivity.class.toString();
    private static final int REQUEST_SMS_PERMISSIONS = 1;
    private static final String[] PERMISSIONS_SMS = {Manifest.permission.READ_SMS, Manifest.permission.WRITE_SMS};

    private Handler mHandler;

    private static SMSManager sSMSManager;

    private void handleHandler() {
        mHandler = new Handler(Looper.getMainLooper()) {
          @Override
          public void handleMessage(Message inputMessage) {
              int state = inputMessage.what;
              switch (state) {
                  default:
                      Log.d(TAG, Integer.toString(state));
              }
          }
        };
    }

    /**
     * Called when the activity is first created.
     */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        sSMSManager = SMSManager.getIntance();
        sSMSManager.setContext(this);
        setContentView(R.layout.main);

        Button backupBtn = (Button) findViewById(R.id.btnBackup);
        backupBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                backupSMS();
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        if (requestCode == REQUEST_SMS_PERMISSIONS) {
            Log.i(TAG, "received response for sms permission request");

            int read = grantResults[0];
            int write = grantResults[1];

            if (read == PackageManager.PERMISSION_GRANTED && write == PackageManager.PERMISSION_GRANTED) {
                doReadSMS();
            }
        }
    }

    private void requestPermission() {
        ActivityCompat.requestPermissions(MainActivity.this, PERMISSIONS_SMS, REQUEST_SMS_PERMISSIONS);
    }

    private boolean checkPermission() {
        int read = ContextCompat.checkSelfPermission(this, Manifest.permission.READ_SMS);
        int write = ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_SMS);

        Log.d(TAG, Integer.toString(read));
        Log.d(TAG, Integer.toString(write));

        boolean rv = (read == PackageManager.PERMISSION_GRANTED) && (write == PackageManager.PERMISSION_GRANTED);
        Log.d(TAG, Boolean.toString(rv));
        return rv;
    }

    public void backupSMS() {
        Log.d(TAG, "backup");

        if (!checkPermission()) {
            requestPermission();
        } else {
            doReadSMS();
        }
    }

    public void doReadSMS() {
        sSMSManager.startLoad((TextView)findViewById(R.id.txtStatus));
        // doWriteSMS();
    }

    public void doWriteSMS() {
        Log.d(TAG, "doWriteSMS");

        ContentValues values = new ContentValues();
        values.put("address", "123456789");
        values.put("body", "foo bar");
        Uri createdRow = getContentResolver().insert(Uri.parse("content://sms/sent"), values);
        Log.d(TAG, createdRow.toString());

        Log.d(TAG, "a new SMS wrote!");
    }
}
