from setuptools import setup, find_packages

install_requires = ["requests"]

setup(
    name="grafana_screenshot_helper",
    version="0.3",
    # py_modules=["grafana_screenshot_helper"],
    packages=["grafana_screenshot_helper"],
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
