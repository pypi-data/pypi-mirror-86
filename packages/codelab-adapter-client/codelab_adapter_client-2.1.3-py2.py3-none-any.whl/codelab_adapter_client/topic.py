'''
channel

将RPC和 [CQRS](https://en.wikipedia.org/wiki/Command%E2%80%93query_separation) 都放在pubsub里 (ROS)


[jupyter client messaging](https://jupyter-client.readthedocs.io/en/stable/messaging.html)
    *  Shell code execution req-rep
    *  Jupyter kernel Control channel
        *  shutdown/restart
    *  stdin: input from user
    *  IOPub
        *  stdout, stderr, debugging events
'''

# notification
# adapter data
# from to
ADAPTER_TOPIC = "adapter/nodes/data"  # 来自插件的消息，topic

# scratch command
SCRATCH_TOPIC = "scratch/extensions/command"
# JUPYTER_TOPIC = "from_jupyter/extensions"

# core
# EXTS_OPERATE_TOPIC由manage订阅，node自治
EXTS_OPERATE_TOPIC = "core/exts/operate" # 区分extensions和node(server)
NODES_OPERATE_TOPIC = "core/nodes/operate"
NODES_STATUS_TOPIC = "core/nodes/status"
ADAPTER_STATUS_TOPIC = "core/status" # adapter core info
NODES_STATUS_TRIGGER_TOPIC = "core/nodes/status/trigger"
NODE_STATU_CHANGE_TOPIC = "core/node/statu/change"
NOTIFICATION_TOPIC = "core/notification"
GUI_TOPIC = "gui/operate"

# ble
ADAPTER_BLE_TOPIC = "adapter/ble"
SCRATCH_BLE_TOPIC = "scratch/ble"

# mqtt gateway(from/to)
TO_MQTT_TOPIC = "to_mqtt"
FROM_MQTT_TOPIC = "from_mqtt"

# jupyter

# Home Assistant gateway(from/to)
FROM_HA_TOPIC = "from_HA"
TO_HA_TOPIC = "to_HA"

# websocket(socketio)
# Home Assistant
FROM_WEBSOCKET_TOPIC = "from_websocket"
TO_WEBSOCKET_TOPIC = "to_websocket"