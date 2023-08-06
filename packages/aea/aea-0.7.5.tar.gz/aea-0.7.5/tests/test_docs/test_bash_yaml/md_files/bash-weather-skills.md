``` bash
aea fetch fetchai/weather_station:0.18.0 --alias my_weather_station
cd my_weather_station
aea install
```
``` bash
aea create my_weather_station
cd my_weather_station
aea add connection fetchai/p2p_libp2p:0.12.0
aea add connection fetchai/soef:0.13.0
aea add connection fetchai/ledger:0.10.0
aea add skill fetchai/weather_station:0.16.0
aea install
aea config set agent.default_connection fetchai/p2p_libp2p:0.12.0
```
``` bash
aea fetch fetchai/weather_client:0.19.0 --alias my_weather_client
cd my_weather_client
aea install
```
``` bash
aea create my_weather_client
cd my_weather_client
aea add connection fetchai/p2p_libp2p:0.12.0
aea add connection fetchai/soef:0.13.0
aea add connection fetchai/ledger:0.10.0
aea add skill fetchai/weather_client:0.16.0
aea install
aea config set agent.default_connection fetchai/p2p_libp2p:0.12.0
```
``` bash
aea generate-key fetchai
aea add-key fetchai fetchai_private_key.txt
aea add-key fetchai fetchai_private_key.txt --connection
```
``` bash
aea generate-key fetchai
aea add-key fetchai fetchai_private_key.txt
aea add-key fetchai fetchai_private_key.txt --connection
```
``` bash
aea generate-wealth fetchai
```
``` bash
aea run
```
``` bash
aea run
```
``` bash
cd ..
aea delete my_weather_station
aea delete my_weather_client
```
``` yaml
default_routing:
  fetchai/ledger_api:0.7.0: fetchai/ledger:0.10.0
  fetchai/oef_search:0.10.0: fetchai/soef:0.13.0
```
``` yaml
default_routing:
  fetchai/ledger_api:0.7.0: fetchai/ledger:0.10.0
  fetchai/oef_search:0.10.0: fetchai/soef:0.13.0
```
``` yaml
config:
  delegate_uri: 127.0.0.1:11001
  entry_peers: ['SOME_ADDRESS']
  local_uri: 127.0.0.1:9001
  log_file: libp2p_node.log
  public_uri: 127.0.0.1:9001
```