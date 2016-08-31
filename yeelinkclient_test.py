from yeelinkclient import *

YEELINK_API_KEY = 'ededf5081c163590b275398b49ec1f62'
YEELINK_DEVICE_ID = "350526"
YEELINK_SENSOR_ID_HUMIDITY = "393399"
YEELINK_SENSOR_ID_TEMPERATOR= "393400"


def yeelink_send(hum_value, temp_value):
	client = YeelinkClient(apikey=YEELINK_API_KEY)
	hum_op = DataOperation(conn=client, deviceid=YEELINK_DEVICE_ID, sensorid=YEELINK_SENSOR_ID_HUMIDITY)
	hum_op.send_data_value(hum_value)
	temp_op = DataOperation(conn=client, deviceid=YEELINK_DEVICE_ID, sensorid=YEELINK_SENSOR_ID_TEMPERATOR)
	temp_op.send_data_value(temp_value)


def yeelink_send_onestep(hum_value, temp_value):
	client = YeelinkClient(apikey=YEELINK_API_KEY)
	md_op = MutipleDataOperation(conn=client, deviceid=YEELINK_DEVICE_ID)
	raw_data_hum = {'sensor_id': YEELINK_SENSOR_ID_HUMIDITY, 'value': hum_value}
	raw_data_temp = {'sensor_id': YEELINK_SENSOR_ID_TEMPERATOR, 'value': temp_value}
	md_op.send_data([raw_data_hum, raw_data_temp])

def yeelink_read():
	client = YeelinkClient(apikey=YEELINK_API_KEY)
	hum_op = DataOperation(conn=client, deviceid=YEELINK_DEVICE_ID, sensorid=YEELINK_SENSOR_ID_HUMIDITY)
	hum_op.get_data_value()
	temp_op = DataOperation(conn=client, deviceid=YEELINK_DEVICE_ID, sensorid=YEELINK_SENSOR_ID_TEMPERATOR)
	temp_op.get_data_value()


yeelink_send(40, 29)
yeelink_read()

yeelink_send_onestep(40.02, 29.02)
yeelink_read()