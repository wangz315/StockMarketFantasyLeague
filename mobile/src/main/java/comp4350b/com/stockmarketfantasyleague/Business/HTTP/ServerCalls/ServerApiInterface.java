package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls;


import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.Investment;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockHistory;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockLookup;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.User;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Field;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.Headers;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface ServerApiInterface {

    @GET("api/stock/{stock_symbol}")
    Call<StockLookup> getCurrentStockData(@Path("stock_symbol") String stockSymbol);


    @POST("api/user/")
    Call<Void> addUser(@Header("UserID") String userId,
                       @Header("FirstName") String firstName,
                       @Header("LastName") String lastName);

    @GET("api/user/{user_id}")
    Call<User> getUser(@Path("user_id") String userId);

    @GET("api/user")
    Call<List<User>> getAllUsers();

    @GET("api/stock/{stock_symbol}/history")
    Call<List<StockHistory>> getStockHistoryToToday(@Path("stock_symbol") String stockSymbol,
                                             @Header("dateStart") String dateStart);

    @GET("api/stock/{stock_symbol}/history")
    Call<List<StockHistory>> getStockHistory(@Path("stock_symbol") String stockSymbol,
                                                    @Header("dateStart") String dateStart,
                                                    @Header("dateEnd") String dateEnd);

    @POST("api/invest/sell/")
    Call<Void> sellStockInvestment(@Header("InvestmentID") String investmentId,
                                         @Header("ShareCount") int shareCount);

    @POST("api/invest/buy/")
    Call<Investment> buyStockInvestment(@Header("UserID") String userId,
                                        @Header("StockSymbol") String stockSymbol,
                                         @Header("ShareCount") int shareCount);

    @GET("api/invest/getAll/{user_id}")
    Call<List<Investment>> getAllUserInvestments(@Path("user_id") String userId);

    @GET("api/invest/{investment_id}")
    Call<Investment> getInvestmentDetails(@Path("investment_id") String investmentId);



}
