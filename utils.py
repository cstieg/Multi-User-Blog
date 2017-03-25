"""
originally written by 'dmw'
(http://stackoverflow.com/questions/1531501/json-serialization-of-google-app-engine-models)
slight modifications made
"""

import datetime
from google.appengine.ext import db



SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
    """Converts a datastore entity into a Python dict"""
    output = {}

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to MILLISECONDS-since-epoch (JS "new Date()").
            #ms = time.mktime(value.utctimetuple()) * 1000
            #ms += getattr(value, 'microseconds', 0) / 1000
            #output[key] = int(ms)
            output[key] = value.strftime('%c')
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output
