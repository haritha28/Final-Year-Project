// Register `patient-list` component, along with its associated controller and template
angular.
  module('spandanam').
  component('patientList', {
    templateUrl:'../static/js/patient-list/patient-list.template.html',
    controller: function PatientListController($http) {
      var self=this;
      $http.get('/getPatientList').then(function(response) {
        self.patients = response.data;
      });
    }
  });