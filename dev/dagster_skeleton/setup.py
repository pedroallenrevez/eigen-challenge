from setuptools import find_packages, setup

setup(
    name="dagster_skeleton",
    packages=find_packages(exclude=["dagster_skeleton_tests"]),
    install_requires=["dagster", "dagster-cloud"],
    extras_require={"dev": ["dagit", "pytest"]},
)
