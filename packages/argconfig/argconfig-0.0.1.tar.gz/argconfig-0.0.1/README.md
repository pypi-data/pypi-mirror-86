# argconfig
argparse + yaml config system

This takes the same format as the argparse.ArgumentParser class; however
it adds the feature of setting a default yaml file for base configuration
to override the default set in the code. Usage has the following overwrite
priority:

command line > config file > default set in code

This enables a flexible configuration based, commandline interface options
at scale.

## Requirements
* Python 3.7+
* pyyaml
* argparse

## Example
### Config File
Use the example.yaml config file in the same directory as your example python code:
```
$ cat example.yaml
foo : test1
bar : 2.0
```
### Example Code
The example python code setsup the variables foo and bar to equal 'testing' and 2.0 respectively. 
(Note the syntax is almost identical as argparse.ArgumentParser.)
```
import argconfig

parser = argconfig.ArgumentParser(description='argconfig example',config='./example.yaml')
parser.add_argument('-f','--foo', type=str, default='testing',
                    help='foo (default=testing, config=test)')
parser.add_argument('--bar',
                    help='bar (default=None, config = 2.0)')
args = parser.parse_args()

print('foo:',args.foo)
print('bar:',args.bar)
```
### Example Command Line Usage
Run time of the example with foo and bar set by command line:
```
python example.py --foo test --bar 3.0
```
returns the following two print statements:
```
foo: test
bar: 3.0
```

While the values set in example.yaml is used when the values are not overriden by the command line:
```
python example.py
```
returns the following two print statements:
```
foo: test1
bar: 2.0
```
