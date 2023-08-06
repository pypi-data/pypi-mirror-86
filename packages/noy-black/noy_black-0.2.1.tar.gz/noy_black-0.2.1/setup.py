from noy_black import VERSION
from setuptools import setup

# fmt: off
setup(
      name = 'noy_black'
    , version = VERSION
    , packages = ["noy_black"]
    , include_package_data=True

    , python_requires = ">= 3.6"

    , install_requires =
      [ 'black==20.8b1'
      , 'noseOfYeti>=2.0.0'
      ]

    , entry_points =
      { 'console_scripts' :
        [ 'noy_black = noy_black.main:main'
        ]
      }

    , author = 'Stephen Moore'
    , license = 'MIT'
    , author_email = 'delfick755@gmail.com'

    , url = "https://github.com/delfick/noy_black"
    , description = 'Monkey patched black that understands nose of yeti'
    , long_description = open("README.rst").read()
    )
# fmt: on
