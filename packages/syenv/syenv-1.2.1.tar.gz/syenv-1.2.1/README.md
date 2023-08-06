# Syenv

Syenv is a lightweight tool whose role is to load environment variables for configuration purposes.  
It has the advantage of offering some rather practical features to improve configuration management.  

## Table of content
- [Syenv](#syenv)
  - [Table of content](#table-of-content)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Usage](#usage)
    - [Basics](#basics)
    - [Advanced](#advanced)
      - [Custom configuration class](#custom-configuration-class)
      - [Using pattern selector](#using-pattern-selector)
  - [Variables syntax](#variables-syntax)
    - [Foreword](#foreword)
    - [Typing](#typing)
    - [Interpolation](#interpolation)

## Features

- Environment variables importer;
- Typing of environment variables;
- Supports interpolation;
- Prefix management to select a specific set of variables ;
- Pattern selector for retrieve some specifics variables.

## Requirements

- python >= 3.8

## Usage

### Basics

Syenv is really easy to use, as the following example shows.  
We consider the following environment file:

```bash
# .env
MY_APP_FTPS_PARAM_HOST=hostname
MY_APP_FTPS_PARAM_USER=username
MY_APP_FTPS_PARAM_PORT=int::22

MY_APP_STORAGE_DIR=pathlib.Path::storage
MY_APP_STUFF_STORAGE=pathlib.Path::{{MY_APP_STORAGE_DIR}}/stuffs
```

We can observe that the syntax of the values is a bit special. Syenv supports `variable typing` and `interpolation` (see [Variables syntax](#variables-syntax)).  
**Important:** Syenv has no environment variable file loader. It is not its role to do this type of processing. So you are free to use the tool of your choice, like `python-dotenv` for example.

```python
# __main__.py

import dotenv
import syenv

# In this example, we are using python-dotenv to load environment variables.
dotenv.load_dotenv()
env: syenv.Syenv = syenv.Syenv(prefix='MY_APP_')

# Now, we can access to our env vars!
print(env.FTPS_PARAM_HOST)
'''
>>> 'hostname' 
'''

print(env.STUFF_STORAGE)
''' 
>>> PosixPath('storage/stuffs') 
'''
```

We can notice that the prefix `MY_APP_` has been substitued.

### Advanced

#### Custom configuration class

We can use Syenv with a custom config class like the following example.

```python
# config/config.py

import syenv

class Config(syenv.Syenv):
    def __init__(self, prefix: str = 'MY_APP_') -> None:
        super().__init__(prefix)

        self.another_var: str = 'Hey!'

    @property
    def ftp_uri(self) -> str:
        return f'ftp://{self.FTPS_PARAM_HOST}:{self.FTPS_PARAM_PORT}'

```

We can also instanciate the Config class in the `__init__.py` file for facilities...

```python
# config/__init__.py

from config.config import Config

conf: Config = Config()
```

Then, considering the same env vars as above:

```python
# __main__.py

from config import conf

print(conf.as_dict)
'''
>>> {'FTPS_PARAM_HOST': 'hostname',
     'FTPS_PARAM_USER': 'username',
     'FTPS_PARAM_PORT': 22,
     'STORAGE_DIR': PosixPath('storage'),
     'STUFF_STORAGE': PosixPath('storage/stuffs'),
     'another_var': 'Hey!'}
'''

print(conf.ftp_uri)
''' 
>>> 'ftp://hostname:22'
'''
```

#### Using pattern selector

Consider using this env file :

```bash
# .env
MY_APP_FTP_PARAM_HOST=hostname
MY_APP_FTP_PARAM_USER=username
MY_APP_FTP_PARAM_PASSWORD=secret

MY_APP_STORAGE_DIR=pathlib.Path::storage
MY_APP_STUFF_STORAGE=pathlib.Path::{{MY_APP_STORAGE_DIR}}/stuffs
```

Lets using the python FTP lib for example :

```python
from ftplib import FTP
import dotenv
from syenv import Syenv

dotenv.load_dotenv()
env: Syenv = Syenv(prefix='MY_APP_')
ftp: FTP = FTP(**env.from_pattern('FTP_PARAM_', to_lower=True))

print(**env.from_pattern('FTP_PARAM_', to_lower=True))
'''
>>> {'host': 'hostname',
     'user': 'username',
     'password': 'secret'}
'''
```

**Note:** we can also keep the pattern string to the keys if we want.

## Variables syntax

### Foreword

Syenv reads system environment variables. The basic syntax is therefore the same.

    <ENV_KEY>=<ENV_VALUE>

For example:

    export APP_TEST_ENVVAR=some value

Will result of:

```python
import syenv

env: syenv.Syenv = syenv.Syenv('APP_TEST_')

print(env.ENVVAR)
'''
>>> 'some value'
'''
```

### Typing

We can specify the type of an environment variable in its value.

    <ENV_KEY>=[<TYPE>:]<VALUE>

**Note:** notice that the typing is optionnal. If no type are specified, the `str` object is used.

For example:

    export APP_TEST_TIMEOUT=int:30

Will result of:

```python
import syenv

env: syenv.Syenv = syenv.Syenv('APP_TEST_')

print(type(env.TIMEOUT), env.TIMEOUT)
'''
>>> <class 'int'> 30
'''
```

**Note:** As you can guess, the Syenv typing support all standards python objects as well as any external librairies which are installed into the project.  
The only important thing is to specify the correct package path during the writing of the value.

### Interpolation

Syenv also support interpolation for better configuration managing.  
The syntax is pretty generic:

    {{<ENV_KEY>}}

For example:

    export APP_TEST_ROOT_DIR=my_project
    export APP_TEST_STATIC_DIR={{APP_TEST_ROOT_DIR}}/statics

Will result of:

```python
import syenv

env: syenv.Syenv = syenv.Syenv('APP_TEST_')

print(env.ROOT_DIR)
'''
>>> 'my_project'
'''

print(env.STATIC_DIR)
'''
>>> 'my_project/statics'
'''
```

**Note:** We can also mixe the typing with interpolation. Just like the following example:

    export APP_TEST_ROOT_DIR=pathlib.Path:my_project
    export APP_TEST_STATIC_DIR=pathlib.Path:{{APP_TEST_ROOT_DIR}}/statics

Will result of:

```python
...

print(env.ROOT_DIR)
'''
>>> PosixPath('my_project')
'''

print(env.STATIC_DIR)
'''
>>> PosixPath('my_project/statics')
'''
```