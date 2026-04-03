from setuptools import setup, find_packages

package_name = 'embodied_edge_sim'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/simulation.launch.py']),
        ('share/' + package_name + '/test', ['test/test_edge_processing.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='embodied_edge_sim',
    maintainer_email='info@embodied-edge-sim.com',
    description='Embodied Cognition Edge Simulation package',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'edge_node = src.embodied_edge_sim.edge_node:main',
            'network_simulator = src.embodied_edge_sim.network_simulator:main',
            'cognition_interface = src.embodied_edge_sim.cognition_interface:main',
            'visualization_manager = src.embodied_edge_sim.visualization_manager:main',
            'global_integrator = src.embodied_edge_sim.global_integrator:main',
            'node_coordinator = src.embodied_edge_sim.node_coordinator:main',
            'physical_interface = src.embodied_edge_sim.physical_interface:main',
            'decision_analyzer = src.embodied_edge_sim.decision_analyzer:main',
        ],
    },
    package_data={
        package_name: ['package.xml', 'launch/*', 'test/*']
    }
)