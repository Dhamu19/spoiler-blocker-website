var app = angular.module('SpoilerBlockerWebsite', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('MainController', function($scope, $http) {
	$scope.testVar = null;
	$scope.testHtml = function() {
		$http({
			method: 'POST',
 			url: '/testRoute',
 			data: {
				testData: "Bye"
			},
			headers: {'Content-Type': 'json'}
		}).then(function(data) {
			console.log(data);
			$scope.testVar = data.data;
		});
	};
	$scope.testHtml();
});
