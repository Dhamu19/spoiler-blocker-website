var app = angular.module('SpoilerBlockerWebsite', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('BrowseController', function($scope, $http) {
	$scope.Math = window.Math;
	$scope.lists = [];

	$scope.getLists = function(numLists) {
		$http({
			method: 'POST',
 			url: '/getLists',
 			data: {
				numLists: numLists
			},
			headers: {'Content-Type': 'json'}
		}).then(function(data) {
			console.log(data);
			$scope.lists = data.data;
		});
	};
	$scope.range = function(n) {
    return new Array(n);
  };

	$scope.getLists(10);
});
