import os  # Operating system library
from glob import glob  # Handles file path names
from setuptools import setup  # Facilitates the building of packages

package_name = "origin_one_description"

# Path of the current directory
cur_directory_path = os.path.abspath(os.path.dirname(__file__))


data_files = [
    ("share/" + package_name, ["package.xml"]),
    ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
    (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    (os.path.join("share", package_name, "rviz"), glob("rviz/*")),
    (os.path.join("share", package_name, "urdf"), glob("./urdf/*.urdf")),
    (os.path.join("share", package_name, "urdf/meshes"), glob("./urdf/meshes/*")),
]

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=data_files,
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Bob Hendrikx",
    maintainer_email="b.hendrikx@avular.com",
    description="Robot description models for the Avular Origin V1.0",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [],
    },
)
