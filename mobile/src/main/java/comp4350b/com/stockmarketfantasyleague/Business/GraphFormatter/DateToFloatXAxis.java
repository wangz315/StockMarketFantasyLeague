package comp4350b.com.stockmarketfantasyleague.Business.GraphFormatter;

import android.util.Log;

import com.github.mikephil.charting.data.Entry;

import junit.framework.Test;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.StockHistory;

public class DateToFloatXAxis {

    enum PrecisionEnum{
        PRECISION_SECONDS(1000),
        PRECISION_MINUTES(1000 * 60),
        PRECISION_HOURS(1000 * 60 * 60),
        PRECISION_DAYS(1000 * 60 * 60 * 24),;

        int precision;

        PrecisionEnum(int i) {
            precision = i;
        }

        int precision() {
            return precision;
        }
    }

    /**
     * Convert a set of dates into a set of float values.
     * Then standardizes the values so there is one that can be set to 0 (by keeping track of
     * the minimum value.
     * @param dateList The list of date values in milliseconds since 01/01/1970 (default)
     * @param PRECISION Constant value that converts milliseconds since 1970 to
     * @return
     */
    public static List<Float> convertDateSetToFloatSet(List<String> dateList, int PRECISION) {
        List<Float> result = new ArrayList<>();
        //convert the dates to floats
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        long dateToIntegerTime;
        //keep track of the minimum to update
        long minReferenceTime = Long.MAX_VALUE;
        for (String s: dateList) {
            try {
                dateToIntegerTime = dateFormat.parse(s).getTime() / (PRECISION);
                if (dateToIntegerTime < minReferenceTime) minReferenceTime = dateToIntegerTime;
                result.add((float) dateToIntegerTime);
            } catch (ParseException e) {
                Log.d("Could not parse " + s + " into long", e.getMessage());
            }
        }

        float thisValue;
        for (int i = 0; i < result.size(); i++) {
            thisValue = result.get(i);
            result.set(i,(thisValue - minReferenceTime));
        }
        return result;
    }


    /**
     * Helper method to facilitate the conversion between the generic collection type
     * Reason to add this redundancy is to cut back on code, else different response objects are needed
     * This method is only called for stock history values, so we only have 1 check
     * @param response The raw response from the GET API call
     * @return The result of makeEntries() after it has gotten the right List
     */
    public static List<Entry> makeEntriesFromResponseObject(List<ResponseObject> response) {
        List<StockHistory> result = new ArrayList<>();
        for (ResponseObject responseObject : response) {
            if (responseObject instanceof StockHistory) {
                result.add((StockHistory)responseObject);
            }
        }
        return makeEntries(result);
    }

    /**
     * Convert a list of StockHistory values into Entries for use in the MPAndroidChart library
     * @param stockHistory The list containing stock histories (which must have a getDate() value)
     * @return A list of Entries ready to be graphed
     */
    public static List<Entry> makeEntries(List<StockHistory> stockHistory) {
        List<Entry> result = new ArrayList<Entry>();
        List<String> xValueStringDates = new ArrayList<>();
        List<Float> xValueFloatDates;

        for (StockHistory s : stockHistory) {
            xValueStringDates.add(s.getDate());
        }

        xValueFloatDates = DateToFloatXAxis.
                convertDateSetToFloatSet(
                        xValueStringDates,
                        PrecisionEnum.PRECISION_HOURS.precision()
                );
        xValueStringDates.clear();
        //add the corresponding Y values
        for (int i = 0; i < stockHistory.size(); i++) {
            result.add(new Entry(xValueFloatDates.get(i),
                    Float.valueOf(stockHistory.get(i).getAdjClose())));
        }
        return result;
    }
}
