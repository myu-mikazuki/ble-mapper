from setuptools import find_packages, setup

package_name = 'ble_mapper_ble'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='y-mikami',
    maintainer_email='m2250370@photon.chitose.ac.jp',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'ble_detector = ble_mapper_ble.ble_node:main',
            'ble_locator = ble_mapper_ble.ble_locator_node:main',
            'dummy_publisher = ble_mapper_ble.dummy_publisher:main',
            'dummy_tf_publisher = ble_mapper_ble.dummy_tf_publisher:main',
        ],
    },
)
