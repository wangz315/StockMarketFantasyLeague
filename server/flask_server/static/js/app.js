angular.module('StockApp', ['ngRoute', 'ngCookies'])
.config(function($routeProvider, $locationProvider) {
  $routeProvider
  .when('/', {
    templateUrl: 'static/partials/home.html'
  })
  .when('/stocks', {
    templateUrl: 'static/partials/stocks.html',
    controller: 'stockCtrlr'
  })
  .when('/register', {
    templateUrl: 'static/partials/register.html',
    controller: 'registerCtrlr'
  })
  .when('/signin', {
    templateUrl: 'static/partials/signin.html',
    controller: 'signinCtrlr'
  })
  .when('/profile', {
    templateUrl: 'static/partials/profile.html',
    controller: 'profileCtrlr'
  })
  .when('/404', {
    templateUrl: 'static/partials/404.html'
  })
  .otherwise({
        redirectTo: '/404'
   })
  $locationProvider.html5Mode({
    enabled: true,
    requireBase: false
  });
}).directive('chart', function () {
    return {
        restrict:'E',
        template:'<div></div>',
        transclude:true,
        replace:true,
        scope: '=',
        link:function (scope, element, attrs) {
            var opt = {
                chart:{
                    renderTo:element[0],
                    type:'line',
                    marginRight:10,
                    marginBottom:40,
                    backgroundColor:'transparent'
                },
                title:{
                    text:attrs.title,
                    x:-20 //center
                },
                subtitle:{
                    text:attrs.subtitle,
                    x:-20
                },
                xAxis:{
                    tickInterval:1,
                    title:{
                        text:attrs.xname
                    }
                },
                plotOptions:{
                    lineWidth:0.3,
                    allowPointSelect: true
                },
                yAxis:{
                    title:{
                        text:attrs.yname
                    },
                    tickInterval:(attrs.yinterval)?new Number(attrs.yinterval):null,
                    max:attrs.ymax,
                    min: attrs.ymin
                },tooltip:{
                    formatter:scope[attrs.formatter]||function () {
                        return '<b>' + this.y + '</b>'
                    }
                },legend:{
                    layout:'vertical',
                    align:'right',
                    verticalAlign:'top',
                    x:-10,
                    y:20,
                    borderWidth: 1
                },credits: {
                    enabled: false
                },
            }
            //Update when charts data changes
            scope.$watch(function (scope) {
                return JSON.stringify({
                    xAxis:{
                        categories:scope[attrs.xdata]
                        },title:{
                            text: "Historical Information"
                        },
                    series:scope[attrs.ydata]
                });
            }, function (news) {
                news = JSON.parse(news)
                if (!news.series)return;
                angular.extend(opt,news)
                var chart = new Highcharts.Chart(opt);
            });
        }
    }

});
