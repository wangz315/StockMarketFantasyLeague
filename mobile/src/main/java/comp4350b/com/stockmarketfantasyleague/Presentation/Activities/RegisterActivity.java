package comp4350b.com.stockmarketfantasyleague.Presentation.Activities;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.util.List;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.ResponseObject;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.AsyncGetRestResponse;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ExecutableAfterAsyncTask;
import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ServerCalls.ServerApiCaller;
import comp4350b.com.stockmarketfantasyleague.R;

public class RegisterActivity extends Activity implements ExecutableAfterAsyncTask {

    private boolean queryingResult = false;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
    }

    public void onClickRegister(View view) {
        if (queryingResult) {
            makeToastMessage("Please wait for previous result...");
            return;
        }
        EditText userId = (EditText)findViewById(R.id.editRegisterUsername);
        EditText firstName = (EditText)findViewById(R.id.editRegisterFirstName);
        EditText lastName = (EditText)findViewById(R.id.editRegisterLastName);
        if (userId.getText().toString().length() < 6 ||
                userId.getText().toString().length() > 15  ) {
            makeToastMessage("UserId must be between 6 and 15 characters");
            return;
        }
        if (firstName.getText().toString().length() == 0) {
            makeToastMessage("Please enter a first name");
            return;
        }
        if (lastName.getText().toString().length() == 0) {
            makeToastMessage("Please enter a last name");
            return;
        }

        //if code reaches here, the texts are valid
        queryingResult = true;
        new AsyncGetRestResponse(this, ServerApiCaller.RESPONSE_ADD_USER,
                userId.getText().toString(),
                firstName.getText().toString(),
                lastName.getText().toString()).execute();
    }

    private void makeToastMessage(String message) {
        Toast.makeText(this,message,Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onCompletedAsyncTask(List<ResponseObject> response, int RESPONSE_TYPE) {
        //response finished
        queryingResult = false;
        makeToastMessage("Successfully Registered! You can now login");
        Intent intent = new Intent(this,LoginActivity.class);
        startActivity(intent);
    }

    @Override
    public void onFailedAsyncTask(int responseType) {
        queryingResult = false;
        if (this.hasWindowFocus()) {
            switch (responseType) {
                case ServerApiCaller.RESPONSE_ADD_USER:
                    //anticipating 1 response
                    Toast.makeText(this,"You are already registered",Toast.LENGTH_SHORT).show();
                    break;
            }
        }
    }

}
