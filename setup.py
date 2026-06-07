from setuptools import find_packages, setup

package_name = 'lab_2_tb'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='david',
    maintainer_email='davidtorrest1097@gmail.com',
    description='Lab 2 — TurtleBot3 trajectories and mapping',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'circle_trajectory = lab_2_tb.circle_trajectory:main',
            's_trajectory = lab_2_tb.s_trajectory:main',
        ],
    },
)
