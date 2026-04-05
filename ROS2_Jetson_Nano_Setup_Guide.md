# ROS2 Jetson Nano Setup Guide

## Overview
This guide provides step-by-step instructions for installing ROS2 (Robot Operating System 2) on the NVIDIA Jetson Nano, a popular single-board computer for robotics and AI applications.

## Prerequisites
- NVIDIA Jetson Nano with L4T (Linux for Tegra) OS
- USB flash drive (8GB+ recommended)
- MicroSD card (32GB+ recommended)
- Power supply for Jetson Nano

## Installation Steps
### 1. Flash Jetson Nano OS
1. Download L4T from [NVIDIA Developer](https://developer.nvidia.com/embedded/linux)
2. Flash to MicroSD using Etcher or `dd` command:
   ```bash
   sudo dd if=Linux_for_Tegra/L4T/L4T_XXXX_XXX/tegra194-p3445-200a-0002.dts of=/dev/sdX bs=4M status=progress
   ```

### 2. Install ROS2
#### Option A: Build from Source (Recommended)
1. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install -y build-essential cmake git python3-colcon-common
   ```
2. Create catkin workspace:
   ```bash
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws
   colcon build --symlink-install --packages-select rcl
   ```
3. Source the setup file:
   ```bash
   echo 'source ~/ros2_ws/install/setup.bash' >> ~/.bashrc
   source ~/.bashrc
   ```

#### Option B: Binary Installation (Experimental)
```bash
# Add repository (check latest version at https://repomodel.ros2.io)
 sudo sh -c 'echo "deb http://packages.ros.org:11350/repos/ros-<distro>-main-<arch>.deb /" > /etc/apt/sources.list.d/ros-latest.list'

# Install ROS2 core
sudo apt install ros-<distro>-desktop
```

## Verification
1. Check ROS2 version:
   ```bash
   ros2 --version
   ```
2. List available nodes:
   ```bash
   ros2 node list
   ```
3. Test with a simple talker/listener example:
   ```bash
   # In one terminal
   ros2 run demo_nodes_cpp talker
   
   # In another terminal
   ros2 run demo_nodes_cpp listener
   ```

## Troubleshooting
- **Missing libraries**: Run `sudo apt install ros-<distro>-desktop` to install full desktop version
- **Permission issues**: Add user to `dialout` group:
  ```bash
  sudo usermod -aG dialout $USER
  ```
- **Build errors**: Check [ROS2 GitHub issues](https://github.com/ros2/ros2/issues) for ARM64-specific problems

## References
1. [NVIDIA Jetson Nano Documentation](https://docs.nvidia.com/jetson/)
2. [ROS2 Installation](https://docs.ros.org/en/rolling/Installation/Ubuntu-Installation-ROS2-<distro>.html)
3. [Community Forum](https://discourse.ros.org/)