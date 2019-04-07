package comp4350b.com.stockmarketfantasyleague.Presentation.Activities;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.Toast;

import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.User;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.AsyncGetRestResponse;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ExecutableAfterAsyncTask;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ServerApiCaller;
import comp4350b.com.stockmarketfantasyleague.R;

/**
 * A placeholder fragment containing a simple view.
 */
public class LoginActivity extends Activity implements ExecutableAfterAsyncTask {

    private boolean checkingIfValidUser = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
    }

    public void onClickStartUserHome(View view) {
        if (!checkingIfValidUser) {
            new AsyncGetRestResponse(this, ServerApiCaller.RESPONSE_GET_ALL_USERS,"").execute();
            checkingIfValidUser = true;
        }
        closeKeyboard();
    }

    private void closeKeyboard() {
        if (getCurrentFocus() != null) {
            InputMethodManager inputManager = (InputMethodManager)
                    getSystemService(Context.INPUT_METHOD_SERVICE);

            inputManager.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(),
                    InputMethodManager.HIDE_NOT_ALWAYS);
        }
    }

    @Override
    public void onCompletedAsyncTask(List<ResponseObject> response, int RESPONSE_TYPE) {
        //response done, clear the flag
        checkingIfValidUser = false;
        if (this.hasWindowFocus()) {
            //check if this user exists
            EditText textField = (EditText)findViewById(R.id.editLoginUsername);
            String userLoginText = textField.getText().toString();
            if (validUsernameCheck(userLoginText, response)) {
                Toast.makeText(this,"Successfully logged in!",Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(this, UserHomeActivity.class);
                intent.putExtra(User.INTENT_USER_ID,userLoginText);
                startActivity(intent);
            } else {
                //toast message
                Toast.makeText(this,"invalid user ID",Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    public void onFailedAsyncTask(int responseType) {
        //response done, clear flag
        checkingIfValidUser = false;
        if (this.hasWindowFocus()) {
            Toast.makeText(this, "Unable to login, connection failed", Toast.LENGTH_SHORT).show();
        }

    }

    /**
     * Checks each user in responseObject to see if this userId == the userId in one of the valid
     * users
     * @param userLoginText
     * @param response
     * @return
     */
    private boolean validUsernameCheck(String userLoginText, List<ResponseObject> response) {
        for (ResponseObject ro : response) {
            if (ro instanceof User) {
                if (userLoginText.equals(((User) ro).getUserID())) {
                    return true;
                }
                if (userLoginText.equalsIgnoreCase(((User) ro).getUserID())) {
                    Toast.makeText(this, "Invalid user. Did you mean " + ((User) ro).getUserID(),
                            Toast.LENGTH_SHORT).show();
                    return false;
                }
            }
        }
        return false;
    }
}
