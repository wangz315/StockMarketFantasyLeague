describe('Test stock page', function() {
  browser.get('/');
  var homeTitle = element(by.id('title'));
  var stockButton = element(by.id('stocks-button'));
  var profileButton = element(by.id('profile-button'));
  var signinButton = element(by.id('signin-button'));
  var registerButton = element(by.id('register-button'));
  var logoutButton = element(by.id('logout-button'));

  function makeid()
  {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 7; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
  }


  beforeEach(function() {
    var origFn = browser.driver.controlFlow().execute;

    browser.driver.controlFlow().execute = function() {
      var args = arguments;
      origFn.call(browser.driver.controlFlow(), function() {
        return protractor.promise.delayed(30);
      });

      return origFn.apply(browser.driver.controlFlow(), args);
    };
  });
  
  it('should have a title', function() {
    expect(homeTitle.getText()).toEqual('Stock Fantasy League');
  });

  it('should be able to sign in', function() {
    signinButton.click();
    element.all(by.id('userID')).get(1).click();


  });
  
  it('should be able to search stocks and invest', function() {
    browser.sleep(2000);
    stockButton.click();
    var searchInput = element(by.id('stockSymbolInput'));
    var searchButton = element(by.id('search-button'));
    var investmentInput = element(by.id('amountInvest'));
    var investmentConfirmButton = element(by.id('investmentConfirm-button'));
    var investmentModalConfirmButton = element(by.id('investmentModalConfirm-button'));
    searchInput.sendKeys("goog");
    searchButton.click();
    investmentInput.sendKeys(1);
    investmentConfirmButton.click();
    investmentModalConfirmButton.click();
  });

  it('should be able to sell stocks and view profile', function() {
    browser.sleep(2000);
    profileButton.click();
    element.all(by.id('sell_button')).get(1).click();
  });

   it('should be able to register', function() {
    logoutButton.click();
    registerButton.click();
    var userIDInput= element(by.id('userID-input'));
    var firstNameInput = element(by.id('firstName-input'));
    var lastNameInput = element(by.id('lastName-input'));
    var registerConfirmButton = element(by.id('registerConfirm-button'));
    userIDInput.sendKeys(makeid());
    firstNameInput.sendKeys(makeid());
    lastNameInput.sendKeys(makeid());
    registerConfirmButton.click();
  });

  it('should be able to log out', function() {
    logoutButton.click();
  });

});