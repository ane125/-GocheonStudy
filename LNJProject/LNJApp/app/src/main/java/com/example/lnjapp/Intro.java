package com.example.lnjapp;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import  android.os.Handler;

public class Intro extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // 인트로 메인 화면 불러오기
        setContentView(R.layout.intro);

        Handler handler = new Handler();
        //postDelayed(Runnable, mills)
        handler.postDelayed(new Runnable() {

            @Override
            public void run() {
                Intent intent = new Intent(getApplicationContext(), MainActivity.class);
                startActivity(intent);
                finish();
            }
        }, 5000); //5초 뒤 화면 전환 되도록 설정
    }

    @Override
    protected void onPause() {
        super.onPause();
    }
}
