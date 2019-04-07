package comp4350b.com.stockmarketfantasyleague.Presentation.Adapters;

import android.content.Context;
import android.support.annotation.LayoutRes;
import android.support.annotation.NonNull;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import comp4350b.com.stockmarketfantasyleague.Business.HTTP.ResponseBody.Investment;
import comp4350b.com.stockmarketfantasyleague.R;

public class InvestmentAdapter extends ArrayAdapter<Investment> {
    public InvestmentAdapter(@NonNull Context context, @NonNull Investment[] objects) {
        super(context, 0, objects);
    }

    @NonNull
    @Override
    public View getView(int position, View convertView, @NonNull ViewGroup parent) {
        Investment invest = getItem(position);

        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.item_investment, parent, false);
        }
        TextView tvName = (TextView) convertView.findViewById(R.id.itemTvInvestmentName);
        assert invest != null;
        tvName.setText(invest.toString());
        return convertView;
    }


}
