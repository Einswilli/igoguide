//[Dashboard Javascript]

//Project:	Maximum Admin - Responsive Admin Template
//Primary use:   Used only for the main dashboard (index.html)


$(function () {

  'use strict';
	
	window.Apex = {
		stroke: {
		  width: 2
		},
		markers: {
		  size: 0
		},
		tooltip: {
		  fixed: {
			enabled: true,
		  }
		}
    };
	var options1 = {
          series: [{
          data: [25, 66, 41, 89, 63, 36, 9, 54]
        }],
          chart: {
          type: 'line',
          width: 150,
          height: 50,
          sparkline: {
            enabled: true
          }
        },
		colors: ['#39DA8A'],
		stroke: {
          curve: 'smooth'
        },
        tooltip: {
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function (seriesName) {
                return ''
              }
            }
          },
          marker: {
            show: false
          }
        }
        };

        var chart1 = new ApexCharts(document.querySelector("#chart-11"), options1);
        chart1.render();
	
	
	
	var options1 = {
          series: [{
          data: [25, 55, 41, 89, 50, 25, 44, 12]
        }],
          chart: {
          type: 'line',
          width: 150,
          height: 50,
          sparkline: {
            enabled: true
          }
        },
		colors: ['#FF5B5C'],
		stroke: {
          curve: 'smooth'
        },
        tooltip: {
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function (seriesName) {
                return ''
              }
            }
          },
          marker: {
            show: false
          }
        }
        };

        var chart1 = new ApexCharts(document.querySelector("#chart-12"), options1);
        chart1.render();
	
	
	var options1 = {
          series: [{
          data: [50, 25, 44, 12, 25, 55, 41, 89]
        }],
          chart: {
          type: 'line',
          width: 150,
          height: 50,
          sparkline: {
            enabled: true
          }
        },
		colors: ['#39DA8A'],
		stroke: {
          curve: 'smooth'
        },
        tooltip: {
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function (seriesName) {
                return ''
              }
            }
          },
          marker: {
            show: false
          }
        }
        };

        var chart1 = new ApexCharts(document.querySelector("#chart-13"), options1);
        chart1.render();
	
	
	
	var options1 = {
          series: [{
          data: [25, 55, 44, 12, 41, 89, 50, 25]
        }],
          chart: {
          type: 'line',
          width: 150,
          height: 50,
          sparkline: {
            enabled: true
          }
        },
		colors: ['#FF5B5C'],
		stroke: {
          curve: 'smooth'
        },
        tooltip: {
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function (seriesName) {
                return ''
              }
            }
          },
          marker: {
            show: false
          }
        }
        };

        var chart1 = new ApexCharts(document.querySelector("#chart-14"), options1);
        chart1.render();
		 
	
	var options = {
        series: [{
          name: 'Online',
          data: [44, 55, 41, 67, 22, 43, 41, 12, 56, 51, 42, 44]
        }, {
          name: 'Offline',
          data: [13, 23, 20, 8, 13, 27, 22, 17, 28, 14, 9, 12]
        }],
        chart: {
          type: 'bar',
          height: 260,
          stacked: true,
          toolbar: {
            show: false
          },
          zoom: {
            enabled: false
          }
        },
		dataLabels: {
          enabled: false
        },
		colors:['#ef0753', '#2444e8'],
        responsive: [{
          breakpoint: 480,
        }],
        plotOptions: {
          bar: {
            horizontal: false,
			  columnWidth: '40%',
          },
        },
        xaxis: {
          categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan'],
        },
        legend: {
          position: 'top',
           horizontalAlign: 'right',
        },
        fill: {
          opacity: 1
        }
      };

      var chart = new ApexCharts(document.querySelector("#yearly-comparison"), options);
      chart.render();
	
	
	  	
	var options = {
          series: [{
          name: 'Net Profit',
          data: [44, 55, 57, 56, 61, 58, 63]
        }, {
          name: 'Revenue',
          data: [76, 85, 101, 98, 87, 105, 91]
        }],
          chart: {
          type: 'bar',
		  foreColor:"#bac0c7",
          height: 345,
			  toolbar: {
        		show: false,
			  }
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '30%',
            endingShape: 'rounded'
          },
        },
        dataLabels: {
          enabled: false,
        },
		grid: {
			show: false,			
		},
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent']
        },
		colors: ['#8950fc', '#f64e60'],
        xaxis: {
          categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
			
        },
        yaxis: {
          
        },
		 legend: {
      		show: false,
		 },
        fill: {
          opacity: 1
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return "$ " + val + " thousands"
            }
          },
			marker: {
			  show: false,
		  },
        }
        };

        var chart = new ApexCharts(document.querySelector("#recent_trend"), options);
        chart.render();
	
	new ApexCharts(document.querySelector("#chart-1"), {
        series: [{ data: [25, 66, 41, 89, 63, 25, 44, 12, 36, 9, 54, 89, 63, 25, 44] }],
        chart: { type: "bar", height: 75, sparkline: { enabled: !0 } },
        colors: ["#8950fc"],
        plotOptions: { bar: { columnWidth: "40%" } },
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: { crosshairs: { width: 1 } },
        tooltip: {
            fixed: { enabled: !1 },
            x: { show: !1 },
            y: {
                title: {
                    formatter: function (e) {
                        return "";
                    },
                },
            },
            marker: { show: !1 },
        },
    }).render();
	
	
	new ApexCharts(document.querySelector("#chart-2"), {
		 series: [{
          name: 'Net Profit',
          data: [44, 55, 57, 56, 61, 58, 63, 60, 66]
        }, {
          name: 'Revenue',
          data: [76, 85, 101, 98, 87, 105, 91, 114, 94]
        }],
        chart: { type: "area", height: 80, sparkline: { enabled: !0 } },
        colors: ['#f64e60', '#1bc5bd'],
        plotOptions: { bar: { columnWidth: "40%" } },
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: { crosshairs: { width: 1 } },
        tooltip: {
            fixed: { enabled: !1 },
            x: { show: !1 },
            y: {
                title: {
                    formatter: function (e) {
                        return "";
                    },
                },
            },
            marker: { show: !1 },
        },
    }).render();
	
	
	
	new ApexCharts(document.querySelector("#chart-3"), {
		 series: [{
          name: 'Net Profit',
          data: [44, 55, 47, 80, 61, 95, 63, 85, 66]
        }, {
          name: 'Revenue',
          data: [76, 40, 90, 60, 87, 58, 91, 74, 94]
        }],
        chart: { type: "line", height: 140, sparkline: { enabled: !0 } },
		stroke: {
          width: 2,
          curve: 'smooth'
        },
		markers: {
          size: 4,
          colors: ["#ffffff"],
          strokeColors: ['#ffa800', '#8950fc'],
          strokeWidth: 2,
          hover: {
            size: 7,
          }
        },
        colors: ['#ffa800', '#8950fc'],
        plotOptions: { bar: { columnWidth: "40%" } },
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: { crosshairs: { width: 1 } },
        tooltip: {
            fixed: { enabled: !1 },
            x: { show: !1 },
            y: {
                title: {
                    formatter: function (e) {
                        return "";
                    },
                },
            },
            marker: { show: !1 },
        },
    }).render();
	
	
	var options = {
          series: [76],
          chart: {
          type: 'radialBar',
			  height: 195,
          offsetY: -20,
          sparkline: {
            enabled: true
          }
        },
		
        stroke: {
			lineCap: "round"
		  },
        plotOptions: {
          radialBar: {
            startAngle: -90,
            endAngle: 90,
            track: {
              background: "#e7e7e7",
              strokeWidth: '100%',
              margin: 5, // margin is in pixels
            },
			hollow: {
				margin: 15,
				size: "70%"
			  },
            dataLabels: {
              name: {
                show: false
              },
              value: {
                offsetY: -2,
                fontSize: '30px'
              }
            }
          }
        },
        grid: {
          padding: {
            top: -10
          }
        },
        labels: ['Average Results'],
        };

        var chart = new ApexCharts(document.querySelector("#revenue9"), options);
        chart.render();
	
	
		
		
	
		 window.Apex = {
		  stroke: {
			width: 3
		  },
		  markers: {
			size: 0
		  },
		  tooltip: {
			fixed: {
			  enabled: false,
			}
		  }
		};

		var randomizeArray = function (arg) {
		  var array = arg.slice();
		  var currentIndex = array.length,
			temporaryValue, randomIndex;

		  while (0 !== currentIndex) {

			randomIndex = Math.floor(Math.random() * currentIndex);
			currentIndex -= 1;

			temporaryValue = array[currentIndex];
			array[currentIndex] = array[randomIndex];
			array[randomIndex] = temporaryValue;
		  }

		  return array;
		}
	
		// data for the sparklines that appear below header area
		var sparklineData = [47, 45, 54, 38, 56, 24, 65, 31, 37, 39, 62, 51, 35, 41, 35, 27, 93, 53, 61, 27, 54, 43, 19, 46];

		 var spark3 = {
		  chart: {
			type: 'area',
			height: 210,
			sparkline: {
			  enabled: true
			},
		  },
		  stroke: {
			curve: 'smooth'
		  },
		  fill: {
			opacity: 0.3,
			type: 'gradient',
			gradient: {
			  gradientToColors: ['#ffffff', '#ffffff']
			},
		  },
		  series: [{
			data: randomizeArray(sparklineData)
		  }],
		  labels: [...Array(24).keys()].map(n => `2018-09-0${n+1}`),
		  xaxis: {
			type: 'datetime',
		  },
		  yaxis: {
			min: 0
		  },
		  colors: ['#DCE6EC'],
			tooltip: {
				theme: 'dark'
			},
		};

		var spark3 = new ApexCharts(document.querySelector("#spark3"), spark3);
		spark3.render();

	
	
	
	
	
}); // End of use strict
