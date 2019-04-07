package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody;

import java.io.Serializable;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class StockLookup implements Serializable, ResponseObject
{

    @SerializedName("stock_name")
    @Expose
    private String stockName;
    @SerializedName("stock_price")
    @Expose
    private String stockPrice;
    @SerializedName("stock_open")
    @Expose
    private String stockOpen;
    private final static long serialVersionUID = 3402942865088081195L;

    /**
     * No args constructor for use in serialization
     *
     */
    public StockLookup() {
    }

    /**
     *
     * @param stockName
     * @param stockPrice
     * @param stockOpen
     */
    public StockLookup(String stockName, String stockPrice, String stockOpen) {
        super();
        this.stockName = stockName;
        this.stockPrice = stockPrice;
        this.stockOpen = stockOpen;
    }

    public String getStockName() {
        return stockName;
    }

    public void setStockName(String stockName) {
        this.stockName = stockName;
    }

    public String getStockPrice() {
        return stockPrice;
    }

    public void setStockPrice(String stockPrice) {
        this.stockPrice = stockPrice;
    }

    public String getStockOpen() {
        return stockOpen;
    }

    public void setStockOpen(String stockOpen) {
        this.stockOpen = stockOpen;
    }

}