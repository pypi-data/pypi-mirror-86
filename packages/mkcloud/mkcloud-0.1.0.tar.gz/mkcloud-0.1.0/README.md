# 童心制物云服务 mkcloud

## 目前提供的功能

### 聊天机器人

    `发消息 mkcloud.robot.chat('哈哈哈哈')`
    `切换中英文服务 mkcloud.robot.setLanguage('en')`

### MqTT功能

- 导入方式：
  
    `from mkcloud.mqtt import mqtt`

- 设置参数

  `mqtt.set_broker('mb1234','broker.emqx.io',1883)`

- MQTT连接

    `mqtt.connect()`

- 信息发送

    `mqtt.publish_message("topic", "messages")`

- 信息接收

    `def callback(topic, data): print("CallBack -Received", data, "topic:", topic)`
    `mqtt.set_callback(callback)`
    `mqtt.subscribe_message("topic1")`
    `mqtt.subscribe_message("topic2")`
