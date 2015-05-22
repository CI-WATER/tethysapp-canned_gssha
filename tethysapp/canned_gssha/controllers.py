from django.shortcuts import render
from django.http import JsonResponse

from tethys_gizmos.templatetags.tethys_gizmos import HighchartsDateEncoder
from tethys_gizmos.gizmo_options import MapViewLegendClass, MapViewLayer, MapViewOptions, MapViewDrawOptions, MapViewViewOptions

from model import CannedScenario, CannedResult


def home(request):
    """
    Controller for the app home page.
    """
    # Configure Sliders
    slider1_options = {'display_text': 'Temperature [' + unichr(176) + 'F]',
                       'name': 'param1',
                       'min': 20,
                       'max': 100,
                       'initial': 60,
                       'step': 0.5}

    slider2_options = {'display_text': 'Temperature Amplitude [' + unichr(176) + 'F]',
                       'name': 'param2',
                       'min': 5,
                       'max': 20,
                       'initial': 12.5,
                       'step': 0.5}

    slider3_options = {'display_text': 'Rain Duration [hours]',
                       'name': 'param3',
                       'min': 1,
                       'max': 10,
                       'initial': 5.5,
                       'step': 0.25}

    slider4_options = {'display_text': 'Rain Intensity [mm]',
                       'name': 'param4',
                       'min': 10,
                       'max': 100,
                       'initial': 55,
                       'step': 1.0}

    slider5_options = {'display_text': 'Rain Start [hour]',
                       'name': 'param5',
                       'min': 0,
                       'max': 24,
                       'initial': 12,
                       'step': 0.25}

    slider6_options = {'display_text': 'Snow Line [m]',
                       'name': 'param6',
                       'min': -100,
                       'max': 400,
                       'initial': 150,
                       'step': 1.0}

    slider7_options = {'display_text': 'Snow Gradient [m/m]',
                       'name': 'param7',
                       'min': 0,
                       'max': 0.002,
                       'initial': 0.001,
                       'step': 0.00001}

    # Configure plot
    polar_plot_object = {
        'chart': {
            'polar': True,
            'type': 'line'
        },
        'title': {
            'text': '',
        },
        'subtitle': {
            'text': 'Note: Values shown in plot are normalized for easy comparison.',
            'style': {
                'margin-bottom': '10px'
            }
        },
        'legend': {
            'verticalAlign': 'middle',
            'align': 'left',
            'layout': 'vertical'
        },
        'pane': {
            'size': '80%'
        },
        'xAxis': {
            'categories': ['Temperature', 'Temperature Amplitude', 'Rain Duration',
                           'Rain Intensity', 'Rain Start', 'Snow Line', 'Snow Gradient'],
            'tickmarkPlacement': 'on',
            'lineWidth': 0
        },
        'yAxis': {
            'gridLineInterpolation': 'polygon',
            'lineWidth': 0,
            'min': 0,
            'max': 1.00,
            'tickInterval': 0.25

        },
        'tooltip': {
            'valueDecimals': 2,
        },
        'series': [{'name': 'Input',
                    'type': 'area',
                    'data': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                    'pointPlacement': 'on',
                    'color': '#f1c40f'
                   }]
    }

    polar_plot = {'highcharts_object': polar_plot_object,
                  'width': '100%',
                  'height': '320px',
                  'attributes': 'id=polar-plot'}

    # Results plot
    highcharts_object = {
        'chart': {
            'type': 'areaspline',
            'zoomType': 'x'
        },
        'title': {
            'text': ''
        },
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle',
            'borderWidth': 0,
            'enabled': False
        },
        'xAxis': {
            'title': {
                'enabled': True,
                'text': 'Time',
                'offset': 35
            },
            'type': 'datetime',
            'minRange': 3 * 3600000,  # three hours
            'tickLength': 10,
            'labels': {
                'y': 25
            }
        },
        'yAxis': {
            'title': {
                'enabled': True,
                'text': 'Flowrate [cms]'
            },
            'max': 100.0
        },
        'tooltip': {
            'pointFormat': '{point.y} cms',
            'valueDecimals': 2,
            'xDateFormat': '%d %b %Y %H:%M'
        },
        'series': [{
                       'name': 'Hydrograph',
                       'color': '#3498db',
                       'data': []}
        ]}

    line_plot_view = {'highcharts_object': highcharts_object,
                      'width': '100%',
                      'height': '320px',
                      'attributes': 'id=hydrograph-plot'}

    # Define view options for the map
    view_options = MapViewViewOptions(
      projection='EPSG:4326',
      center=[-111.47, 40.2],
      zoom=11,
      maxZoom=18,
      minZoom=2
    )

    # Define KML layers
    base_kml_layer = MapViewLayer(source='KML',
      options={'url': '/static/canned_gssha/kml/onload.kml'},
      legend_title='Initial KML Layer',
      legend_extent=[-111.64, 40.08, -111.28, 40.29],
      legend_classes=[
         MapViewLegendClass('polygon', 'Watershed Boundary', fill='#ff8000'),
         MapViewLegendClass('line', 'Stream Network', stroke='#0000ff'),
    ])   

    # Define map view options
    map_view_options = MapViewOptions(
      height='600px',
      width='100%',
      controls=['ZoomSlider', 'Rotate', 'FullScreen',
                {'MousePosition': {'projection': 'EPSG:4326'}},],
      layers=[base_kml_layer],
      view=view_options,
      basemap={'MapQuest': {'layer': 'osm'}},
      legend=True
    )

    context = {'slider1_options': slider1_options,
               'slider2_options': slider2_options,
               'slider3_options': slider3_options,
               'slider4_options': slider4_options,
               'slider5_options': slider5_options,
               'slider6_options': slider6_options,
               'slider7_options': slider7_options,
               'polar_plot': polar_plot,
               'line_plot_view': line_plot_view,
               'map_view_options': map_view_options}

    return render(request, 'canned_gssha/home.html', context)


def match(request):
    """
    Execute the match algorithm. Returns JSON object.
    """
    # Default Result
    params = None
    result = {'success': False}

    # Get the request parameters
    if request.method == 'GET':
        params = request.GET
    elif request.method == 'POST':
        params = request.POST

    if params and 'param1' in params:
        try:
            # Assemble param list
            param_list = (float(params['param1']),
                          float(params['param2']),
                          float(params['param3']),
                          float(params['param4']),
                          float(params['param5']),
                          float(params['param6']),
                          float(params['param7']))


            result['data'] = CannedScenario.match(param_list, False, True)
            result['data']['hydrograph'] = CannedResult.get_hydrograph_by_id(result['data']['scenario_id'])
            result['success'] = True
        except:
            raise
            pass

    return JsonResponse(data=result, encoder=HighchartsDateEncoder)