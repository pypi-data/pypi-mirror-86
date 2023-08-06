from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='stocker',
    packages=['stocker'],
    version='0.1.7',
    description='Stock Price Prediction',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='jcamiloangarita',
    author_email='camiloang94@gmail.com',
    url='https://github.com/jcamiloangarita/stocker',
    keywords='stock price prediction',
    classifiers=['Programming Language :: Python :: 3',
                 'Natural Language :: English',
                 'Topic :: Utilities'],
    install_requires=['numpy', 'pandas-datareader', 'pytrends', 'pandas', 'requests', 'scikit-learn', 'keras',
                      'tensorflow', 'matplotlib']
)
