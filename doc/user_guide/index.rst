User Guide
==========



This module provides functionalities to help investigate the Udwi Database.
Once the relevant sources has been selected, you need to use the :py:mod:`udwi_data_connector.power_connector`
classes to access the time series data.


From one user to the data
-------------------------

The relations between a user to the data is presented by the following image.

.. image:: /_static/simplified_relation_user_to_sources.png
  :width: 600
  :alt: simplified_relation_user_to_sources

The main ideas to remember is that :

* one user can have multiple sites (each site has a "owner_id" which is the "user_id")
* one site can have multiple sources (each site has a "site_id")
* one sources can have multiple "data_type", for instance a Comfort sensor has a Temperature and humidity data_type
* one source can have zero or one sensor, for instance an API as no sensor

The function :py:func:`.all_sources` returns a DataFrame with every information in relation:

* One row correspond to one source and one data_type (so one comfort source returns two row)
* every row includes the information of the sensor, the source, the site and the user.

Suppressed user and site information
------------------------------------

When a user end his subscription, the personal information are removed from the database :

* email is changed to `fake@ecoco2.com`
* the site address and lng lat are set to None
* the program information is removed.

However, the user_id and site_id is kept, along with the sources and the data of this site.
