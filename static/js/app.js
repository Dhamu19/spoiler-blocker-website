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
  // $locationProvider.html5Mode(true);
});

app.factory('Query', function($http){
  return {
    query: ''
  };
});

app.controller('HomeController', function($scope, Query) {
  $scope.emptyQuery = function() {
    Query.query = '';
  }
})

app.controller('BrowseController', function($scope, $http, Query, $window) {
  $scope.round = $window.Math.round;
  $scope.lists = {};
  $scope.numLists = null;
  $scope.currentPage = 1;
  $scope.postsPerPage = null;

  $scope.getPostsPerPage = function () {
    $http({
      method: 'GET',
      url: '/postsPerPage',
      headers: {'Content-Type': 'json'}
    }).then(function(response) {
      $scope.postsPerPage = response.data;
    })
  }

  $scope.getLists = function(){
    $http({
      method: 'POST',
      url: '/getLists',
      data: {
        query: Query.query,
        pageNum: $scope.currentPage
      },
      headers: {'Content-Type': 'json'}
    }).then(function(response) {
      // response.data is array of json objects
      var listObj = {};
      var result = response.data.result;

      if (response.data.count != -1) {
        $scope.numLists = response.data.count;
      }

      for (var i=0; i<result.length; i++) {
        var id = result[i]['id'];
        listObj[id] = result[i];
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

  $scope.$watch(function () { return Query.query; }, function (newValue, oldValue) {
    if (newValue) {
      $scope.getLists(Query.query);
    }
  });

  $scope.getPostsPerPage();
  $scope.getLists();
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

app.controller('NavController', function($scope, $http, Query, $location) {
  $scope.asyncSelected = undefined;

  $scope.getTitles = function(query) {
    return $http({
      method: 'POST',
      url: '/getTitles',
      data: {
        query: query
      },
      headers: {'Content-Type': 'json'}
    }).then(function(response) {
      return response.data;
  	});
  }

  $scope.submitSearch = function() {
    if ($location.path() != '/') {
      $location.path('/');
    }
    Query.query = $scope.asyncSelected;
    $scope.asyncSelected = '';
  }

  $scope.navigateToCreate = function () {
    $location.path('/createList');
  }
})
