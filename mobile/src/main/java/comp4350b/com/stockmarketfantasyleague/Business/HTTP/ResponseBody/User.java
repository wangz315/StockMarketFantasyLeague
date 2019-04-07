package comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody;

import java.io.Serializable;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class User implements Serializable, ResponseObject
{

    @SerializedName("LastName")
    @Expose
    private String lastName;
    @SerializedName("Balance")
    @Expose
    private Double balance;
    @SerializedName("UserID")
    @Expose
    private String userID;
    @SerializedName("FirstName")
    @Expose
    private String firstName;
    private final static long serialVersionUID = -1058281288546096522L;

    public final static String INTENT_USER_ID = "USER_ID";

    /**
     * No args constructor for use in serialization
     *
     */
    public User() {
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Double getBalance() {
        return balance;
    }

    public void setBalance(Double balance) {
        this.balance = balance;
    }

    public String getUserID() {
        return userID;
    }

    public void setUserID(String userID) {
        this.userID = userID;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

}