package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody;

import java.io.Serializable;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class Investment implements Serializable, ResponseObject
{

    @SerializedName("CurrentValue")
    @Expose
    private Double currentValue;
    @SerializedName("InitialValue")
    @Expose
    private Double initialValue;
    @SerializedName("InvestmentID")
    @Expose
    private String investmentID;
    @SerializedName("UserID")
    @Expose
    private String userID;
    @SerializedName("DateCreated")
    @Expose
    private String dateCreated;
    @SerializedName("ShareCount")
    @Expose
    private Integer shareCount;
    @SerializedName("StockSymbol")
    @Expose
    private String stockSymbol;
    private String forTestPurpose;
    private final static long serialVersionUID = 5052139122851446321L;

    public Investment(String forTestPurpose)
    {
        this.forTestPurpose="Testing";
        this.currentValue=0.0;
        this.initialValue=0.0;
        this.dateCreated="date";
        this.investmentID="investID";
        this.shareCount=0;
        this.stockSymbol="$$";
        this.userID="usrID";
    }

    public Double getCurrentValue() {
        return currentValue;
    }

    public void setCurrentValue(Double currentValue) {
        this.currentValue = currentValue;
    }

    public Investment withCurrentValue(Double currentValue) {
        this.currentValue = currentValue;
        return this;
    }

    public Double getInitialValue() {
        return initialValue;
    }

    public void setInitialValue(Double initialValue) {
        this.initialValue = initialValue;
    }

    public Investment withInitialValue(Double initialValue) {
        this.initialValue = initialValue;
        return this;
    }

    public String getInvestmentID() {
        return investmentID;
    }

    public void setInvestmentID(String investmentID) {
        this.investmentID = investmentID;
    }

    public Investment withInvestmentID(String investmentID) {
        this.investmentID = investmentID;
        return this;
    }

    public String getUserID() {
        return userID;
    }

    public void setUserID(String userID) {
        this.userID = userID;
    }

    public Investment withUserID(String userID) {
        this.userID = userID;
        return this;
    }

    public String getDateCreated() {
        return dateCreated;
    }

    public void setDateCreated(String dateCreated) {
        this.dateCreated = dateCreated;
    }

    public Investment withDateCreated(String dateCreated) {
        this.dateCreated = dateCreated;
        return this;
    }

    public Integer getShareCount() {
        return shareCount;
    }

    public void setShareCount(Integer shareCount) {
        this.shareCount = shareCount;
    }

    public Investment withShareCount(Integer shareCount) {
        this.shareCount = shareCount;
        return this;
    }

    public String getStockSymbol() {
        return stockSymbol;
    }

    public void setStockSymbol(String stockSymbol) {
        this.stockSymbol = stockSymbol;
    }

    public Investment withStockSymbol(String stockSymbol) {
        this.stockSymbol = stockSymbol;
        return this;
    }

    public String toString() {
        String result = "";
        result += "Investment in stock: " + stockSymbol;
        if (dateCreated != null) result += " was done at: " + dateCreated;
        result += "\nYou currently own " + Integer.toString(shareCount) + " shares of this stock";
        result += "\nWith a current value of " + Double.toString(currentValue) +
                " per stock, the total value comes to: " + Double.toString(currentValue * shareCount);
        return result;

    }

}