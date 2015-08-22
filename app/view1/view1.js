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

        $scope.serieVisible = null;
        $scope.editSerie = null;
        $scope.editSerieCopy = {};
        $scope.editField = [];

        function saveSeries() {
            $http.put('series.json', $scope.series).success(function(data, status, headers, config) {
                $log.debug('status: ' + status);
            }).error(function(data, status, headers, config) {
                $modal({title: 'Error', content: 'Status: '+status+' while saving data to server...', show: true});
            });
        }

        $scope.confirmDelete = function(serie) {
            var modal1 = $modal({scope: $scope, template: 'templates/modal-yesno-tmpl.html',
                title: 'Delete '+serie.name+'?', content:'Do you really want to delete '+serie.name+' serie?',
                show: false, prefixEvent: 'confirmDelete', serie: serie});
            modal1.$promise.then(modal1.show);
        };

        $scope.$on('confirmDelete.hide' , function(element, modal) {
            if(element.targetScope.deleteit == true) {
                var idx = $scope.series.indexOf(modal.$options.serie);
                $scope.series.splice(idx, 1);

                saveSeries();
            }
        });

        $scope.showDetails = function(serie) {
            $scope.serieVisible = serie;
/*
            if ($scope.serieVisible != null) {
                serie.style = {position: 'absolute', top:'0px'};
            } else {
                serie.style = {position: 'relative', top:'auto'};
            }
*/
        };

        $scope.showEdit = function(serie, field) {
            $scope.editSerie = serie;
            angular.copy(serie, $scope.editSerieCopy);
            $scope.editField[serie.name+field] = true;
        };

        $scope.processKey = function(event, field) {
            if (event.keyCode == 27) {
                angular.copy($scope.editSerieCopy, $scope.editSerie);
                $scope.editField[$scope.editSerie.name+field] = false;
            } else if (event.keyCode == 13) {
                saveSeries();
                $scope.editField[$scope.editSerie.name+field] = false;
            }
        };

        $scope.saveSerie = function() {
            saveSeries();
        }
    }]);