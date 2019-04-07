package comp4350b.com.stockmarketfantasyleague.Business.GraphFormatter;

import com.github.mikephil.charting.data.Entry;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.InjectMocks;
import org.mockito.MockitoAnnotations;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockHistory;

import static org.mockito.Mockito.*;

public class DateToFloatXAxisTest {
    List<String> correctDateSet;
    List<String> badDateSet;
    List<ResponseObject> mockResponseObject;
    List<StockHistory> mockStockHistoryObject;

    @Before
    public void setUp() {
        correctDateSet = new ArrayList<>();
        badDateSet = new ArrayList<>();

        String[] goodDates = {
                "2017-01-01",
                "2015-2-03",
                "2012-01-1",
                "2017-05-21",
                "2016-03-11",
                "2012-02-01",
                "2013-01-10",
                "2014-02-01",
                "2017-02-01",
                "2017-11-01",
                "2017-12-23"
        };
        String[] badDates = {
                "201-01-01",
                "2015-2-035",
                "20122-01-01",
                "2017-405-21",
                "-03-11",
                "201202-01",
                "2013-041-10",
                "2014-0140-01",
                "2017-02-99",
                "20127-11-31",
                "2017-12-223"
        };
        Collections.addAll(correctDateSet,goodDates);
        Collections.addAll(badDateSet,badDates);
    }

    @Test
    public void testConvertDateSetToFloatSet() throws Exception {
        List<Float> correctFloatSet;
        List<Float> badFloatSet;
        //test every precision and see if all have a 0 value
        for(DateToFloatXAxis.PrecisionEnum e : DateToFloatXAxis.PrecisionEnum.values()) {
            correctFloatSet = DateToFloatXAxis.convertDateSetToFloatSet(
                    correctDateSet,
                    e.precision);
            badFloatSet = DateToFloatXAxis.convertDateSetToFloatSet(
                    badDateSet,
                    e.precision);

            //check all values and see if there is for sure a 0 value
            boolean zeroValueExists = false;
            for (Float f : correctFloatSet) {
                if (f.intValue() == 0) {
                    zeroValueExists = true;
                    break;
                }
            }
            //check that a 0 value exists
            Assert.assertTrue(zeroValueExists);
            //assert that the sizes are equal to the original set
            Assert.assertTrue(correctDateSet.size() == correctFloatSet.size());
            //assert that the bad data set has:
            //  1. less than correct data set
            //  2. equal to 0 data
            Assert.assertTrue(badDateSet.size() < correctDateSet.size());
            Assert.assertTrue(badDateSet.size() == 0);
        }
    }

    @Test
    public void testMakeEntriesFromResponseObject() throws Exception {
        List<Entry> result = DateToFloatXAxis.makeEntriesFromResponseObject(mockResponseObject);
    }

    @Test
    public void testMakeEntries() throws Exception {
        List<Entry> result = DateToFloatXAxis.makeEntries(mockStockHistoryObject);
    }
}