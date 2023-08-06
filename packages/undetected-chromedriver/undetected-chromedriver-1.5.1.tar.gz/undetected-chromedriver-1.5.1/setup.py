"""

         888                                                  888         d8b
         888                                                  888         Y8P
         888                                                  888
 .d8888b 88888b.  888d888 .d88b.  88888b.d88b.   .d88b.   .d88888 888d888 888 888  888  .d88b.  888d888
d88P"    888 "88b 888P"  d88""88b 888 "888 "88b d8P  Y8b d88" 888 888P"   888 888  888 d8P  Y8b 888P"
888      888  888 888    888  888 888  888  888 88888888 888  888 888     888 Y88  88P 88888888 888
Y88b.    888  888 888    Y88..88P 888  888  888 Y8b.     Y88b 888 888     888  Y8bd8P  Y8b.     888
 "Y8888P 888  888 888     "Y88P"  888  888  888  "Y8888   "Y88888 888     888   Y88P    "Y8888  888   88888888

BY ULTRAFUNKAMSTERDAM (https://github.com/ultrafunkamsterdam)"""

from setuptools import setup


setup(
    name="undetected-chromedriver",
    version="1.5.1",
    packages=["undetected_chromedriver"],
    install_requires=["selenium",],
    url="https://github.com/ultrafunkamsterdam/undetected-chromedriver",
    license="GPL-3.0",
    author="UltrafunkAmsterdam",
    author_email="info@blackhat-security.nl",
    description="""
                Optimized selenium.webdriver.Chrome drop-in, to prevent being triggered by anti-bot services like Distil / CloudFlare / Imperva / DataDome and such.
                main classes: Chrome, ChromeOptions
                Please note: results may vary due to external factors and/or modus operandi. 
                No guarantees are given, yet I can guarantee ongoing and tenacious efforts evading and handling detection algorithms.
                For more information check out the README.""",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
