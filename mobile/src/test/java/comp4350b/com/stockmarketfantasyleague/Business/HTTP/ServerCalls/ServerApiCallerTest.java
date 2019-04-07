package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.Investment;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockHistory;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockLookup;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.User;


import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.util.ArrayList;
import java.util.List;

import static org.mockito.Mockito.*;
import static org.junit.Assert.*;

public class ServerApiCallerTest {

    List<ResponseObject> StockData= ServerApiCaller.getCurrentStockData("$$");
    List<ResponseObject> user=ServerApiCaller.getUser("usr");
    //List<ResponseObject> stock= ServerApiCaller.getStockHistoryToToday("$$","date");

    @InjectMocks
    ServerApiCaller serverApiCaller;
    ResponseObject ro;



    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void convertResponseToList() throws Exception {
        List<ResponseObject> result=ServerApiCaller.convertResponseToList(ro);
        assertTrue("Response not being created", !result.isEmpty());
    }

    @Test
    public void getCurrentStockData() throws Exception {
       List<ResponseObject> result= ServerApiCaller.getCurrentStockData("GOOG");
        assertTrue("not fetching stock data",!result.isEmpty());
    }
    @Test
    public void notExsistentStockData() throws Exception{
        List<ResponseObject> result= ServerApiCaller.getCurrentStockData("nonexistent");
        assertFalse("this stock does not exist",result.isEmpty());
    }

    @Test
    public void getUser() throws Exception {
        List<ResponseObject> result= ServerApiCaller.getUser("232323");
        assertTrue("not same users",!result.isEmpty());
    }

    @Test
    public void getnonExsistantUser() throws Exception{
        List<ResponseObject> result= ServerApiCaller.getUser("rish.rah");
        assertFalse("some thing this user should not exist", result.isEmpty());

    }
    @Test
    public void getAllUsers() throws Exception {
        List<ResponseObject> result=ServerApiCaller.getAllUsers();
        assertTrue("empty userlist",!result.isEmpty());
    }

    @Test
    public void getStockHistoryToToday() throws Exception {
        List<ResponseObject> result= ServerApiCaller.getStockHistoryToToday("GOOG","2017-01-21");
        assertTrue("Stock does not exists", result!=null);
    }



    @Test
    public void getStockHistory() throws Exception {
            List<ResponseObject> result= ServerApiCaller.getStockHistory("GOOG","2017-01-20","2017-01-21");
            assertTrue("Unable to find history",result!=null);
    }

    @Test
    public void sellStockInvestment() throws Exception {

        List<ResponseObject> result= ServerApiCaller.sellStockInvestment("do_not_delete_test_investment",3);
        assertTrue("Server has null on success", result!=null);//
    }

    @Test
    public void buyStockInvestment() throws Exception {
            List<ResponseObject> result= ServerApiCaller.buyStockInvestment("232323","GOOG",1);
            assertTrue("not able ",result!=null);

    }

    @Test
    public void getAllUserInvestments() throws Exception {
        List<ResponseObject> result= ServerApiCaller.getAllUserInvestments("232323");
        assertTrue("not able to fetch users", result!=null);

    }


    @Test
    public void getInvestmentDetails() throws Exception {
        List<ResponseObject> result= ServerApiCaller.getInvestmentDetails("do_not_delete_test_investment");
        assertTrue("shows null on succes", result==null);

    }

}
