# Genshin Impact Companion Hub & Build Guide

An original, multi-platform utility application built using Python and the Flet framework. This project demonstrates a clear three-tier separation of concerns across presentation, service logic, and local data persistence layers.

## Project Structure Overview
* `app.py` - Main desktop graphical workspace interface layout.
* `mobile_app.py` - Handheld simulator companion view layout.
* `service.py` - Independent Logic & Service layer abstraction.
* `data/` - Hard disk file-system data storage (JSON models).
* `icons/` - Graphical application workspace assets.

## Installation & Setup Instructions

### 1. Prerequisites
Ensure you have a modern Python installation initialized on your device path (Python 3.9 through Python 3.12 verified).

### 2. Dependency Configuration
Install the required architectural UI framework and HTTP communication layers via your machine terminal:
```bash
pip install flet httpx
