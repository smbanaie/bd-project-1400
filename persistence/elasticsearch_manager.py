from kafka import KafkaConsumer
import json, requests


consumer = KafkaConsumer('persistence', auto_offset_reset='earliest', bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=1000, value_deserializer=lambda m: json.loads(m.decode('utf-8')))


header = {"content-type":"application/json"}
new_index = {
	"mappings": {
		"properties": {
			"message": {
				"type": "text",
				"fields" : {
					"keyword" : {
					"type" : "text",
					"analyzer": "parsi",
					"fielddata": "true"
					}
				}
			}
		}
	}
}


x = requests.head('http://localhost:9200/telegram')
if x.status_code != 200:
	requests.put('http://localhost:9200/telegram', data = json.dumps(new_index), headers=header)

while(True):
	for item in consumer:
		new_item = item.value
		x = requests.post('http://localhost:9200/telegram/_doc/{}'.format(new_item['UUID']), data = json.dumps(new_item), headers=header)