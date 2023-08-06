==================
install-webdrivers
==================

Easy-to-use script to install the latest versions of chromedriver 
and geckodriver on Travis-CI.

Installation
------------
You can install this command directly from PyPI using pip as follows::
    
    $ pip install tchappui-webdrivers

User guide
----------

After having installed tchappui-webdrivers from PyPI,
simply install the last stable versions of chromedriver and 
geckdriver using the install-webdrivers command. Here is a sample
.travis.yml file as an example django project::

    dist: bionic
    language: python

    python:
      - '3.8'

    addons:
      # ajouter uniquement les navigateurs utilisés
      chrome: stable
      firefox: latest

    branches:
      only:
        - staging
    
    install:
      - pip install tchappui-webdrivers

    before_script:
      - install-webdrivers --path /usr/local/bin/

    env:
      global:
        # we suppose the settings for Travis are in a dedicated file
        - DJANGO_SETTINGS_MODULE="config.settings.travis"

    services:
      - postgresql

    script:
      - python manage.py test

Then, in your tests, start both chrome and firefox in headless mode:

.. code-block:: python

    from selenium import webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--window-size=1920x1080')


    firefox_options = webdriver.FirefoxOptions()
    firefox_options.headless = True
    firefox_options.add_argument('--window-size=1920x1080')

