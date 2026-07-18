# Visual Preview

## Desktop App

```text
+-----------------------------------------+----------------------+
| Scenario map                            | Controls             |
|                                         |                      |
| Inbound zone        Shelf rows          | Start / Pause        |
| Cart A trail  ----> Packing Lane        | Reset / New Episode  |
| Sensor rays around robot                | Training toggle      |
|                                         | Steps/frame slider   |
| Status and arrival metrics              | Sensor rays slider   |
+-----------------------------------------+----------------------+
```

## Web App

```text
+-----------------------------+-----------------------------+
| Scenario Map                | Reward History              |
| Shelves, zones, trail, rays | Episode reward chart        |
+-----------------------------+-----------------------------+
| Episode | Step | Reward | Arrived | Exploration | States  |
+-----------------------------------------------------------+
```

Both views use the same `WarehouseEnv`, scenario JSON, and Q-learning baseline.
