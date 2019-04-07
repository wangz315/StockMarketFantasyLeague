angular.module('StockApp').controller('profileCtrlr', ['$scope', '$cookies', '$http', '$window', function($scope, $cookies, $http, $window) {
	$scope.showUserInfo = false;
	$scope.showErrorTable = false;


    $scope.fetchInvestData = function() {
        $scope.response = null;
        
        $http({
            method: 'GET',
            url: '/api/invest/getAll/' + $cookies.get('loggedInUser')
        }).then(function(response) {
            $scope.status = response.status;
            $scope.investInfo = response.data;

            $scope.showErrorTable = false;
        }, function(response) {
            $scope.status = response.status;
            
            $scope.errorInfo = response.data;
            $scope.showErrorTable = true;
        });
    };
    
    $scope.sellInvestment = function(event, investmentID) {
        $scope.response = null;
        
        event.target.disabled = true;
        
        var numberPicker = event.target.parentElement.parentElement.getElementsByClassName('shareCountInput')[0].firstChild;
        
        $http({
            method: 'POST',
            url: '/api/invest/sell/',
            headers: {
                InvestmentID: investmentID,
                ShareCount: numberPicker.value
            }
        }).then(function(response) {
            $window.location.reload(false);
        }, function(response) {
            $scope.status = response.status;
        
            event.target.disabled = false;
            
            $scope.errorInfo = response.data;
            $scope.showErrorTable = true;
        });
    };


	$scope.fetchUserData = function() {
        $scope.response = null;
        
        $http({
            method: 'GET',
            url: '/api/user/' + $cookies.get('loggedInUser')
        }).then(function(response) {
            $scope.status = response.status;
            
            $scope.userInfo = response.data;
            $cookies.put('balance', $scope.userInfo.Balance);
            
            $scope.showUserInfo = true;
            $scope.showErrorTable = false;
        }, function(response) {
            $scope.status = response.status;
            
            $scope.errorInfo = response.data;
            
            $scope.showUserInfo = false;
            $scope.showErrorTable = true;

            $cookies.get('loggedInUser') = null;
            $window.location.href = '/signin';
        });
    };
    
    $scope.profileBusinessLogic = function() {
        if ($cookies.get('loggedInUser') == null) {
            $window.location.href = '/signin';
        } else {            
            $scope.fetchUserData();
            $scope.fetchInvestData();
        }
    };
    
    $scope.profileBusinessLogic();
}]);