# Customer movement simulator 0.1.0 documentation

This service is responsible for simulating customer movement around retail store.
## Table of Contents

* [Servers](#servers)
* [Channels](#channels)

## Servers

### **development** Server

| URL | Protocol | Description |
|---|---|---|
| localhost | mqtt | Development mosquitto broker |

## Channels

### **customer/enter** Channel

#### `publish` Operation

##### Message

###### Payload

| Name | Type | Description | Accepted values |
|---|---|---|---|
| id | string | ID of the customer | _Any_ |
| ts | integer | Timestamp (unix time) | _Any_ |

> Examples of payload _(generated)_

```json
{
  "id": "string",
  "ts": 0
}
```




### **customer/exit** Channel

#### `publish` Operation

##### Message

###### Payload

| Name | Type | Description | Accepted values |
|---|---|---|---|
| id | string | ID of the customer | _Any_ |
| ts | integer | Timestamp (unix time) | _Any_ |

> Examples of payload _(generated)_

```json
{
  "id": "string",
  "ts": 0
}
```




### **customer/move** Channel

#### `publish` Operation

##### Message

###### Payload

| Name | Type | Description | Accepted values |
|---|---|---|---|
| id | string | ID of the customer | _Any_ |
| ts | integer | Timestamp (unix time) | _Any_ |
| x | integer | coordinate x | _Any_ |
| y | integer | coordinate y | _Any_ |

> Examples of payload _(generated)_

```json
{
  "id": "string",
  "ts": 0,
  "x": 0,
  "y": 0
}
```




