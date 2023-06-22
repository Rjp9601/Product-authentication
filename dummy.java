package com.baecon.scan;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.app.ProgressDialog;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;

public class dummy extends AppCompatActivity {

    ImageView img;
    TextView tx,tx1,tx2,tx3,tx4;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dummy);

        img=findViewById(R.id.flag);
        tx=findViewById(R.id.text);
        tx1=findViewById(R.id.text1);
        tx2=findViewById(R.id.text2);
        tx3=findViewById(R.id.text3);
        tx4=findViewById(R.id.text4);

        String data=getIntent().getStringExtra("result");
        System.out.println(data);
        String[] arrSplit = data.split("[|]");
        String user = arrSplit[0];
        String w = arrSplit[1];
        String s = arrSplit[2];
        String t = arrSplit[3];
        String u = arrSplit[4];
        String v = arrSplit[5];
        tx.setText(user);
        tx1.setText(s);
        tx2.setText(t);
        tx3.setText(u);
        tx4.setText(v);

        String stUrl = UrlLinks.urlserverpython +"static/ipfs/"+w+".jpg";
        //String url = strings[0];
        Bitmap bitmap = null;
        try {
            InputStream inputStream = new java.net.URL(stUrl).openStream();

            bitmap = BitmapFactory.decodeStream(inputStream);
        } catch (IOException e) {
            e.printStackTrace();
        }

        img.setImageBitmap(bitmap);

    }
}