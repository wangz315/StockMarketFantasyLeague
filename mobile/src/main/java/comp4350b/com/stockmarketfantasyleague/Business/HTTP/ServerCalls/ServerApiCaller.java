package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls;

import java.util.ArrayList;
import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.Investment;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockHistory;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockLookup;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.User;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ServerApiCaller {

    public static final int RESPONSE_STOCK_LOOKUP = 0;
    public static final int RESPONSE_STOCK_LOOKUP_TO_TODAY = 1;
    public static final int RESPONSE_STOCK_LOOKUP_TO_DATE = 2;
    public static final int RESPONSE_GET_USER = 3;
    public static final int RESPONSE_GET_ALL_USERS = 4;
    public static final int RESPONSE_SELL_STOCK_INVESTMENT = 5;
    public static final int RESPONSE_BUY_STOCK_INVESTMENT = 6;
    public static final int RESPONSE_GET_ALL_USER_INVESTMENTS = 7;
    public static final int RESPONSE_GET_INVESTMENT = 8;
    public static final int RESPONSE_ADD_USER = 9;

    private static final String SERVER_URL = "http://52.42.66.215:5000/";
    private static final int SUCCESSS_CODE = 200;

    private static ServerApiInterface buildRetrofitObject() {
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(SERVER_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        return retrofit.create(ServerApiInterface.class);
    }

    public static List<ResponseObject> convertResponseToList(ResponseObject responseObject) {
        List<ResponseObject> result = new ArrayList<>();
        result.add(responseObject);
        return result;
    }

    private static List<ResponseObject> convertResponseToList(List<?> body) {
        List<ResponseObject> result = new ArrayList<>();
        Object item;
        for (int i = 0; i < body.size(); i++) {
            item = body.get(i);
            if (item instanceof ResponseObject) {
                result.add((ResponseObject) item);
            }
        }
        return result;
    }

    /**
     * Following executes code on the current thread
     * make sure to run on thread
     *
     * @param stockSymbol
     * @return
     */
    public static List<ResponseObject> getCurrentStockData(String stockSymbol) {
        Response<StockLookup> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<StockLookup> resultData = serverApiInterface.getCurrentStockData(stockSymbol);
        try {
            response = resultData.execute();

            if (response != null) {
                return convertResponseToList(response.body());
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static List<ResponseObject> addUser(String userId, String firstName, String lastName) {
        Response<Void> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<Void> resultData =
                serverApiInterface.addUser(
                        userId,
                        firstName,
                        lastName
                );
        try {
            response = resultData.execute();
            if (response.code() == 200) {
                ResponseObject emptyobject = new User();
                List<ResponseObject> result = new ArrayList<>();
                result.add(emptyobject);
                return result;
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static List<ResponseObject> getUser(String userId) {
        Response<User> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<User> resultData = serverApiInterface.getUser(userId);
        try {
            response = resultData.execute();

            if (response != null) {
                return convertResponseToList(response.body());
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static List<ResponseObject> getAllUsers() {
        Response<List<User>> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<List<User>> resultData = serverApiInterface.getAllUsers();
        try {
            response = resultData.execute();

            if (response != null) {
                return convertResponseToList(response.body());
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }


    public static List<ResponseObject> getStockHistoryToToday(String stockSymbol, String dateStart) {
        Response<List<StockHistory>> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<List<StockHistory>> resultData =
                serverApiInterface.getStockHistoryToToday(
                        stockSymbol,
                        dateStart
                );
        try {
            response = resultData.execute();

            if (response != null) {
                return convertResponseToList(response.body());
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static List<ResponseObject> getStockHistory(String stockSymbol, String dateStart, String dateEnd) {
        Response<List<StockHistory>> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<List<StockHistory>> resultData =
                serverApiInterface.getStockHistory(
                        stockSymbol,
                        dateStart,
                        dateEnd
                );
        try {
            response = resultData.execute();

            if (response != null) {
                return convertResponseToList(response.body());
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }


    public static List<ResponseObject> sellStockInvestment(String investmentId, int shareCount) {
        Response<Void> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<Void> resultData =
                serverApiInterface.sellStockInvestment(
                        investmentId,
                        shareCount
                );
        try {
            response = resultData.execute();
            if (response.code() == SUCCESSS_CODE) {
                ResponseObject emptyobject = new User();
                List<ResponseObject> result = new ArrayList<>();
                result.add(emptyobject);
                return result;
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static List<ResponseObject> buyStockInvestment(String userId, String stockSymbol, int shareCount) {
        Response<Investment> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<Investment> resultData =
                serverApiInterface.buyStockInvestment(
                        userId,
                        stockSymbol,
                        shareCount
                );
        try {
            response = resultData.execute();

            if (response != null) {
                return convertResponseToList(response.body());
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static List<ResponseObject> getAllUserInvestments(String userId) {
        Response<List<Investment>> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<List<Investment>> resultData =
                serverApiInterface.getAllUserInvestments(
                        userId
                );
        try {
            response = resultData.execute();

            if (response != null) {
                return convertResponseToList(response.body());
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public static List<ResponseObject> getInvestmentDetails(String investmentId) {
        Response<Investment> response = null;
        ServerApiInterface serverApiInterface = buildRetrofitObject();
        final Call<Investment> resultData =
                serverApiInterface.getInvestmentDetails(
                        investmentId
                );
        try {
            response = resultData.execute();

            if (response != null) {
                return convertResponseToList(response.body());
            } else {
                return null;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

}
