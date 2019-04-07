// testing controller
describe('RegisterController', function() {
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
      return $controller('registerCtrlr', {'$scope' : $rootScope });
    };
  }));

  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should defined all scope variable', function() {
    var controller = createController();
    expect($rootScope.sucessToRegister).toBe(false);
    expect($rootScope.failToRegister).toBe(false);
  });

  it('should post invest information ', function() {
    var controller = createController();
    $httpBackend.when('POST', '/api/user/')
      .respond();
    $rootScope.onClickReg();
    $httpBackend.flush();
    if($rootScope.failToRegister == true){
      expect($rootScope.failToRegister).toBe(false);
    }
    expect($rootScope.sucessToRegister).toBe(true);
  });

  it('should fail post invest information ', function() {
    var controller = createController();
    $httpBackend.when('POST', '/api/user/')
      .respond(401, '');
    $rootScope.onClickReg();
    $httpBackend.flush();
    if($rootScope.sucessToRegister == false){
      expect($rootScope.failToRegister).toBe(true);
    }
  });

});