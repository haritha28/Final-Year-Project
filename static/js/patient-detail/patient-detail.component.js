var sensorType = [];
angular.module('spandanam').component('patientDetail', {
    templateUrl: '../static/js/patient-detail/patient-detail.template.html',
    controller: ['$routeParams', '$http', '$scope',
        function PatientDetailController($routeParams, $http, $scope) {
            this.mrd = $routeParams.mrd;
            var self = this;
            $http.get('/getPatientList').then(function (response) {
                self.patient = response.data;
            });

            var j = 0;
            var link = '/getSensorTypes/'.concat($routeParams.mrd);
            var result = $http.get(link).then(function (response, $scope) {
                var sensorType = [];
                for (i = 0; i < response.data.length; i++) {
                    sensorType.push(response.data[i][0]);
                    j++;
                }
                var select = document.getElementById('selectSensor');

                var i;
                for (i = 0; i < sensorType.length; i++) {
                    /*var requiredType = sensorType[i].concat("::");
                     requiredType = requiredType.concat(sensorType[i + 1]);
                     requiredType = requiredType.concat("-->");
                     requiredType = requiredType.concat(sensorType[i + 2]);*/
                    var opt = sensorType[i];
                    var el = document.createElement("option");
                    el.textContent = opt;
                    el.value = opt;
                    select.appendChild(el);
                }
                $("#selectSensor").change(function () {
                    name = $(this).find(":selected").text();
                    console.log(name);

                    var linkNext = '/getTimeStamps/'.concat($routeParams.mrd);
                    $http.get(linkNext).then(function (response, $scope) {
                        var sensorTime = [];
                        for (i = 0; i < response.data.length; i++) {
                            console.log(name);
                            if (response.data[i][0] == name) {
                                requiredType = response.data[i][1];
                                requiredType = requiredType.concat("--->");
                                requiredType = requiredType.concat(response.data[i][2]);
                                sensorTime.push(requiredType);
                            }
                        }

                        var selectTime = document.getElementById('selectTime');
                        $('#selectTime').empty();
                        for (i = 0; i < sensorTime.length; i++) {
                            var opt = sensorTime[i];
                            var el = document.createElement("option");
                            el.textContent = opt;
                            el.value = opt;
                            selectTime.appendChild(el);
                        }
                    });


                });

            });


        }
    ]

});