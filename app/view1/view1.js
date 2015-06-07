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

        $scope.confirmDelete = function(serie) {
            var modal1 = $modal({scope: $scope, template: 'templates/modal-yesno-tmpl.html',
                title: 'Delete '+serie.name+'?', content:'Do you really want to delete '+serie.name+' serie?',
                show: false, prefixEvent: 'confirmDelete', serie: serie});
            modal1.$promise.then(modal1.show);
        };

        $scope.$on('confirmDelete.hide' , function(element, modal1) {
            if(element.targetScope.deleteit == true) {
                var idx = $scope.series.indexOf(modal1.$options.serie);
                $scope.series.splice(idx, 1);

                $http.put('../series.json', $scope.series).success(function(data, status, headers, config) {
                    $log.debug('status: ' + status);
                }).error(function(data, status, headers, config) {
                    $modal({title: 'Error', content: 'Status: '+status+' while saving data to server...', show: true});
                });
            }
        });
    }]);