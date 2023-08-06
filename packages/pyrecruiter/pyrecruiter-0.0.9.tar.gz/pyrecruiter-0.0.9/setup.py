from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Information Technology',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyrecruiter',
  version='0.0.9',
  description='This is a Light weight Open source Python Package made specially for Job Seekers and Recruiters in the field of Data science and Machine Learning (Currently), In order to use the Power of Machine Learning to help Shortlist the Right Candidates for a specific Job.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type = "text/markdown",
  url='https://github.com/msp04/PyRecruiter',  
  author='Mohit Singh Pawar',
  author_email='mohitsinghpawar4@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['job','recruit','recruiters','shortlister','pyrecruit','pyrecruiter','PyRecruiter'],
  packages=find_packages(),
  install_requires=['pathlib == 1.0.1','scikit-learn == 0.23.2','openpyexcel == 2.5.14','pandas >= 0.20.0'] 
)