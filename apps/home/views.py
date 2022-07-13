# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from rox.server.rox_server import Rox
from core.flags import Flags, ROLLOUT_ENV_KEY

# Load flags
flags = Flags()
# Setup Feature Management SDK
try:
  flag_dict = {}
  # Register the flags container
  Rox.register('dashboard', flags)
  print("Feature Management Flags Registered")
  # Setup the environment key
  cancel_event = Rox.setup(ROLLOUT_ENV_KEY, flags.options) #.result()
  print("Feature Management Setup - Starting Server")
  print("enableLineGraph: %s" % (flags.enableRevenueKPI.is_enabled()))
  print("enableRevenueKPI: %s" % (flags.LineGraphVariant.get_value()))
except Exception as e:
  print('%s (%s)' % (e, type(e)))


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    try:
      Rox.fetch()
      print('fetched')
    except Exception as e:
      print('%s (%s)' % (e, type(e)))
  
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        ### --- Feature FLAGS --- ###
        # add ff inside context dict to pass them to the templates on frontend
        context['enableCustomersKPI'] = flags.enableCustomersKPI.get_value()
        context['LineGraphVariant'] = flags.LineGraphVariant.get_value()
        context['enableLineGraph'] = flags.enableLineGraph.is_enabled()
        context['enableRevenueKPI'] = flags.enableRevenueKPI.is_enabled()
        # context['enableNewTaskButton'] = flags.enableNewTaskButton.get_value()     

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
