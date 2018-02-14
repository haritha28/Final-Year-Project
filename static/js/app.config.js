angular.
  module('spandanam').
  config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/patients', {
        }).
        when('/patients/:mrd', {
          template: '<patient-detail></patient-detail>'
        }).
          when('/patients/:mrd/plot', {
          template: '<patient-detail></patient-detail><spandanam></spandanam>'
        }).
        otherwise('/patients');
    }
  ]);