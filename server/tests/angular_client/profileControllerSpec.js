// testing controller
describe('ProfileController', function() {
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
      return $controller('profileCtrlr', {'$scope' : $rootScope});
    };
  
  }));

  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should defined all scope variable', function() {
    var controller = createController();
    expect($rootScope.showUserInfo).toBe(false);
    expect($rootScope.showErrorTable).toBe(false);
  });
});