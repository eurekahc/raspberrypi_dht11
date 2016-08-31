#!/usr/bin/python
import time
import requests
import json

BASE_URL = 'http://api.yeelink.net/v1.1/'
DEFAULT_VERSION = 'v1.1'

class Device(object):
	def __init__(type, title, about, tags, unit_name, unit_symbol):
		self._type = type #value, switcher, gps, gen, photo
		self._title = title
		self._about = about
		self._tags = tags
		self._unit_name = unit_name
		self._unit_symbol = unit_symbol


class YeelinkError(Exception):
    pass


class YeelinkHTTPError(YeelinkError):
    pass


class YeelinkForbiddenError(YeelinkHTTPError):
    pass


class YeelinkInvalidInputError(YeelinkError):
    pass


def create_exception_object(response):
    code = response.status_code
    if code == 500:
        return YeelinkHTTPError("An Internal Server Error Occurred.\n")
    elif code == 400:
        return YeelinkHTTPError("Your response is invalid.\n")
    elif code == 404:
        return YeelinkHTTPError("Resource responseed not found.\n")
    elif code in [403, 401]:
        return YeelinkForbiddenError("You don't have permissions to access this resource.\n")
    else:
        return YeelinkHTTPError("Not Handled Exception.\n")


def raise_informative_exception(list_of_error_codes):
    def real_decorator(fn):
        def wrapped_f(self, *args, **kwargs):
            response = fn(self, *args, **kwargs)
            if response.status_code in list_of_error_codes:
                error = create_exception_object(response)
                raise error
            else:
                return response
        return wrapped_f
    return real_decorator


def validate_multidata_input():
    def real_decorator(fn):
        def wrapped_f(self, *args, **kwargs):
            if not isinstance(args[0], list):
                raise YeelinkInvalidInputError("Invalid argument type. [list]")

            required_keys = ['sensor_id', 'value']
            def check_keys(obj):
                for key in required_keys:
                    if key not in obj:
                        raise YeelinkInvalidInputError('Key "%s" is missing' % key)

            def check_list_item(obj):
            	if not isinstance(obj, dict):
            		raise YeelinkInvalidInputError("Invalid argument type. [dict]")
            	check_keys(obj)
            
            map(check_list_item, args[0])

            return fn(self, *args, **kwargs)
        return wrapped_f
    return real_decorator


class RemoteConnection(object):
    def __init__(self, apikey=None, base_url=None):
        self.base_url = base_url or BASE_URL
        self._apikey = apikey
        self._apikey_header = {'U-ApiKey': self._apikey}

    def _get_custom_headers(self):
        headers = {'content-type': 'application/json'}
        return headers

    def _prepare_headers(self):
	    headers = {}
	    headers.update(self._apikey_header)
	    headers.update(self._get_custom_headers())
	    return headers    

    def _prepare_data(self, data):
        return json.dumps(data)

    @raise_informative_exception([400, 401, 403, 404, 500])
    def get(self, path, **kwargs):
        headers = self._prepare_headers()
        response = requests.get(self.base_url + path, headers=headers, **kwargs)
        return response

    @raise_informative_exception([400, 401, 403, 404, 500])
    def post(self, path, raw_data, **kwargs):
        headers = self._prepare_headers()
        data = self._prepare_data(raw_data)
        url = self.base_url + path
        response = requests.post(url, data=data, headers=headers, **kwargs)
        return response


class YeelinkObjcetOperation(object):
	def __init__(self, apikey=None, conn=None):
		if conn is None:
			self._remote_connection = RemoteConnection(apikey)
		else:
			self._remote_connection = conn


class DeviceOperation(YeelinkObjcetOperation):
	def __init__(self, apikey=None, conn=None,deviceid=None):
		self._device_id = deviceid
		super(DeviceOperation, self).__init__(apikey, conn)

	def create_device(self):
		pass

	def edit_device(self):
		pass

	def get_devices(self):
		pass

	def get_device(self):
		pass

	def delete_device(self):
		pass


class SensorOperation(YeelinkObjcetOperation):
	def __init__(self, apikey=None, conn=None,vdeviceid=None, sensorid=None):
		self._device_id = deviceid
		self._sensor_id = sensorid
		super(SensorOperation, self).__init__(apikey, conn)

	def create_sensor(self):
		pass

	def edit_sensor(self):
		pass

	def get_sensors(self):
		pass

	def get_sensor(self):
		pass

	def delet_sensor(self):
		pass


def show_result(result):
	print result.status_code
	print result.text


class DataOperation(YeelinkObjcetOperation):
	def __init__(self, apikey=None, conn=None, deviceid=None, sensorid=None):
		super(DataOperation, self).__init__(apikey, conn)
		self._base_path = 'device/' + deviceid
		self._base_path += '/sensor/' + sensorid		

	def send_data_value(self, data_value):
		path = self._base_path
		path += '/datapoints'
		post_data = {'value': data_value}  
		result = self._remote_connection.post(path, post_data)
		#show_result(result)

	def send_data_value_with_time(self, data_value, data_timestamp=None):
		path = self._base_path
		path += '/datapoints'
		if data_timestamp is None:
			data_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
		post_data = {'value': data_value} 
		post_data.update({'timestamp': data_timestamp})
		self._remote_connection.post(path, post_data)

	def send_data_values(self, data_values):
		path = self.__base_path
		path += '/datapoints'
		self._remote_connection.post(path, data_values)

	def send_data_gps(self):
		pass

	def send_data_gen(self):
		pass

	def edit_data_value(self):
		pass

	def get_data_value(self, key=None):
		path = self._base_path
		path += '/datapoint'
		result = self._remote_connection.get(path)
		#show_result(result)


class MutipleDataOperation(YeelinkObjcetOperation):
	def __init__(self, apikey=None, conn=None, deviceid=None):
		super(MutipleDataOperation, self).__init__(apikey, conn)
		self._device_id = deviceid		
		self._path = 'device/' + self._device_id
		self._path += '/datapoints'
	
	@validate_multidata_input()
	def send_data(self, raw_data):
		result = self._remote_connection.post(self._path, raw_data)
		#show_result(result)


class YeelinkClient(RemoteConnection):
	pass