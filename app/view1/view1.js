'use strict';

angular.module('myApp.view1', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view1', {
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ['$rootScope', '$scope', '$http', '$location', '$log', function ($rootScope, $scope, $http, $location, $log) {

        $http.get('../series.json').success(function (data) {
            $scope.series = data;
        });

        $scope.gotoEdit = function(serie){
            $rootScope.serieToEdit = serie;
            $location.path('/view2');
        };
    }]);