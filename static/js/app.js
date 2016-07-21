var app = angular.module('SpoilerBlockerWebsite', ['ngRoute', 'ui.bootstrap']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.config(function($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl : '../static/angulartemplates/home.html',
				controller  : 'HomeController'
			})
			.when('/createList', {
				templateUrl : '../static/angulartemplates/createList.html',
				controller  : 'CreateController'
			})
			.when('/browseLists', {
				templateUrl : '../static/angulartemplates/lists.html',
				controller  : 'BrowseController'
			})
      // .when('/searchLists', {
			// 	templateUrl : '../static/angulartemplates/searchLists.html',
			// 	controller  : 'SearchController'
			// })
      .otherwise({
        redirectTo: '/'
      });
});

app.factory('Lists', function($http){
  var getLists = function(query){
     return $http({
        method: 'POST',
        url: '/getLists',
        data: {
          query: query
        },
        headers: {'Content-Type': 'json'}
    })
  }
  return {
    query: '',
    getLists: getLists
  };
});

app.controller('HomeController', function($rootScope, $scope, Lists) {
  $scope.emptyQuery = function() {
    Lists.query = '';
  }
})

app.controller('BrowseController', function($scope, $http, Lists) {
  $scope.lists = [];

  $scope.getLists = function(query) {
    Lists.getLists(query).then(function(response) {
      $scope.lists = response.data;
		});
	};

  $scope.$watch(function () { return Lists.query; }, function (newValue, oldValue) {
    if (newValue) {
      $scope.getLists(Lists.query);
    }
  });

  $scope.getLists(Lists.query);

	// $scope.getLists = function(query){
	// 	$http({
	// 		method: 'POST',
 // 			url: '/getLists',
 // 			data: {
	// 			query: query
	// 		},
	// 		headers: {'Content-Type': 'json'}
	// 	}).then(function(response) {
	// 		$scope.lists = response.data;
	// 	});
	// };
  //
  // $scope.$on('query', function (event, arg) {
  //   $scope.getLists(arg);
  // });
});

app.controller('CreateController', function($scope, $http) {
	$scope.createForm = {};

	$scope.submitForm = function () {
		$http({
			method: 'POST',
 			url: '/createList',
 			data: $scope.createForm,
			headers: {'Content-Type': 'json'}
		}).then(function(data) {
			console.log(data);
		});
		$scope.createForm = {};
	}
})

app.controller('NavController', function($scope, $http, Lists, $location) {
  $scope.asyncSelected = undefined;

  $scope.getTitles = function(query) {
    return Lists.getLists(query).then(function(response) {
      return response.data.map(function(item) {
        return item.title;
      });
		});
  }

  $scope.submitSearch = function() {
    if ($location.path() != '/browseLists') {
      $location.path('/browseLists');
    }
    Lists.query = $scope.asyncSelected;
    $scope.asyncSelected = '';
  }
})
