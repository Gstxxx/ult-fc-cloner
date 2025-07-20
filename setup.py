#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup para o EA FC 25 Web App Scraper
Configuração para conversão em executável
"""

from setuptools import setup, find_packages

setup(
    name="fc25-scraper",
    version="1.0.0",
    description="Scraper automatizado para EA FC 25 Web App",
    author="Sistema de Web Scraping",
    packages=find_packages(),
    install_requires=[
        "selenium==4.15.2",
        "webdriver-manager==4.0.1",
        "pandas==2.1.3",
        "beautifulsoup4==4.12.2",
        "lxml==4.9.3",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "fc25-scraper=fc25_scraper:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 