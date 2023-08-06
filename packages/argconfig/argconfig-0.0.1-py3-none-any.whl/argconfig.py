import argparse
import yaml

__author__ = "Patrick C O\'Driscoll"
__copyright__ = "2020"
__credits__ = ["Patrick C O\'Driscoll"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Patrick C O\'Driscoll"
__email__ = "patrick.c.odriscoll@gmail.com"


class ArgumentParser(argparse.ArgumentParser):
  """ Argconfig:
      Improvement on the argparse.ArgumentParser class. It adds the functionality of a
      configuration file. The order of load importance is as follows:
        command line > config file > code set default
      Added command line option of:
        config=None, points to a yaml formated config file.
  """
  def __init__(self, config=None, *args, **kargs,):
    ''' Initialization of the class '''
    super().__init__(*args,**kargs)
    if config is not None:
      self.config = config
      try:
        with open(config,'r') as f:
          self.parms = yaml.safe_load(f)
      except:
        pass
    return
  
  def add_argument(self, *args, **kargs):
    ''' Add argument
        Same as argparse.ArgumentParser with the addded functionality of:
            Command line > config file > code set default
    '''
    try:
      kargs['default'] = self.getConfig(args,kargs['default'])
    except:
      try:
          kargs['default'] = self.getConfig(args,None)
      except:
        pass
      pass
    super().add_argument(*args,**kargs)
    return

  def getConfig(self,arg,value):
    ''' Get configuration from config
        Override the code based default based upon the settings in the config file. 
    '''
    for ii in arg:
      try:
        return self.parms[ii.lstrip('-')]
      except:
        pass
    return value


if __name__ == "__main__":
  """ Example of loader:
    command line arugments > config file > code set defailt
    command line argument:
      foo : depends on user
      bar : depends on user setting
    example.yaml set to:
      foo : test1
      bar : 2.0
    default :
      foo : testing
      bar : implicit None
  """
  parser = ArgumentParser(description='argparse + yaml config file example',config='./example.yaml')
  parser.add_argument('-f','--foo', type=str, default='testing',help='foo (default=testing, config=test)')
  parser.add_argument('--bar',                                  help='bar (default=None, config = 2.0)')
  args = parser.parse_args()

  print('foo:',args.foo)
  print('bar:',args.bar)
