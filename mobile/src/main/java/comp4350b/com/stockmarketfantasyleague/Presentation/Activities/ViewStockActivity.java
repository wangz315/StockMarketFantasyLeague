package comp4350b.com.stockmarketfantasyleague.Presentation.Activities;

import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.github.mikephil.charting.charts.LineChart;
import com.github.mikephil.charting.data.Entry;
import com.github.mikephil.charting.data.LineData;
import com.github.mikephil.charting.data.LineDataSet;
import com.github.mikephil.charting.utils.ColorTemplate;
import com.github.mikephil.charting.utils.EntryXComparator;

import java.util.Collections;
import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.GraphFormatter.DateToFloatXAxis;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.AsyncGetRestResponse;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockHistory;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockLookup;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ExecutableAfterAsyncTask;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ServerApiCaller;
import comp4350b.com.stockmarketfantasyleague.R;

public class ViewStockActivity extends Activity implements ExecutableAfterAsyncTask {
    LineChart lineChartDisplayAvailableStocks;
    EditText editTextStockSearch;
    Button buttonSubmitStockSearch;
    String stockSymbolLookup;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_stock);

        lineChartDisplayAvailableStocks = (LineChart) findViewById(R.id.linechartDisplayAvailableStocks);
        editTextStockSearch = (EditText) findViewById(R.id.editTextSearchStockSymbol);
        buttonSubmitStockSearch = (Button) findViewById(R.id.buttonSubmitTextSearchStockSymbol);

        //if button is found, add onClick listener
        assert (buttonSubmitStockSearch != null);
        buttonSubmitStockSearch.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                doSearch();
                closeKeyboard();
            }
        });

    }

    private void closeKeyboard() {
        if (this.hasWindowFocus()) {
            InputMethodManager inputManager = (InputMethodManager)
                    getSystemService(Context.INPUT_METHOD_SERVICE);

            inputManager.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(),
                    InputMethodManager.HIDE_NOT_ALWAYS);
        }
    }


    protected void doSearch() {
        //check that the IDs aren't null
        assert (lineChartDisplayAvailableStocks != null);
        assert (editTextStockSearch != null);
        stockSymbolLookup = editTextStockSearch.getText().toString();
        //do a stock lookup for today's value + the last month's (default)
        new AsyncGetRestResponse(this, ServerApiCaller.RESPONSE_STOCK_LOOKUP, stockSymbolLookup).execute();
        new AsyncGetRestResponse(this, ServerApiCaller.RESPONSE_STOCK_LOOKUP_TO_TODAY, stockSymbolLookup, "2017-03-01").execute();
    }

    private void successfulStockLookup(StockLookup stockLookup) {

        Toast
                .makeText(this, "Today's " + stockLookup.getStockName() +
                        " stock value is: " + stockLookup.getStockPrice(), Toast.LENGTH_SHORT)
                .show();
    }

    private void successfulStockHistoryLookupToToday(List<ResponseObject> response) {
        assert (response != null);
        assert (((List<?>)response).get(0) instanceof StockHistory);
        //modify the correct view
        LineChart lineChart = (LineChart) findViewById(R.id.linechartDisplayAvailableStocks);
        //generate the table
        List<Entry> stockDataToEntries = DateToFloatXAxis.makeEntriesFromResponseObject(response);
        //sort them
        Collections.sort(stockDataToEntries, new EntryXComparator());
        LineDataSet lineDataSet = new LineDataSet(stockDataToEntries, "Default Stock Values");
        lineDataSet.setValueTextSize((float)16);
        lineDataSet.setColors(ColorTemplate.COLORFUL_COLORS);
        LineData lineData = new LineData(lineDataSet);

        //populate the data in the graph
        lineChart.setData(lineData);
        lineChart.setBackgroundColor(Color.WHITE);
        lineChart.setGridBackgroundColor(Color.BLACK);
        lineChart.setBorderColor(Color.BLACK);
        lineChart.invalidate();
    }


    @Override
    public void onCompletedAsyncTask(List<ResponseObject> response, int responseType) {
        if (this.hasWindowFocus()) {
            switch (responseType) {
                case ServerApiCaller.RESPONSE_STOCK_LOOKUP:
                    //anticipating 1 response
                    if (response.size() == 1) {
                        if (response.get(0) instanceof StockLookup) {
                            successfulStockLookup((StockLookup)response.get(0));
                        }
                    }
                    break;
                case ServerApiCaller.RESPONSE_STOCK_LOOKUP_TO_TODAY:
                    successfulStockHistoryLookupToToday(response);
                    break;
            }
        }
    }

    @Override
    public void onFailedAsyncTask(int responseType) {
        if (this.hasWindowFocus()) {
            switch (responseType) {
                case ServerApiCaller.RESPONSE_STOCK_LOOKUP:
                    //anticipating 1 response
                    Toast.makeText(this,"Stock Lookup failed",Toast.LENGTH_SHORT).show();
                    break;
                case ServerApiCaller.RESPONSE_STOCK_LOOKUP_TO_TODAY:
                    Toast.makeText(this,"Stock History Lookup failed",Toast.LENGTH_SHORT).show();
                    break;
            }
        }
    }


}