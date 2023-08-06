from setuptools import setup

setup(
    name = 'clear_screen_CLS',
    version = '1.0.1',
    author = 'Samuel Batista',
    description = "Clear Screen for all OS's",
    long_description = "Whenever you need to run a 'cls', a screen cleaning, just import this script and run it and that's it!"
    + "Simple but very useful in all types of scripts. How to use: import cls;cls.cls()",
    author_email = 'samuelbatistaprime@hotmail.com',
    packages = ['cls'],
    url = 'https://github.com/don-batista/CLear_Screen',
    project_urls = {
        'Source Code': 'https://github.com/don-batista/CLear_Screen',
        'Download': 'https://github.com/don-batista/CLear_Screen/blob/main/archive/1.0.1.zip'
    },
    license = 'MIT',
    keywords = {
        'Clear screen',
        'CLS',
        'Clear terminal screen',
        'Clear screen python'
        
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ]
)



