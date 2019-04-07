// testing controller
describe('SigininController', function() {
  var $httpBackend, $rootScope, createController, authRequestHandler;
  // Set up the module
  beforeEach(module('StockApp'));
  beforeEach(inject(function($injector) {
    // Set up the mock http service responses
    $httpBackend = $injector.get('$httpBackend');
    // Get hold of a scope (i.e. the root scope)
    $rootScope = $injector.get('$rootScope');
    // The $controller service is used to create instances of controllers
    var $controller = $injector.get('$controller');
    createController = function() {
      return $controller('signinCtrlr', {'$scope' : $rootScope});
    };
  
  }));

  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

    it('should fetch all users', function() {
      var controller = createController();
      $httpBackend.when('GET', '/api/user/')
        .respond();
      $rootScope.generateUserList();
      $httpBackend.flush();
      expect($rootScope.userList).not.toBe(null);
  });

});