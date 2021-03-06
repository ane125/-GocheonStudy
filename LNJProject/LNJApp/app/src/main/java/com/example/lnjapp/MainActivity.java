package com.example.lnjapp;

        import androidx.appcompat.app.AppCompatActivity;

        import android.content.Intent;
        import android.os.Bundle;
        import android.os.Handler;
        import android.view.View;
        import android.widget.Button;

public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // 인트로 메인 화면 불러오기
        setContentView(R.layout.activity_main);

        Button b = (Button)findViewById(R.id.button);
        b.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                // 버튼 클릭 시 동작 설정
                Intent intent = new Intent(MainActivity.this, SubActivity.class);
                startActivity(intent);
            }
        });

    } //onCreate
} //end MainActivity
