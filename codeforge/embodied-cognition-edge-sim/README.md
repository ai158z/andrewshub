# Embodied Cognition Edge Simulation (embodied-cognition-edge-sim)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A distributed processing prototype in ROS2 that simulates edge computing architectures for embodied cognition experiments. This system explores the parallels between edge computing and biological neural networks, particularly how distributed systems might support forms of awareness or cognition in android embodiments.

## Features

- **Distributed Node Network**: Simulates a network of edge nodes with configurable communication constraints
- **Network Condition Simulation**: Models varying latency and bandwidth between nodes
- **Local Processing Modules**: Mimics edge computing nodes with local processing capabilities
- **Global Integration Layer**: Aggregates insights from distributed nodes for system-wide awareness
- **Embodied Cognition Interface**: Provides physical interaction simulation for android embodiments
- **Real-time Visualization**: Visualizes data flow and decision-making patterns across the network
- **Configurable Parameters**: Network conditions can be adjusted via YAML configuration files

## Prerequisites

- Python 3.8+
- ROS2 (Foxy, Galactic, or Humble recommended)
- Required Python packages:
  - `rclpy`
  - `rclpy_components`
  - `std_msgs`
  - `sensor_msgs`
  - `geometry_msgs`
  - `nav_msgs`
  - `tf2_ros`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/embodied-cognition-edge-sim.git
   cd embodied-cognition-edge-sim
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Build the ROS2 package:**
   ```bash
   colcon build
   ```

4. **Source the environment:**
   ```bash
   source install/setup.bash
   ```

## Setup Instructions

1. Ensure ROS2 is properly installed and sourced
2. Build and source the package as described above
3. Configure network parameters in `config/network_params.yaml` as needed

## Environment Variables

- `ROS_DOMAIN_ID`: Set the ROS2 domain ID for network isolation (optional)
- `RMW_IMPLEMENTATION`: Choose the RMW implementation (e.g., FastDDS, CycloneDDS)

## Usage Examples

### Launching the Simulation

```bash
ros2 launch embodied_edge_sim simulation.launch.py
```

### Running Individual Nodes

```bash
ros2 run embodied_edge_sim edge_node
ros2 run embodied_edge_sim network_simulator
ros2 run embodied_edge_sim cognition_interface
```

### Running Tests

```bash
colcon test
```

## API Documentation

This project uses ROS2 standard messaging interfaces:
- `std_msgs`: Standard data types (int, float, string, etc.)
- `sensor_msgs`: Sensor data messages
- `geometry_msgs`: Geometric data types (pose, twist, etc.)
- `nav_msgs`: Navigation-related messages
- `tf2_ros`: Transform library for coordinate frame management

## Project Structure

```
embodied-cognition-edge-sim/
├── src/
│   └── embodied_edge_sim/
│       ├── edge_node.py
│       ├── network_simulator.py
│       ├── cognition_interface.py
│       ├── visualization_manager.py
│       ├── global_integrator.py
│       ├── latency_model.py
│       ├── edge_processor.py
│       ├── node_coordinator.py
│       ├── physical_interface.py
│       ├── data_flow_visualizer.py
│       └── decision_analyzer.py
├── launch/
│   └── simulation.launch.py
├── config/
│   └── network_params.yaml
├── test/
│   └── test_edge_processing.py
├── package.xml
├── setup.py
├── requirements.txt
└── Dockerfile
```

## Testing

Run the test suite using:

```bash
colcon test
```

Or run specific tests:

```bash
python3 -m pytest test/test_edge_processing.py
```

## Deployment

### Docker Deployment

Build the Docker image:

```bash
docker build -t embodied-edge-sim .
```

Run the container:

```bash
docker run -it embodied-edge-sim
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction,...
```