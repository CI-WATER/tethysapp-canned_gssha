// Globals
var INPUT_SERIES, MATCH_SERIES, SCENARIO_ID, MATCH_HYDROGRAPH;

// Update user interface
function update_ui() {
  var polar_plot, hydrograph_plot;

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
});