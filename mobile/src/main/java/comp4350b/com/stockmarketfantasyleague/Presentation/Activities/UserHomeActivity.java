package comp4350b.com.stockmarketfantasyleague.Presentation.Activities;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.Investment;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.User;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.AsyncGetRestResponse;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ExecutableAfterAsyncTask;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ServerApiCaller;
import comp4350b.com.stockmarketfantasyleague.R;

/**
 * A placeholder fragment containing a simple view.
 */
public class UserHomeActivity extends Activity implements ExecutableAfterAsyncTask {

    private String thisUserId;
    private List<Investment> investments;
    private User user;
    private boolean gotUser = false;
    private boolean gotInvestments = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        thisUserId = getIntent().getStringExtra(User.INTENT_USER_ID);
        //set the text
        if (thisUserId != null) {
            gotUser = false;
            gotInvestments = false;
            new AsyncGetRestResponse(this,ServerApiCaller.RESPONSE_GET_USER,thisUserId).execute();
        }
        setContentView(R.layout.activity_user_home);
    }

    @Override
    public void recreate() {
        startActivity(getIntent());
        finish();
    }

    @Override
    public void onResume()
    {
        super.onResume();
        thisUserId = getIntent().getStringExtra(User.INTENT_USER_ID);
        //set the text
        if (thisUserId != null) {
            gotUser = false;
            gotInvestments = false;
            new AsyncGetRestResponse(this,ServerApiCaller.RESPONSE_GET_USER,thisUserId).execute();
        }
    }

    public void onClickOpenViewStocks(View view) {
        Intent intent = new Intent(view.getContext(), ViewStockActivity.class);
        view.getContext().startActivity(intent);
    }


    public void onClickOpenBuyStocks(View view) {
        Intent intent = new Intent(view.getContext(), BuyStockActivity.class);
        intent.putExtra(User.INTENT_USER_ID,thisUserId);
        view.getContext().startActivity(intent);
    }


    public void onClickOpenSellStocks(View view) {
        Intent intent = new Intent(view.getContext(), SellStockActivity.class);
        intent.putExtra(User.INTENT_USER_ID,thisUserId);
        startActivity(intent);
    }

    @Override
    public void onCompletedAsyncTask(List<ResponseObject> response, int RESPONSE_TYPE) {
        if (this.hasWindowFocus()) {
            if (RESPONSE_TYPE == ServerApiCaller.RESPONSE_GET_USER) {
                gotUser = true;
                user = (User) response.get(0);
                if (user == null) {
                    Toast.makeText(this,"Could not get user",Toast.LENGTH_SHORT).show();
                    return;
                }
            }
            if (gotUser ) {
                TextView textView = (TextView)findViewById(R.id.tvDisplayUserInformation);
                String result = "Welcome, ";
                result += user.getUserID() + "\nYou currently have a balance of $" + Double.toString(user.getBalance()) +
                        ".";
                textView.setText(result);
            }
        }
    }

    @Override
    public void onFailedAsyncTask(int responseType) {
        if (this.hasWindowFocus()) {
            switch (responseType) {
                case ServerApiCaller.RESPONSE_GET_USER:
                    //anticipating 1 response
                    Toast.makeText(this,"Unable to get user",Toast.LENGTH_SHORT).show();
                    break;
                case ServerApiCaller.RESPONSE_GET_INVESTMENT:
                    //anticipating 1 response
                    Toast.makeText(this,"Unable to get investments",Toast.LENGTH_SHORT).show();
                    break;
            }
        }
    }
}
