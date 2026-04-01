from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="http://localhost:8086", token="raala-super-secret-token", org="raala")
query_api = client.query_api()

print("--- RAALA INFLUXDB DIAGNOSTIC ---")

try:
    q = '''
    from(bucket: "raala")
      |> range(start: 0)
      |> filter(fn: (r) => r["_measurement"] == "sensor_readings")
      |> filter(fn: (r) => r["sensor_id"] == "sensor_01")
      |> filter(fn: (r) => r["_field"] == "temperature")
      |> sort(columns: ["_time"])
      |> limit(n: 1)
    '''
    result = query_api.query(q)
    for table in result:
        for record in table.records:
            print("🕒 OLDEST RECORD in Bucket:", record.get_time())

    q_count = '''
    from(bucket: "raala")
      |> range(start: -24h)
      |> filter(fn: (r) => r["_measurement"] == "sensor_readings")
      |> filter(fn: (r) => r["sensor_id"] == "sensor_01")
      |> filter(fn: (r) => r["_field"] == "temperature")
      |> count()
    '''
    res_count = query_api.query(q_count)
    for table in res_count:
        for record in table.records:
            print("📊 TOTAL ROWS IN LAST 24H:", record.get_value())
            
except Exception as e:
    print("❌ ERROR:", e)
