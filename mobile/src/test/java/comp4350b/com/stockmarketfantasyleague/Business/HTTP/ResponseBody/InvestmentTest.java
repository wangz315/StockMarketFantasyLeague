package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.MockitoAnnotations;

import static org.mockito.Mockito.*;

public class InvestmentTest {
    @InjectMocks
    Investment investment;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testWithCurrentValue() throws Exception {
        Investment result = investment.withCurrentValue(0.0);
        Assert.assertEquals("current value not same",new Investment("").getCurrentValue(),result.getCurrentValue(),0.0);
    }

    @Test
    public void testWithInitialValue() throws Exception {
        Investment result = investment.withInitialValue(0d);
        Assert.assertEquals("initial values not same",new Investment("").getInitialValue(), result.getInitialValue(),0.0);
    }

    @Test
    public void testWithInvestmentID() throws Exception {
        Investment result = investment.withInvestmentID("investID");
        Assert.assertTrue("InvestmentID not same",new Investment("").getInvestmentID().equals(result.getInvestmentID()) );
    }

    @Test
    public void testWithUserID() throws Exception {
        Investment result = investment.withUserID("usrID");
        Assert.assertTrue("userID not same ",new Investment("").getUserID().equals(result.getUserID()) );
    }

    @Test
    public void testWithDateCreated() throws Exception {
        Investment result = investment.withDateCreated("date");
        Assert.assertTrue("dates are not matching",new Investment("").getDateCreated().equals(result.getDateCreated()) );
    }

    @Test
    public void testWithShareCount() throws Exception {
        Investment result = investment.withShareCount(0);
        Assert.assertTrue("Share count not matching",new Investment("").getShareCount()== result.getShareCount());
    }

    @Test
    public void testWithStockSymbol() throws Exception {
        Investment result = investment.withStockSymbol("$$");
        Assert.assertTrue("Stock symbols don't match",new Investment("").getStockSymbol().equals(result.getStockSymbol()));
    }


}