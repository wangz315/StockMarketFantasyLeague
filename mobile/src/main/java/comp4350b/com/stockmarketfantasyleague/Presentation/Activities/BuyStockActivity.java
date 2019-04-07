package comp4350b.com.stockmarketfantasyleague.Presentation.Activities;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.User;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.AsyncGetRestResponse;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ExecutableAfterAsyncTask;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ServerApiCaller;
import comp4350b.com.stockmarketfantasyleague.R;

public class BuyStockActivity extends Activity implements ExecutableAfterAsyncTask {

    private boolean queryingResult = false;
    private String userId;
    private boolean gotStock = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_buy_stock);
        this.userId = getIntent().getStringExtra(User.INTENT_USER_ID);
        if (userId == null) userId = "";
    }

    public void onClickBuyStocks(View view) {
        if (queryingResult) {
            makeToastMessage("Please wait for previous result...");
            return;
        }
        if (userId.equals("")) {
            makeToastMessage("Connection lost. Please login again");
            return;
        }
        EditText stockSymbol = (EditText)findViewById(R.id.etBuyStockSymbol);
        EditText stockAmount = (EditText)findViewById(R.id.etBuyStockAmount);

        if (stockSymbol.getText().toString().length() == 0) {
            makeToastMessage("Please enter a first name");
            return;
        }
        if (stockAmount.getText().toString().length() == 0) {
            makeToastMessage("Please enter a stock amount");
            return;
        }

        if (Integer.parseInt(stockAmount.getText().toString()) < 0) {
            makeToastMessage("Please enter a positive share count");
            return;
        }

        //if code reaches here, the texts are valid
        queryingResult = true;
        gotStock = false;
        new AsyncGetRestResponse(this,ServerApiCaller.RESPONSE_STOCK_LOOKUP,
                stockSymbol.getText().toString()
        ).execute();
    }

    private void makeToastMessage(String message) {
        Toast.makeText(this,message,Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onCompletedAsyncTask(List<ResponseObject> response, int RESPONSE_TYPE) {
        queryingResult = false;
        if (gotStock) makeToastMessage("Stock bought!");
        switch (RESPONSE_TYPE) {
            case ServerApiCaller.RESPONSE_STOCK_LOOKUP:
                gotStock = true;
                EditText stockSymbol = (EditText)findViewById(R.id.etBuyStockSymbol);
                EditText stockAmount = (EditText)findViewById(R.id.etBuyStockAmount);

                if (stockSymbol.getText().toString().length() == 0) {
                    makeToastMessage("Please enter a first name");
                    return;
                }
                if (stockAmount.getText().toString().length() == 0) {
                    makeToastMessage("Please enter a stock amount");
                    return;
                }

                if (Integer.parseInt(stockAmount.getText().toString()) < 0) {
                    makeToastMessage("Please enter a positive share count");
                    return;
                }

                queryingResult = true;
                new AsyncGetRestResponse(this, ServerApiCaller.RESPONSE_BUY_STOCK_INVESTMENT,
                        userId,
                        stockSymbol.getText().toString(),
                        stockAmount.getText().toString()).execute();
                break;
        }
    }


    @Override
    public void onFailedAsyncTask(int responseType) {
        queryingResult = false;
        switch (responseType) {
            case ServerApiCaller.RESPONSE_BUY_STOCK_INVESTMENT:
                makeToastMessage("Unable to buy stock. Not enough funds or stock doesn't exist");
                break;
            case ServerApiCaller.RESPONSE_STOCK_LOOKUP:
                makeToastMessage("Invalid Stock symbol");
                break;
        }
    }
}
