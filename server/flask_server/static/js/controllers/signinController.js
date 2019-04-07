angular.module('StockApp').controller('signinCtrlr', ['$scope', '$cookies', '$http', '$window', function($scope, $cookies, $http, $window) {
    $scope.signInBusinessLogic = function() {
        if ($cookies.get('loggedInUser') != null) {
            $http({
                method: 'GET',
                url: '/api/user/' + $cookies.get('loggedInUser')
            }).then(function(response) {
                $window.location.href = '/profile';
            }, function(response) {
                $cookies.remove('loggedInUser');                
                $scope.generateUserList();
            });
        } else {
            $scope.generateUserList();
        }
    };
    
    $scope.generateUserList = function() {
        $http({
            method: 'GET',
            url: '/api/user/'
        }).then(function(response) {
            $scope.userList = response.data;
        }, function(response) {
        });
    };
    
    $scope.signInUser = function(userID) {
        $cookies.put('loggedInUser', userID);       
        $window.location.href = '/profile';
    };
    
    $scope.signInBusinessLogic();
}]);