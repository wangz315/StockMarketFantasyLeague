package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody;

import java.io.Serializable;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class StockHistory implements Serializable, ResponseObject
{

    @SerializedName("Volume")
    @Expose
    private String volume;
    @SerializedName("Symbol")
    @Expose
    private String symbol;
    @SerializedName("Adj_Close")
    @Expose
    private String adjClose;
    @SerializedName("High")
    @Expose
    private String high;
    @SerializedName("Low")
    @Expose
    private String low;
    @SerializedName("Date")
    @Expose
    private String date;
    @SerializedName("Close")
    @Expose
    private String close;
    @SerializedName("Open")
    @Expose
    private String open;
    private final static long serialVersionUID = 3095189330496863351L;

    /**
     * No args constructor for use in serialization
     *
     */
    public StockHistory() {
    }

    public String getVolume() {
        return volume;
    }



    public void setVolume(String volume) {
        this.volume = volume;
    }

    public String getSymbol() {
        return symbol;
    }

    public void setSymbol(String symbol) {
        this.symbol = symbol;
    }

    public String getAdjClose() {
        return adjClose;
    }

    public void setAdjClose(String adjClose) {
        this.adjClose = adjClose;
    }

    public String getHigh() {
        return high;
    }

    public void setHigh(String high) {
        this.high = high;
    }

    public String getLow() {
        return low;
    }

    public void setLow(String low) {
        this.low = low;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getClose() {
        return close;
    }

    public void setClose(String close) {
        this.close = close;
    }

    public String getOpen() {
        return open;
    }

    public void setOpen(String open) {
        this.open = open;
    }


}