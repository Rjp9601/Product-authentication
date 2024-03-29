package com.baecon.scan;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    TextView btn;
    private static final int REQUEST_CODE = 101;

    @RequiresApi(api = Build.VERSION_CODES.M)


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        btn = findViewById(R.id.scan);


        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                IntentIntegrator intentIntegrator = new IntentIntegrator(MainActivity.this);

                intentIntegrator.setPrompt("For Flash use volume button");
                intentIntegrator.setBeepEnabled(true);
                intentIntegrator.setOrientationLocked(true);
                intentIntegrator.setCaptureActivity(Capture.class);
                intentIntegrator.initiateScan();
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        final IntentResult intentResult = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        if (intentResult.getContents() != null) {
            AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
            builder.setTitle("Result");
            builder.setMessage("Message");

            builder.setPositiveButton("Ok", new DialogInterface.OnClickListener() {

                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();

                    StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
                    StrictMode.setThreadPolicy(policy);
                    String url = UrlLinks.pyregister;

                    ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(1);


                    nameValuePairs.add(new BasicNameValuePair("src", intentResult.getContents()));

                    String result = null;
                    try {
                        result = jSOnClassforData.forCallingStringAndreturnSTring(url, nameValuePairs);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    if (result.equals("fail")) {
                        Toast.makeText(MainActivity.this, "No data match found, the product is fake.", Toast.LENGTH_SHORT).show();


                    } else {
                        Intent io = new Intent(MainActivity.this, dummy.class);
                        io.putExtra("result", result);
                        startActivity(io);

                    }


                }
            });

            builder.show();
        }
    }
}