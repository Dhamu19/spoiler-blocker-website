var app = angular.module('SpoilerBlockerWebsite', ['ngRoute', 'ui.bootstrap']);

// Change the interpolation since Jinja2 uses {{}}
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

// To share query between NavController and BrowseController
app.factory('Query', function($http){
  return {
    query: ''
  };
});

app.controller('BrowseController', function($scope, $http, Query, $window) {
  $scope.round = $window.Math.round;
  $scope.lists = {};
  $scope.numLists = null;
  $scope.currentPage = 1;
  $scope.postsPerPage = null;

  // Fired once to get how many posts there are per page
  $scope.getPostsPerPage = function () {
    $http({
      method: 'GET',
      url: '/postsPerPage',
      headers: {'Content-Type': 'json'}
    }).then(function(response) {
      $scope.postsPerPage = response.data;
    })
  }

  // Asks server for lists based on the query and
  // the current page number
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

      // If page num is 1, then count will not be -1
      // If count isn't -1, then update it in the scope
      if (response.data.count != -1) {
        $scope.numLists = response.data.count;
      }

      // Transform list of objects into an object keyed
      // by list ID. Makes list updates faster
      for (var i=0; i<result.length; i++) {
        var id = result[i]['id'];
        listObj[id] = result[i];
      }

      $scope.lists = listObj;
		});
	};

  $scope.rateList = function(listID, rating) {
    // To make stars persist
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
      // Update rating in view
      $scope.lists[listID].rating = response.data.newRating;
    })
  }

  // Watch for changes in query, if changes then
  // Get lists for query and change pagination page to 1
  $scope.$watch(function () { return Query.query; }, function (newValue, oldValue) {
    if (newValue || newValue == '') {
      $scope.currentPage = 1;
      $scope.getLists();
    }
  });

  // Fired once
  $scope.getPostsPerPage();
  // Initial list load
  $scope.getLists();
});

app.controller('CreateController', function($scope, $http, $timeout) {
	$scope.createForm = {};
  $scope.displayAlert = false;

  // Submit form to server, display success alert
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
    $scope.displayAlert = true;

    $timeout(function () {
      // Remove alert after 3 seconds
			$scope.displayAlert = false;
		}, 3000);
	}
})

app.controller('NavController', function($scope, $http, Query, $location) {
  $scope.asyncSelected = undefined;
  $scope.noResults = true;

  // Get titles of lists that match the query
  // These titles are used in the autocomplete
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

  // Go to list browsing view
  // Update query
  $scope.submitSearch = function() {
    Query.query = $scope.asyncSelected;
    if ($location.path() != '/') {
      $location.path('/');
    }
  }

  // Go to createList view
  $scope.navigateToCreate = function () {
    $location.path('/createList');
  }

  $scope.allLists = function () {
    Query.query = '';
    $scope.asyncSelected = '';
  }
})
