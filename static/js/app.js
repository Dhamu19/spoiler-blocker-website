var app = angular.module('SpoilerBlockerWebsite', ['ngRoute', 'ui.bootstrap']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.config(function($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl : '../static/angulartemplates/lists.html',
				controller  : 'BrowseController'
			})
			.when('/createList', {
				templateUrl : '../static/angulartemplates/createList.html',
				controller  : 'CreateController'
			})
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

app.controller('HomeController', function($scope, Lists) {
  $scope.emptyQuery = function() {
    Lists.query = '';
  }
})

app.controller('BrowseController', function($scope, $http, Lists, $window) {
  $scope.round = $window.Math.round;
  $scope.lists = {};

  $scope.getLists = function(query) {
    Lists.getLists(query).then(function(response) {
      // response.data is array of json objects
      var listObj = {};
      for (var i=0; i<response.data.length; i++) {
        var id = response.data[i]['id'];
        listObj[id] = response.data[i];
      }

      $scope.lists = listObj;
		});
	};

  $scope.rateList = function(listID, rating) {
    $scope.lists[listID].user_rating_from_cookie = rating;
    $http({
      method: 'POST',
      url: '/rateList',
      data: {
       id: listID,
       rating: rating
      },
      headers: {'Content-Type': 'json'}
    }).then(function(response) {
      $scope.lists[listID].rating = response.data.newRating;
    })
  }

  $scope.$watch(function () { return Lists.query; }, function (newValue, oldValue) {
    if (newValue) {
      $scope.getLists(Lists.query);
    }
  });

  $scope.getLists(Lists.query);
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
    if ($location.path() != '/') {
      $location.path('/');
    }
    Lists.query = $scope.asyncSelected;
    $scope.asyncSelected = '';
  }

  $scope.navigateToCreate = function () {
    $location.path('/createList');
  }
})
