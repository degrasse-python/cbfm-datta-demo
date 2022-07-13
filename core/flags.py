# Import Cloudbees SDK
from rox.server.rox_server import Rox 
from rox.server.rox_options import RoxOptions
from rox.server.flags.rox_flag import RoxFlag
from rox.core.entities.rox_string import RoxString
from rox.core.entities.rox_int import RoxInt
from rox.core.entities.rox_double import RoxDouble

ROLLOUT_ENV_KEY ="613fa182a5e4a9413e8c0b65"

# example of a naive Logger
class MyLogger:
  def error(self, msg, ex=None):
      print('error: %s exception: %s' %(msg, ex))

  def warn(self, msg, ex=None):
      print('warn: %s' % msg)

  def debug(self, msg, ex=None):
      print('debug: %s' % msg)

# Create Roxflags in the Flags container class
class Flags:
  def __init__(self):
    """Cloudbees Feature Flag Management intial values"""
    ### --- Define the feature flags --- ###
    # KPI
    self.enableCustomersKPI = RoxFlag(False)
    # Login Screen
    self.enableSocialSignOn = RoxFlag(False)
    # list of all dashboard options - here we give the engn team the option to revert
    self.LineGraphVariant = RoxString('is-newversion', ['is-revert', 'is-newversion'])
    self.enableRevenueKPI =  RoxFlag(False)
    self.enableLineGraph =  RoxFlag(False)
    self.enableNewTaskButton =  RoxFlag(False)

    # User attr
    Rox.set_custom_boolean_property('isBeta', False)
    Rox.set_custom_boolean_property('isAdmin', False)
    
    # Options

    # setup configuration_fetched_handler in the options object
    self.options = RoxOptions(
        version="1.0.4",
        fetch_interval=30,
        logger=MyLogger(),
        configuration_fetched_handler=lambda o: 
          print("applied-from=%s creation-date=%s has-changes=%s error=%s" % 
                (o.fetcher_status , o.creation_date , o.has_changes , o.error_details)),
          
        # configuration_fetched_handler=lambda o: print("applied-from=%s creation-date=%s has-changes=%s error=%s" % (o.fetcher_status , o.creation_date , o.has_changes , o.error_details)),

        #lambda sender: sender=="APPLIED_FROM_NETWORK" # TODO: add things to do when configuration was fetched
        # When a property does not exist on the client side what do you do?
        # dynamic_property_rule_handler=lambda property, context: # TODO: return dynamic rule for properties
      )
    