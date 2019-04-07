package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls;

import android.os.AsyncTask;

import java.util.ArrayList;
import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;

public class AsyncGetRestResponse extends AsyncTask<Void, Void, Boolean> {

    private int responseType;
    private List<String> listValues;
    private ExecutableAfterAsyncTask activity;
    private List<ResponseObject> response;

    public AsyncGetRestResponse(ExecutableAfterAsyncTask activity, int responseType, String... values) {
        //store all the values into arraylist
        this.responseType = responseType;
        this.activity = activity;
        if (values.length > 0) {
            listValues = new ArrayList<>();
            for (String value : values) {
                listValues.add(value);
            }
        }
    }

    @Override
    protected Boolean doInBackground(Void... params) {
        //see what kind of message this is
        response = null;
        switch (responseType) {
            //response is an object and can be a list or single element
            case ServerApiCaller.RESPONSE_STOCK_LOOKUP:
                response = ServerApiCaller.getCurrentStockData(listValues.get(0));
                break;
            case ServerApiCaller.RESPONSE_STOCK_LOOKUP_TO_TODAY:
                response = ServerApiCaller.getStockHistoryToToday(listValues.get(0), listValues.get(1));
                break;
            case ServerApiCaller.RESPONSE_STOCK_LOOKUP_TO_DATE:
                response = ServerApiCaller.getStockHistory(listValues.get(0), listValues.get(1), listValues.get(1));
                break;
            case ServerApiCaller.RESPONSE_GET_USER:
                response = ServerApiCaller.getUser(listValues.get(0));
                break;
            case ServerApiCaller.RESPONSE_GET_ALL_USERS:
                response = ServerApiCaller.getAllUsers();
                break;
            case ServerApiCaller.RESPONSE_BUY_STOCK_INVESTMENT:
                response = ServerApiCaller.buyStockInvestment(
                        listValues.get(0),
                        listValues.get(1),
                        Integer.parseInt(listValues.get(2))
                );
                break;
            case ServerApiCaller.RESPONSE_SELL_STOCK_INVESTMENT:
                response = ServerApiCaller.sellStockInvestment(
                        listValues.get(0),
                        Integer.parseInt(listValues.get(1))
                );
                break;
            case ServerApiCaller.RESPONSE_GET_ALL_USER_INVESTMENTS:
                response = ServerApiCaller.getAllUserInvestments(
                        listValues.get(0)
                );
                break;
            case ServerApiCaller.RESPONSE_GET_INVESTMENT:
                response = ServerApiCaller.getInvestmentDetails(
                        listValues.get(0)
                );
                break;
            case ServerApiCaller.RESPONSE_ADD_USER:
                response = ServerApiCaller.addUser(
                        listValues.get(0),
                        listValues.get(1),
                        listValues.get(2)
                );
                break;
        }
        if (response == null) return false;
        if (response.size() == 0) return true;
        if (response.get(0) != null) return true;
        return false;
    }

    /**
     * Calls the appropriate task after completing, corresponding to the response type
     * Only calls it if the previous method did not fail
     *
     * @param executionResult
     */
    protected void onPostExecute(Boolean executionResult) {
        //check for successful async task
        if (executionResult) {
            //always return a list of results for consistency
            activity.onCompletedAsyncTask(response,this.responseType);
        } else {
            activity.onFailedAsyncTask(this.responseType);
        }

    }







}
