angular.module('StockApp').controller('homeCtrlr', ['$scope', '$cookies', '$location', '$window', function($scope, $cookies, $location, $window) {
    $scope.getClass = function(path) {
        return ($location.path() === path) ? 'active' : '';
    };
    
    $scope.isLoggedIn = $cookies.get('loggedInUser') ? true : false;
    
    $scope.logOut = function() {
        $cookies.remove('loggedInUser');
        $scope.isLoggedIn = false;
        $window.location.href = '/';
    };
}]);