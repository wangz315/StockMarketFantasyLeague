package comp4350b.com.stockmarketfantasyleague.Presentation.Activities;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.Investment;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.User;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.AsyncGetRestResponse;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ExecutableAfterAsyncTask;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ServerApiCaller;
import comp4350b.com.stockmarketfantasyleague.Presentation.Adapters.InvestmentAdapter;
import comp4350b.com.stockmarketfantasyleague.R;

public class SellStockActivity extends AppCompatActivity implements ExecutableAfterAsyncTask {

    String userId;

    boolean sellingStock;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        userId = getIntent().getStringExtra(User.INTENT_USER_ID);
        if (userId == null) {
            //no userId found
        }
        //load the display
        setContentView(R.layout.activity_sell_stock);
        //tell the user we're loading investments
        Toast.makeText(this, "Loading investments...", Toast.LENGTH_LONG).show();
        //load them
        new AsyncGetRestResponse(this, ServerApiCaller.RESPONSE_GET_ALL_USER_INVESTMENTS, userId).execute();
    }

    @Override
    public void onCompletedAsyncTask(List<ResponseObject> response, int RESPONSE_TYPE) {
        if (this.hasWindowFocus()) {
            switch (RESPONSE_TYPE) {
                case (ServerApiCaller.RESPONSE_GET_ALL_USER_INVESTMENTS):
                    Toast.makeText(this, "Finished loading investments", Toast.LENGTH_SHORT).show();
                    //populate the list
                    ListView listView = (ListView) findViewById(R.id.listDisplayAvailableStocks);
                    assert (listView != null);
                    //convert the response to a list of stock histories
                    Investment[] investments = convertResponseListToInvestments(response);
                    if (investments.length > 0) {
                        //add an adapter to the list
                        InvestmentAdapter investmentAdapter =
                                new InvestmentAdapter(this, (Investment[]) investments);
                        listView.setAdapter(investmentAdapter);

                        listView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
                            @Override
                            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                                sellThisStock(adapterView, view, i, l);
                            }
                        });
                    }
                    break;
                case (ServerApiCaller.RESPONSE_SELL_STOCK_INVESTMENT):
                    if (sellingStock) {
                        sellingStock = false;
                        Toast.makeText(this, "Successfully sold stock!", Toast.LENGTH_SHORT).show();
                        //reload stocks
                        new AsyncGetRestResponse(this, ServerApiCaller.RESPONSE_GET_ALL_USER_INVESTMENTS, userId).execute();
                    } else {
                        Toast.makeText(this, "Trying to sell previous stock...", Toast.LENGTH_SHORT).show();
                    }
                    break;
            }
        }
    }

    @Override
    public void onFailedAsyncTask(int responseType) {
        if (this.hasWindowFocus()) {
            switch (responseType) {
                case ServerApiCaller.RESPONSE_SELL_STOCK_INVESTMENT:
                    sellingStock = false;
                    //anticipating 1 response
                    Toast.makeText(this,"Unable to sell stock...",Toast.LENGTH_SHORT).show();
                    break;
            }
        }
    }

    private void sellThisStock(AdapterView<?> adapterView, View view, int i, long l) {
        sellingStock = true;
            Investment investment;
            if (adapterView.getItemAtPosition(i) instanceof Investment) {
                investment = (Investment) adapterView.getItemAtPosition(i);
                new AsyncGetRestResponse(this,
                        ServerApiCaller.RESPONSE_SELL_STOCK_INVESTMENT,
                        investment.getInvestmentID(),
                        Integer.toString(investment.getShareCount())).execute();
            }
    }


    private Investment[] convertResponseListToInvestments(List<ResponseObject> response) {
        Investment[] result = new Investment[response.size()];
        for (int i = 0; i < response.size(); i++) {
            if (response.get(i) instanceof Investment) {
                result[i] = (Investment) response.get(i);
            }
        }
        return result;
    }
}
