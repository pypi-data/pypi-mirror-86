# VSColab

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
![python version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-blue?logo=python)

Use Colab GPU's and TPU's on your VSCode using the Remote-SSH plugin.

## Installation

```
$ pip install VSColab
```

## Getting Started

Starter Code: https://colab.research.google.com/drive/1u-mCfTPq2w5YIpqwyKZRmgplKB7VxkO_?usp=sharing

### Follow these Steps

* Run all the cells in the Colab Notebook, you will get an output containing the username, tunnel, port number.
* Copy it.
* Install the Remote-SSH extension on your VSCode.
* Open its config file, and paste the copied statements.
* Then connect to the host using this extension.
* Download the python extensions, and select the Python interpreter.

### SSH

To SSH into it, open the terminal and type:
```
ssh root@<tunnel-id> -p<port-number>
```

### Viola! A fully functional ML/AI setup...