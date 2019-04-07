package comp4350b.com.stockmarketfantasyleague.Presentation.Activities;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;

import comp4350b.com.stockmarketfantasyleague.R;

public class MainActivity extends AppCompatActivity{

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.tbMainToolbar);
        toolbar.setTitle(R.string.app_name);
        setSupportActionBar(toolbar);

    }



    public void onClickStartLogin(View view) {
        Intent intent = new Intent(this, LoginActivity.class);
        view.getContext().startActivity(intent);
    }

    public void onClickStartRegister(View view) {
        Intent intent = new Intent(this, RegisterActivity.class);
        view.getContext().startActivity(intent);
    }

}
