from setuptools import setup, find_packages

setup(
    name='XClass-Project',
    version='1.0.0',
    url='https://github.com/iankuys/Xclass-Project',
    packages=find_packages(),    
    install_requires=[
        'flask',
        'opencv-python',
        'mediapipe',
        'RPi.GPIO',
        'python-crontab',
    ],
)