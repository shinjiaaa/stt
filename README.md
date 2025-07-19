<<<<<<< HEAD
## 주제: 메가커피 키오스크 만들기
### 프로젝트 소개
---
+ 사용: Python, Pyqt, qt desinger, DB, SQLite3
+ 기간: 2023.06.13~2023.06.19 (7일)
+ 프로젝트 목적 : 특정 키오스크를 제작하며 DB와 Python활용을 효율적으로 배우는데 목적을 둔다. 
+ 프로젝트 기능
  + 사용자가 취향에 맞는 음료를 주문할 수 있다.
  + 사용자가 원하는 결제방식으로 주문할 수 있다.
+ 프로젝트 개발 툴:
  + PyQt
  + qt Designer
+ 프로젝트 개발 환경:
  + [OS] Windows OS, Window 10
  + [Browser] Chrome
  + [Language] Python 3.11
  + [Library] NumPy, Pandas
  + [FrameWork] PyQt, qt Designer
=======
# Python Audio Processing Tutorials

Welcome to the Python Audio Processing Tutorials repository. This repository contains two main projects focusing on real-time audio processing using different technologies and frameworks.

## Projects

### 1. RTZR Streaming STT API(gRPC) with Mic. Interface

This project demonstrates how to set up a real-time streaming Speech-to-Text (STT) API using gRPC with microphone interface capabilities. It requires the installation of the `PyAudio` library and additional setup for gRPC communication.

- **Requirements**: PyAudio (see [installation instructions](https://pypi.org/project/PyAudio/)).
- **Setup**: Download necessary `.proto` files and generate gRPC client code. For details, check the project's [README](./python-stt-sample/).

### 2. Triton, Tritony VAD Client Sample

This project showcases the use of the Triton Inference Server and Tritony Voice Activity Detection (VAD) to process and analyze audio streams effectively. It involves setting up a Docker container and running a Triton server.

- **Requirements**: pydub, tritonclient, tritony
- **Setup**: Build and run a Docker image for the Triton Inference Server. Testing is facilitated through predefined scripts and pytest. For more information, visit the project's [README](./tritony-sample/).

### 3. STT and STT summary WEBAPP with Python streamlit

Implementation of a web app using only Python's Streamlit and Return Zero's API, without knowledge of frontend and backend development. This web app include functionality to convert audio files to text using Return Zero's API for Speech-to-Text (STT), and then summarizes the converted text.

- **Requirements**: streamlit, requests, pytorch, transformers
- **Setup**: Install requirement librarys, Run streamlit and submit your information. For more information, visit the project's [README](./streamlit-webapp/).



## General Installation

Most project dependencies can be installed via pip:

```bash
pip install -r requirements.txt
```
>>>>>>> 5a38477c8820758d5d86c47ed813a9f83196205f
