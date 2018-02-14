var $yValue = "base";
var $point1 = "";
var $point2 = "";
angular
    .module('sensorDisplay', ['ngRoute'])
    .component('spandanam', {
        templateUrl: '../static/js/sensor-display/sensor-display.template.html'
    })
    .controller('sensorDisplayController',
        function ($routeParams, $http, $scope, $window) {
            sensorId = $routeParams.mrd;
            var self = this;
            var $file;
            var typess = [];
            var result;

            if (idValue == 4) {
                var linkDB = '/getFileLocation/'.concat($routeParams.mrd);

                result = $http.get(linkDB).then(function (response, $scope) {
                    for (i = 0; i < response.data.length; i++) {
                        UpdatedTime = response.data[i][1];
                        UpdatedTime = UpdatedTime.concat("--->");
                        UpdatedTime = UpdatedTime.concat(response.data[i][2]);
                        console.log(UpdatedTime);
                        console.log(timeSelected);
                        if ((typeSelected == (response.data[i][0])) && (timeSelected == UpdatedTime)) {
                            $file2 = response.data[i][4].concat(response.data[i][3]);
                            $yValue = typeSelected;
                            return $file2;
                        }
                    }
                });
            }
            else {
                result = $http.get('/getEMRList').then(function (response, $scope) {
                    emr = response.data;

                    for (i = 0; i < response.data.length; i++) {
                        if (sensorId == (response.data[i][0])) {
                            $file2 = response.data[i][5].concat(response.data[i][2]);
                            $yValue = response.data[i][1];
                            return $file2;
                        }
                    }
                });
            }
            result.then(function () {

                var time = "";
                console.log("Printing idValue here:" + idValue);
                if (idValue == 1) {
                    update = 60;
                    time = "Real time "

                }
                else if (idValue == 2) {
                    update = 60 * 24;
                    time = "24 hour "

                }
                else if (idValue == 3) {
                    update = 60 * 24 * 100;
                    time = "All time "
                }
                else if (idValue == 4) {

                    update = 1;
                    time = $yValue;
                }
                title = time.concat(" graph");
                document.getElementById("graphTitle").innerHTML = title;
                /*if(typeSelected=="ECG")
                 {
                 firstButton= "Analyze for ST";

                 }
                 else
                 {
                 firstButton= "Analyze for AHE";
                 }
                 */
                document.getElementById("analyzeButton").innerHTML = "Analyze data";
                document.getElementById("analyzeButton").onclick = function displaySomething() {
                    document.getElementById("analyticsPanel").innerHTML = "We have send the above data for analysis. " +
                        "The results will appear here as soon as we get it!!"

                    if ($yValue === "ECG")
                        analyzeRoute = '/analyzeECGData';
                    else if ($yValue === "SPO2")
                        analyzeRoute = '/analyzeSPO2Data';
                    else if ($yValue === "AHE Predict")
                        analyzeRoute = '/analyzeAHEPData';
                    else if ($yValue === "AHE Classify")
                        analyzeRoute = '/analyzeAHECData';
                    else if ($yValue === "IHR")
                        analyzeRoute = '/analyzeIHRData';
                    else
                        analyzeRoute = '/analyzeBPData';

                    $http.post(
                        url = analyzeRoute,
                        data = $file2).then(function (response, $scope) {
                        document.getElementById("analyticsPanel").innerHTML = response.data;
                    });


                }

                Plotly.d3.csv($file2, function (rows) {

                    var file = "static/patient_EMR_logs/a06.csv"
                    console.log(file)
                    $file2 = file
                    console.log($file2)
                    rows.map(function (row) {
                        // set the x-data
                        return row['Time'];
                    })
                    var timeList = [];
                    var dataList = [];
                    testDate = new Date();
                    index = -1;
                    for (i = 0; i < rows.length; i++) {
                        //console.log(rows[i].Time);
                        //testDate= rows[i].Time;
                        testDate = new Date(timeList[index]);
                        var ts = Math.round(new Date().getTime() / 1000);
                        /*var tsYesterday = ts - (24 * 3600);
                         console.log(tsYesterday);
                         console.log("The above is the time:");

                         */

                        var hour = 1000 * 60 * update;
                        var day = new Date();
                        var result = (day - (new Date(rows[i].Time)));
                        //  if (rows[i].Mrid == $scope.sensorId) {

                        if (idValue == 4) {
                            index++;
                            //console.log(rows[i].Datapoint);
                            dataList[index] = rows[i].Datapoint;
                            timeList[index] = rows[i].Time;
                            testDate = timeList[index];
                            testDate = new Date(timeList[index]);
                        }
                        else {
                            if (result <= hour) {
                                index++;
                                //console.log(rows[i].Datapoint);
                                dataList[index] = rows[i].Datapoint;
                                timeList[index] = rows[i].Time;
                                testDate = timeList[index];
                                testDate = new Date(timeList[index]);
                                //console.log("The time is:" +testDate + " and the hour is " + testDate.getHours());

                            }
                        }
                        // }
                    }

                    var trace = {
                        type: 'scatter',                    // set the chart type
                        mode: 'lines',                      // connect points with lines
                        x: timeList,
                        y: dataList,
                        point: {                             // set the width of the line.
                            width: 2
                        }
                    };
                    var layout = {
                        // title: title,
                        yaxis: {
                            title: $yValue,

                            titlefont: {
                                family: 'Courier New, monospace',
                                size: 16,
                                color: 'black'
                            },
                        },       // set the y axis title
                        xaxis: {
                            title: "",

                            titlefont: {
                                family: 'Courier New, monospace',
                                size: 16,
                                color: 'red'
                            },

                            showgrid: true,          // customize the date format to "month, day"
                            //tickformat: "%H:%M:%S, %D:%B:%Y"
                            tickformat: "%d-%m-%Y %H:%M"
                        },
                        plot_bgcolor: 'white',
                        paper_bgcolor: '#eee',
                        margin: {                           // update the left, bottom, right, top margin
                            l: 44, b: 63, r: 15, t: 25
                        }
                    };

                    Plotly.newPlot(document.getElementById('tester'), [trace], layout, {showLink: false});
                });
            });

        }
    );