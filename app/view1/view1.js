'use strict';

angular.module('myApp.view1', ['ngRoute',
    'ngAnimate',
    'mgcrea.ngStrap'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view1', {
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ['$rootScope', '$scope', '$http', '$location', '$log', '$modal', function ($rootScope, $scope, $http, $location, $log, $modal) {

        $http.get('../series.json').success(function (data) {
            $scope.series = data;
            $log.debug('$scope.series inside success = ' + $scope.series);
        });

        $log.debug('View1Ctrl called...');
        $log.debug('$scope.series = ' + $scope.series);
/*
        var myOtherModal = $modal({scope: $scope, template: 'modal/docs/modal.demo.tpl.html', show: false});
        // Show when some event occurs (use $promise property to ensure the template has been loaded)
        $scope.showModal = function() {
            myOtherModal.$promise.then(myOtherModal.show);
        };
*/
    }]);