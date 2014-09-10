#!/usr/bin/env python
# coding: utf-8

"""
Converts a native Python dictionary into an XML string. Supports int, float, str, unicode, list, dict and arbitrary nesting.
"""

from __future__ import unicode_literals

__version__ = '1.5.6'
version = __version__

from random import randint
import collections
import logging
import sys
from xml.dom.minidom import parseString

# python 3 doesn't have a unicode type
try:
    unicode
except:
    unicode = str

# python 3 doesn't have a long type
try:
    long
except:
    long = int

def set_debug(debug=True, filename='dicttoxml.log'):
    if debug:
        import datetime
        print('Debug mode is on. Events are logged at: %s' % (filename))
        logging.basicConfig(filename=filename, level=logging.INFO)
        logging.info('\nLogging session starts: %s' % (str(datetime.datetime.today())))
    else:
        logging.basicConfig(level=logging.WARNING)
        print('Debug mode is off.')

ids = [] # initialize list of unique ids

def make_id(element, start=100000, end=999999):
    """Returns a random integer"""
    return '%s_%s' % (element, randint(start, end))

def get_unique_id(element):
    """Returns a unique id for a given element"""
    this_id = make_id(element)
    dup = True
    while dup == True:
        if this_id not in ids:
            dup = False
            ids.append(this_id)
        else:
            this_id = make_id(element)
    return ids[-1]

def get_xml_type(val):
    """Returns the data type for the xml type attribute"""
    if type(val).__name__ in ('str', 'unicode'):
        return 'str'
    if type(val).__name__ in ('int', 'long'):
        return 'int'
    if type(val).__name__ == 'NoneType':
        return 'null'
    if isinstance(val, dict):
        return 'dict'
    if type(val).__name__ in ('list', 'set', 'tuple') or isinstance(val, collections.Iterable):
        return 'list'
    return type(val).__name__

def xml_escape(s):
    if type(s) in (str, unicode):
        s = s.replace('&', '&amp;')
        s = s.replace('"', '&quot;')
        s = s.replace('\'', '&apos;')
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
    return s

def make_attrstring(attr):
    """Returns an attribute string in the form key="val" """
    attrstring = ' '.join(['%s="%s"' % (k, v) for k, v in attr.items()])
    return '%s%s' % (' ' if attrstring != '' else '', attrstring)

def key_is_valid_xml(key):
    """Checks that a key is a valid XML name"""
    logging.info('Inside key_is_valid_xml(). Testing "%s"' % (key))
    test_xml = '<?xml version="1.0" encoding="UTF-8" ?><%s>foo</%s>' % (key, key)
    try: 
        parseString(test_xml)
        return True
    except Exception: #minidom does not implement exceptions well
        return False

def make_valid_xml_name(key, attr):
    """Tests an XML name and fixes it if invalid"""
    logging.info('Inside make_valid_xml_name(). Testing key "%s" with attr "%s"' % (key, str(attr)))
    # pass through if key is already valid
    if key_is_valid_xml(key):
        return key, attr
    # prepend a lowercase n if the key is numeric
    if key.isdigit():
        return 'n%s' % (key), attr
    # replace spaces with underscores if that fixes the problem
    if key_is_valid_xml(key.replace(' ', '_')):
        return key.replace(' ', '_'), attr
    # key is still invalid - move it into a name attribute
    attr['name'] = key
    key = 'key'
    return key, attr

def convert(obj, ids, attr_type, parent='root'):
    """Routes the elements of an object to the right function to convert them based on their data type"""
    logging.info('Inside convert(). obj type is: "%s", obj="%s"' % (type(obj).__name__, obj))
    if type(obj) in (int, float, long, str, unicode):
        return convert_kv('item', obj, attr_type)
    if hasattr(obj, 'isoformat'):
        return convert_kv('item', obj.isoformat(), attr_type)
    if type(obj) == bool:
        return convert_bool('item', obj, attr_type)
    if obj == None:
        return convert_none('item', '', attr_type)
    if isinstance(obj, dict):
        return convert_dict(obj, ids, parent, attr_type)
    if type(obj) in (list, set, tuple) or isinstance(obj, collections.Iterable):
        return convert_list(obj, ids, parent, attr_type)
    raise TypeError('Unsupported data type: %s (%s)' % (obj, type(obj).__name__))
    
def convert_dict(obj, ids, parent, attr_type):
    """Converts a dict into an XML string."""
    logging.info('Inside convert_dict(): obj type is: "%s", obj="%s"' % (type(obj).__name__, obj))
    output = []
    addline = output.append
    for key, val in obj.items():
        logging.info('Looping inside convert_dict(): key="%s", val="%s", type(val)="%s"' % (key, val, type(val).__name__))

        this_id = get_unique_id(parent)
        attr = {} if ids == False else {'id': '%s' % (this_id) }
        
        key, attr = make_valid_xml_name(key, attr)
       
        if type(val) in (int, float, long, str, unicode):
            addline(convert_kv(key, val, attr_type, attr))
            
        elif hasattr(val, 'isoformat'): # datetime
            addline(convert_kv(key, val.isoformat(), attr_type, attr))
            
        elif type(val) == bool:
            addline(convert_bool(key, val, attr_type, attr))
            
        elif isinstance(val, dict):
            if attr_type:
                attr['type'] = get_xml_type(val)
            addline('<%s%s>%s</%s>' % (
                key, make_attrstring(attr), convert_dict(val, ids, key, attr_type), key)
            )
        elif type(val) in (list, set, tuple) or isinstance(val, collections.Iterable):
            if attr_type:
                attr['type'] = get_xml_type(val)
            addline('<%s%s>%s</%s>' % (
                key, make_attrstring(attr), convert_list(val, ids, key, attr_type), key)
            )
        elif val is None:
            addline(convert_none(key, val, attr_type, attr))
        else:
            raise TypeError('Unsupported data type: %s (%s)' % (obj, type(obj).__name__))
    return ''.join(output)

def convert_list(items, ids, parent, attr_type):
    """Converts a list into an XML string."""
    logging.info('Inside convert_list()')
    output = []
    addline = output.append
    this_id = get_unique_id(parent)
    for i, item in enumerate(items):
        logging.info('Looping inside convert_list(): item="%s", type="%s"' % (item, type(item).__name__))
        attr = {} if ids == False else {
            'id': '%s_%s' % (this_id, i+1) 
        }
        if type(item) in (int, float, long, str, unicode):
            addline(convert_kv('item', item, attr_type, attr))
        elif hasattr(item, 'isoformat'): # datetime
            addline(convert_kv('item', item.isoformat(), attr_type, attr))
        elif type(item) == bool:
            addline(convert_bool('item', item, attr_type, attr))
        elif isinstance(item, dict):
            if not attr_type:
                addline('<item>%s</item>' % (convert_dict(item, ids, parent, attr_type)))
            else:
                addline('<item type="dict">%s</item>' % (convert_dict(item, ids, parent, attr_type)))
        elif type(item) in (list, set, tuple) or isinstance(item, collections.Iterable):
            if not attr_type:
                addline('<item %s>%s</item>' % (make_attrstring(attr), convert_list(item, ids, 'item', attr_type)))
            else:
                addline('<item type="list"%s>%s</item>' % (make_attrstring(attr), convert_list(item, ids, 'item', attr_type)))
        elif item == None:
            addline(convert_none('item', None, attr_type, attr))
        else:
            raise TypeError('Unsupported data type: %s (%s)' % (item, type(item).__name__))
    return ''.join(output)

def convert_kv(key, val, attr_type, attr={}):
    """Converts an int, float or string into an XML element"""
    logging.info('Inside convert_kv(): key="%s", val="%s", type(val) is: "%s"' % (key, val, type(val).__name__))
    
    key, attr = make_valid_xml_name(key, attr)
    
    if attr_type:
        attr['type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    return '<%s%s>%s</%s>' % (
        key, attrstring, xml_escape(val), key
    )

def convert_bool(key, val, attr_type, attr={}):
    """Converts a boolean into an XML element"""
    logging.info('Inside convert_bool(): key="%s", val="%s", type(val) is: "%s"' % (key, val, type(val).__name__))
    
    key, attr = make_valid_xml_name(key, attr)
    
    if attr_type:
        attr['type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    return '<%s%s>%s</%s>' % (key, attrstring, unicode(val).lower(), key)

def convert_none(key, val, attr_type, attr={}):
    """Converts a null value into an XML element"""
    logging.info('Inside convert_none(): key="%s"' % (key))
    
    key, attr = make_valid_xml_name(key, attr)
    
    if attr_type:
        attr['type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    return '<%s%s></%s>' % (key, attrstring, key)

def dicttoxml(obj, root=True, custom_root='root', ids=False, attr_type=True):
    """Converts a python object into XML
    attr_type is used to specify if data type for each element should be included in the resulting xml.
    By default, it is set to True.
    """
    logging.info('Inside dicttoxml(): type(obj) is: "%s", obj="%s"' % (type(obj).__name__, obj))
    output = []
    addline = output.append
    if root == True:
        addline('<?xml version="1.0" encoding="UTF-8" ?>')
        addline('<%s>%s</%s>' % (custom_root, convert(obj, ids, attr_type, parent=custom_root), custom_root))
    else:
        addline(convert(obj, ids, attr_type, parent=''))
    return ''.join(output).encode('utf-8')

