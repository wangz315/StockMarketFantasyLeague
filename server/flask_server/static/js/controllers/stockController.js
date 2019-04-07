angular.module('StockApp').controller('stockCtrlr', ['$scope', '$cookies', '$http', '$window', function($scope, $cookies, $http, $window) {
    $scope.showStockRealtime = false;
    $scope.showStockHistory = false;
    $scope.showErrorTable = false;

    $scope.showLoggedInError = false;
    $scope.showIntAmtError = false;
    $scope.showBalanceError = false;
    $scope.showLoggedIn = false;
    $scope.disableInvest = false;


    var dateOneMonthAgo = new Date();
    dateOneMonthAgo.setMonth(dateOneMonthAgo.getMonth() - 1);
    dateOneMonthAgo = dateOneMonthAgo.toISOString().split('T')[0];


    $scope.invest = function() {
        $scope.userBalance = $cookies.get('balance');

        if ($cookies.get('loggedInUser') == null) {
            $scope.showLoggedInError = true;
        } else {
            $scope.showLoggedInError = false;

            if($scope.isInt($scope.amountInvest)) {
                $scope.showIntAmtError = false;

                $scope.UserID = $cookies.get('loggedInUser');
                $scope.stock_symbol = $scope.tempSymbol;
                $scope.ShareCount = $scope.amountInvest;

                if(parseFloat($scope.amountInvest) * parseFloat($scope.stockRealtimeInfo.stock_price) <= parseFloat($cookies.get('balance'))) {
                    $scope.totalCost = parseFloat($scope.amountInvest) * parseFloat($scope.stockRealtimeInfo.stock_price);
                    $scope.showBalanceError = false;
                } else {
                    $scope.showBalanceError = true;
                }
                
            
            } else {
                $scope.showIntAmtError = true;
            }
        }
    }
    
    $scope.fetchInvest = function() {
        $scope.response = null;
        $scope.disableInvest = true;

        $http({
            method: 'POST',
            url: '/api/invest/buy/',
            headers: {
                UserID: $cookies.get('loggedInUser'),
                StockSymbol:  $scope.tempSymbol,
                ShareCount: $scope.amountInvest
            }
        }).then(function(response) {
            $scope.status = response.status;
            $window.location.href = '/profile';

        }, function(response) {
            $scope.status = response.status;
            $scope.errorInfo = response.data;
            $scope.showStockRealtime = false;
            $scope.showStockHistory = false;
            $scope.showErrorTable = true;
        });
    };

    $scope.isInt = function(value) {
        return !isNaN(value) && (function(x) { return (x | 0) === x; })(parseFloat(value))
    }
    
    $scope.fetchStockData = function() {
        var stockSymbol = $scope.stockSymbol.toLowerCase();
        $scope.tempSymbol = stockSymbol;
        

        $scope.fetchRealtimeData(stockSymbol);
        $scope.fetchHistoricalData(stockSymbol);
    }

    $scope.fetchRealtimeData = function(stockSymbol) {
        $scope.response = null;
        $http({
            method: 'GET',
            url: '/api/stock/' + stockSymbol
        }).then(function(response) {
            $scope.status = response.status;

            $scope.stockRealtimeInfo = response.data;
            $scope.stockName = response.data.stock_name;

            $scope.showStockRealtime = true;
            $scope.showErrorTable = false;

            if($cookies.get('loggedInUser') != null) {
                $scope.showLoggedIn = true;
            }

        }, function(response) {
            $scope.status = response.status;

            $scope.errorInfo = response.data;

            $scope.showStockRealtime = false;
            $scope.showStockHistory = false;
            $scope.showErrorTable = true;
        });
    };

    $scope.fetchHistoricalData = function(stockSymbol) {
        $scope.response = null;
        $http({
            method: 'GET',
            url: '/api/stock/' + stockSymbol + '/history',
            headers: {
                dateStart: dateOneMonthAgo
            }
        }).then(function(response) {
            $scope.status = response.status;
            $scope.stockHistoryInfo = response.data;
            var stockHistoryHigh = [];
            var stockHistoryLow = [];
            var stockHistoryClose = [];
            $scope.stockChartXData = [];
            for(var i=0; i< $scope.stockHistoryInfo.length; i++){
                stockHistoryHigh.push(parseFloat($scope.stockHistoryInfo[i].High));
                stockHistoryLow.push(parseFloat($scope.stockHistoryInfo[i].Low));
                stockHistoryClose.push(parseFloat($scope.stockHistoryInfo[i].Close));
                $scope.stockChartXData.push($scope.stockHistoryInfo[i].Date.slice(5));
            }
            $scope.stockChartYData = [{
              "name": "High",
              "color": '#f7a35c',
              "data": stockHistoryHigh
            },{
                "name": "Low",
                "color": '#7cb5ec',
                "data": stockHistoryLow
            },{
                "name": "Close",
                "color": '#90ed7d',
                "data": stockHistoryClose
            }];
            $scope.showStockHistory = true;
        }, function(response) {
            $scope.status = response.status;
            $scope.showStockHistory = false;
        });
    };
}]);
