// testing controller
describe('StockController', function() {
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
      return $controller('stockCtrlr', {'$scope' : $rootScope });
    };
  }));

  afterEach(function() {
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  it('should defined all scope variable', function() {
    var controller = createController();
    expect($rootScope.showStockRealtime).toBe(false);
    expect($rootScope.showStockHistory).toBe(false);
    expect($rootScope.showErrorTable).toBe(false);
    expect($rootScope.showLoggedInError).toBe(false);
    expect($rootScope.showIntAmtError).toBe(false);
    expect($rootScope.showBalanceError).toBe(false);
    expect($rootScope.disableInvest).toBe(false);
  });

  it('should fetch stock information ', function() {
    var controller = createController();
    $httpBackend.when('GET', '/api/stock/test')
      .respond({stock_name: 'test_name', stock_open: '100',stock_price: '200'});
    $rootScope.fetchRealtimeData('test');
    $httpBackend.flush();
    expect($rootScope.stockRealtimeInfo.stock_name).toEqual('test_name');
    expect($rootScope.stockRealtimeInfo.stock_open).toEqual('100');
    expect($rootScope.stockRealtimeInfo.stock_price).toEqual('200');
    expect($rootScope.status).toEqual(200);
    expect($rootScope.showStockRealtime).toBe(true);
    expect($rootScope.showErrorTable).toBe(false);
  });

  it('should fail to fetch stock information ', function() {
    var controller = createController();
    $httpBackend.when('GET', '/api/stock/test')
      .respond(401, '');
    $rootScope.fetchRealtimeData('test');
    $httpBackend.flush();
    expect($rootScope.status).toEqual(401);
    expect($rootScope.showStockRealtime).toBe(false);
    expect($rootScope.showStockHistory).toBe(false);
    expect($rootScope.showErrorTable).toBe(true);
  });

  it('should fetch stock history information ', function() {
    var controller = createController();
    $httpBackend.when('GET', '/api/stock/test/history')
      .respond({Adj_Close:"100", Close:"200", Date:"2017-02-24", 
               High:"300", Low:"50", Open:"120", Symbol:"test_name", Volume: "123456"});
    $rootScope.fetchHistoricalData('test');
    $httpBackend.flush();
    expect($rootScope.stockHistoryInfo.Adj_Close).toEqual('100');
    expect($rootScope.stockHistoryInfo.Close).toEqual('200');
    expect($rootScope.stockHistoryInfo.Date).toEqual('2017-02-24');
    expect($rootScope.stockHistoryInfo.High).toEqual('300');
    expect($rootScope.stockHistoryInfo.Low).toEqual('50');
    expect($rootScope.stockHistoryInfo.Open).toEqual('120');
    expect($rootScope.stockHistoryInfo.Symbol).toEqual('test_name');
    expect($rootScope.stockHistoryInfo.Volume).toEqual('123456');
    expect($rootScope.status).toEqual(200);
    expect($rootScope.showStockHistory).toBe(true);
  });

  it('should fail to fetch stock history information ', function() {
    var controller = createController();
    $httpBackend.when('GET', '/api/stock/test/history')
      .respond(401, '');
    $rootScope.fetchHistoricalData('test');
    $httpBackend.flush();
    expect($rootScope.status).toEqual(401);
    expect($rootScope.showStockHistory).toBe(false);
  });

  it('should post invest information ', function() {
    var controller = createController();
    $httpBackend.when('POST', '/api/invest/buy/')
      .respond();
    $rootScope.fetchInvest();
    $httpBackend.flush();
    expect($rootScope.status).toEqual(200);
  });

  it('should fail post invest information ', function() {
    var controller = createController();
    $httpBackend.when('POST', '/api/invest/buy/')
      .respond(401, '');
    $rootScope.fetchInvest();
    $httpBackend.flush();
    expect($rootScope.status).toEqual(401);
    expect($rootScope.showStockHistory).toBe(false);
  });

  it('Should check function return true for integer', function(){
    var controller = createController();
    var result = $rootScope.isInt(1);
    expect(result).toBe(true);

  });

  it('Should check function return false for non integer', function(){
    var controller = createController();
    var result = $rootScope.isInt("test");
    expect(result).toBe(false);
  });

});