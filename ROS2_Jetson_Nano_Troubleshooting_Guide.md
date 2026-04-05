# ROS2 Jetson Nano Troubleshooting Guide

## Common Issues and Solutions

### 1. Missing Libraries
**Symptom**: Errors like `ModuleNotFoundError: No module named 'rclpy'` or `ImportError: libpython3.8.so.1.0: cannot open shared object file: No such file or directory`
**Solution**: Install required dependencies:
```bash
sudo apt update
sudo apt install -y python3-colcon-common python3-catkin-pkg-modules
```

### 2. Build Errors
**Symptom**: `CMake Error at /usr/share/cmake-3.22/Modules/FindPackageHandleStandardArgs.cmake:627 (message):
  Could NOT find PythonInterp (found suitable version "3.8.10", but version is
  below required version "3.10")`
**Solution**: Use Python 3.10+:
```bash
update-alternatives --set python3 /usr/bin/python3.10
```

### 3. Node Not Found
**Symptom**: `ros2 node list` shows no nodes
**Solution**: Source the workspace:
```bash
source ~/ros2_ws/install/setup.bash
```

### 4. Communication Errors
**Symptom**: Nodes fail to communicate
**Solution**: Ensure all nodes are in the same namespace:
```bash
ros2 service list  # Should show services from all nodes
```

## References
1. [ROS2 Installation Guide](https://docs.ros.org/en/rolling/Installation/Ubuntu-Installation-ROS2-<distro>.html)
2. [ROS2 Troubleshooting](https://github.com/ros2/ros2/issues)
3. [Jetson Nano Documentation](https://docs.nvidia.com/jetson/)