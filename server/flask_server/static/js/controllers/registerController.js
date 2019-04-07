angular.module('StockApp').controller('registerCtrlr', ['$scope', '$window', '$http','$cookies', function($scope, $window, $http,$cookies) {

	$scope.sucessToRegister= false;
	$scope.failToRegister= false;
	$scope.isLoggedIn = $cookies.get('loggedInUser') ? true : false;

	$scope.onClickReg = function(){
		$http({
            method: 'POST',
            url: '/api/user/',
            headers:{
				'UserID': $scope.userId,
				'FirstName':$scope.firstName,
				'LastName':$scope.lastName
			}
        }).then(function(response) {
        	if($scope.failToRegister == true){
        		$scope.failToRegister = false;
        	}
            $scope.sucessToRegister= true;
            if($scope.isLoggedIn == false){
            	$cookies.put('loggedInUser', $scope.userId);
	        	$scope.isLoggedIn = true;
	        	$window.location.href = '/profile';
            }
        }, function(response) {
        	if($scope.sucessToRegister == false){
        		$scope.failToRegister= true;
        	}
        });

	};

	$scope.idValidate = function() {
		var bool = true;
		

		if((''+$scope.userId).length < 6 || (''+$scope.userId).length > 15 || angular.isUndefined($scope.userId)) {
			bool = false;
		}

		return bool;
	};

	$scope.fNameValidate = function() {
		var bool = true;

		if(angular.isUndefined($scope.firstName) || (''+$scope.firstName).length < 1) {
			bool = false;
		}

		return bool;
	};


	$scope.lNameValidate = function() {
		var bool = true;
		

		if(angular.isUndefined($scope.lastName) || (''+$scope.lastName).length < 1) {
			bool = false;
		}

		return bool;
	};



	$scope.regValidate = function() {
		var bool = true;
		$scope.regButton = {};
		$scope.regButton.style = {"color":"black"};

		if((''+$scope.userId).length < 6 || (''+$scope.userId).length > 15 || angular.isUndefined($scope.userId) || angular.isUndefined($scope.firstName) || (''+$scope.firstName).length < 1 || angular.isUndefined($scope.lastName) || (''+$scope.firstName).length < 1) {
			$scope.regButton.style = {"color":"grey"};
			bool = false;
		}

		return bool;

	};


}]);