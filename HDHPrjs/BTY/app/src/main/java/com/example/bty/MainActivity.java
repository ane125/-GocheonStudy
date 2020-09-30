package com.example.bty;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ListView chattList = (ListView) findViewById(R.id.ChattList);

        final String[] mid = {"한동희1","한동희2", "한동희3", "한동희4"};

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, mid);

        chattList.setAdapter(adapter);

        chattList.setOnItemClickListener(new AdapterView.OnItemClickListener()
        {
           public void onItemClick(AdapterView<?> arg0, View arg1, int arg2, long arg3){
               Toast.makeText(getApplicationContext(), mid[arg2],
                       Toast.LENGTH_SHORT).show();
           }
        });
    }
}