package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls;

import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;

public interface ExecutableAfterAsyncTask {

    void onCompletedAsyncTask(List<ResponseObject> response, int RESPONSE_TYPE);
    void onFailedAsyncTask(int responseType);
}
