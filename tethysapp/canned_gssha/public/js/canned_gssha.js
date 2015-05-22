// Globals
var INPUT_SERIES, MATCH_SERIES, SCENARIO_ID, MATCH_HYDROGRAPH;

// Add all layers to the map
var kml_layer25 = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: '/static/canned_gssha/kml/000-025.kml',
    format: new ol.format.KML()
  }),
  visible: false,
});

var kml_layer50 = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: '/static/canned_gssha/kml/025-050.kml',
    format: new ol.format.KML()
  }),
  visible: false,
});

var kml_layer75 = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: '/static/canned_gssha/kml/050-075.kml',
    format: new ol.format.KML()
  }),
  visible: false,
});

var kml_layer100 = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: '/static/canned_gssha/kml/075-100.kml',
    format: new ol.format.KML()
  }),
  visible: false,
});

var kml_layer200 = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: '/static/canned_gssha/kml/100-200.kml',
    format: new ol.format.KML()
  }),
  visible: false,
});

// Update user interface
function update_ui() {
  var polar_plot, hydrograph_plot, map_plot, maxFlow, temp, amp, rainDur, rainInt, rainStart, snowLine, snowGrad;

  // Get a handle on the chart
  polar_plot = $('#polar-plot').highcharts();

  // Update the INPUT_SERIES global
  INPUT_SERIES = [normalize_slider_value('#param1'),
                  normalize_slider_value('#param2'),
                  normalize_slider_value('#param3'),
                  normalize_slider_value('#param4'),
                  normalize_slider_value('#param5'),
                  normalize_slider_value('#param6'),
                  normalize_slider_value('#param7')]

  // Update input series on chart
  polar_plot.series[0].setData(INPUT_SERIES);

  // Update match series on chart
  if (MATCH_SERIES.length > 0) {
    // Create second series if it doesn't exist
    if (polar_plot.series.length < 2) {
        polar_plot.addSeries({
            name: 'Match',
            type: 'area',
            data: MATCH_SERIES,
            pointPlacement: 'on',
            color: '#2ecc71'
        });
    } else {
        polar_plot.series[1].setData(MATCH_SERIES);
    }
  }

  // Update hydrograph plot
  hydrograph_plot = $('#hydrograph-plot').highcharts();

  if (MATCH_HYDROGRAPH.length > 0) {
    // Create series if it doesn't exist
    if (hydrograph_plot.series.length < 1) {
      hydrograph_plot.addSeries({
        name: 'Hydrograph',
        color: '#3498db',
        data: MATCH_HYDROGRAPH
      });

    } else {
      hydrograph_plot.series[0].remove();
      hydrograph_plot.addSeries({
        name: 'Hydrograph',
        color: '#3498db',
        data: MATCH_HYDROGRAPH
      });
    }
  }

  // Find the max value of the hydrograph
  maxFlow = hydrograph_plot.series[0].dataMax;
  console.log(maxFlow);

  // Find the time to peak from max flow
  var xValue = null;
  var points = hydrograph_plot.series[0].points;
  
  for (var i = 0; i < points.length; i++) {
    if (points[i].y = maxFlow) break;
    xValue = points[i].x;
  }
  console.log(xValue);

  // Add flow number to text box
  $('#flow').text('Max Flow: ' + maxFlow.toFixed(2) + ' cms');

  // Remove all other layers that are visible
  kml_layer25.setVisible(false);
  kml_layer50.setVisible(false);
  kml_layer75.setVisible(false);
  kml_layer100.setVisible(false);
  kml_layer200.setVisible(false);

  // Add appropriate flood map to map based on max flow from hydrograph
  if (maxFlow > 0 && maxFlow < 25) {
    kml_layer25.setVisible(true);
  } else if (maxFlow > 25 && maxFlow < 50) {
      kml_layer50.setVisible(true);
  } else if (maxFlow > 50 && maxFlow < 75) {
      kml_layer75.setVisible(true);
  } else if (maxFlow > 75 && maxFlow < 100) {
      kml_layer100.setVisible(true);
  } else if (maxFlow > 100 && maxFlow < 200) {
      kml_layer200.setVisible(true);
  } else {
      null;
  };

  // Add text next to all sliders of what is selected
  temp = $('#param1').val();
  amp = $('#param2').val();
  rainDur = $('#param3').val(); 
  rainInt = $('#param4').val();
  rainStart = $('#param5').val();
  snowLine = $('#param6').val();
  snowGrad = $('#param7').val();

  $('#temp').text(temp);
  $('#amp').text(amp);
  $('#rainDuration').text(rainDur);
  $('#rainInt').text(rainInt);
  $('#rainStart').text(rainStart);
  $('#snowLine').text(snowLine);
  $('#snowGradient').text(snowGrad);
}

// Reset the UI
function reset_ui() {
  var chart, match_series;

  // Reset globals to defaults
  SCENARIO_ID = -999;
  MATCH_SERIES = [];
  MATCH_HYDROGRAPH = [];

  // Remove match series from plot
  chart = $('#polar-plot').highcharts();
  match_series = chart.series[1];

  if (typeof match_series !== 'undefined') {
    match_series.setData([0, 0, 0, 0, 0, 0, 0]);
    match_series.remove();
  }
}

// Find a match via the api
function find_match() {
  var form_data, url, request;

  form_data = $('#parameter-slider-form').serialize();

  url = '/apps/canned-gssha/api/match?' + form_data;

  request = $.ajax({
    type: "GET",
    url: url
  });

  request.done(function(data) {
    if (data['success']) {
      // Update Globals
      SCENARIO_ID = data['data']['scenario_id'];
      MATCH_SERIES = data['data']['parameters'];
      MATCH_HYDROGRAPH = data['data']['hydrograph'];

      // Update the UI
      update_ui();
    }
  });
}

// Normalize the value of the slider
function normalize_slider_value(slider_selector) {
  var x, z, min, max, $slider;

  // Get handle on slider
  $slider = $(slider_selector);

  // Get values from slider
  x = Number($slider.val());
  min = Number($slider.attr('min'));
  max = Number($slider.attr('max'));

  // Calculate normalized value
  z = (x - min) / (max-min);

  return z;

}

function addLayers() {
  // Get handle on map
  map_plot = TETHYS_MAP_VIEW.getMap();

  // Add all 5 layers to map
  map_plot.addLayer(kml_layer25);
  map_plot.addLayer(kml_layer50);
  map_plot.addLayer(kml_layer75);
  map_plot.addLayer(kml_layer100);
  map_plot.addLayer(kml_layer200);
}


// On page load...
$(document).ready(function() {
  // Initialize globals
  SCENARIO_ID = -999;
  MATCH_SERIES = [];
  MATCH_HYDROGRAPH = [];

  // Bind events
  $("input[type='range']").on('input', function() {
      // Reset the UI
      reset_ui();

      // Update the UI
      update_ui();
  });

  $("input[type='range']").on('change', function() {
      // Find the match
      find_match();
  });

  // Add all layers initially to the map
  addLayers();
});