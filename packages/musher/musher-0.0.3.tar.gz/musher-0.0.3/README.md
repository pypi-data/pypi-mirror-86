# Musher

Simple musical key detection.

# Table of Contents

<!-- MarkdownTOC -->

- [Musher](#musher)
- [Table of Contents](#table-of-contents)
- [Quick Start](#quick-start)
  - [Install](#install)
  - [Documentation](#documentation)
  - [Sample Usage](#sample-usage)
  - [What key profile should I use?](#what-key-profile-should-i-use)
- [Installation](#installation)
  - [Python 3.5+(WIP)](#python-35wip)
  - [C++ 14](#c-14)
    - [Dependencies](#dependencies)
      - [Cmake](#cmake)
      - [Conan](#conan)
    - [Install (WIP)](#install-wip)
- [Usage](#usage)
  - [Key Profiles](#key-profiles)
- [Development](#development)
  - [Python](#python)
    - [Install normally](#install-normally)
    - [Install in debug mode](#install-in-debug-mode)
  - [C++](#c)
    - [Build normally](#build-normally)
    - [Build in debug mode](#build-in-debug-mode)
- [Tests](#tests)
  - [Python](#python-1)
    - [Required dependencies](#required-dependencies)
    - [Running tests](#running-tests)
  - [C++](#c-1)
    - [Required dependencies](#required-dependencies-1)
    - [Running tests](#running-tests-1)
- [Documentation](#documentation-1)
  - [Link to documentation](#link-to-documentation)
  - [Dependencies](#dependencies-1)
  - [How to Generate](#how-to-generate)
  - [Publish to Github Pages](#publish-to-github-pages)
- [Cleanup](#cleanup)
- [Useful links](#useful-links)
- [Credits](#credits)

<!-- /MarkdownTOC -->


# Quick Start

## Install

```bash
pip install musher 
```

## [Documentation](https://jmaldon1.github.io/Musher/index.html)

## [Sample Usage](#usage)

## [What key profile should I use?](#key-profiles)


# Installation

You can choose to install this package in 2 ways, Python and C++. The package was primary written in C++ and wrapped in Python. Choose either of the following methods of installation.


## Python 3.5+(WIP)

```
pip install musher
```

## C++ 14

### Dependencies

#### Cmake

```
-- MacOS --
brew install cmake

-- Linux --
sudo apt install cmake

-- Windows --
Download from https://cmake.org/download/
```

#### Conan

```
pip install conan
```

### Install (WIP)

```
conan install musher
```


# Usage

```python
import os
import musher

audio_file_path = os.path.join("data", "audio_files", "mozart_c_major_30sec.wav")
wav_decoded = musher.decode_wav_from_file(audio_file_path)
print(wav_decoded)
{'avg_bitrate_kbps': 1411,
 'bit_depth': 16,
 'channels': 2,
 'file_type': 'wav',
 'length_in_seconds': 30.0,
 'mono': False,
 'normalized_samples': array([
       [ 0.        ,  0.        ,  0.        , ..., -0.33203125, -0.32833862, -0.3274536 ],
       [ 0.        ,  0.        ,  0.        , ..., -0.29162598, -0.27130127, -0.25457764]
    ], dtype=float32),
 'sample_rate': 44100,
 'samples_per_channel': 1323000,
 'stereo': True}

normalized_samples = wav_decoded["normalized_samples"]
sample_rate = wav_decoded["sample_rate"]
# Different key profiles produce different results.
# 'Temperley' produces good results for classical music.
key_profile_type = "Temperley"
key_output = musher.detect_key(normalized_samples, sample_rate, key_profile_type)
print(key_output)
{'first_to_second_relative_strength': 0.6078072169442225,
 'key': 'C',
 'scale': 'major',
 'strength': 0.7603224296919142}
```

## Key Profiles

[Description of all available key profiles](https://jmaldon1.github.io/Musher/musher_cpp.html#key)

# Development

## Python

### Install normally

```sh
pip install .
# OR
python3 setup.py install
```

### Install in debug mode

```sh
pip install -e .
# OR
python3 setup.py develop
```

_NOTE_: This package has 2 dependencies: **Pybind11** and **Numpy**. You may need to install these python packages if the setup.py does not do it for you.

## C++

### Build normally

```sh
python setup.py cmake

# OR

mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .

```

### Build in debug mode

```sh
python setup.py cmake --debug

# OR

mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DENABLE_TESTS=On
cmake --build .
```

# Tests

## Python

### Required dependencies

```sh
pip install tox pytest
```

### Running tests
This will run tests against a pip installed copy of the source code (best to do before deploying code).

```sh
# Running this command does not require pytest to be installed
tox 
```

This will run tests directly (best to do while modifying the code base).

```sh
pytest ./tests -v
```

## C++

### Required dependencies

1. [Google Test](https://github.com/google/googletest) (Conan should install this for you when the project is built in debug mode.)

### Running tests

```sh
# Ctest
python setup.py ctest

# OR

# Google test
python setup.py gtest
```

# Documentation

Generate documentation using Doxygen, Breathe, and Sphinx.

## [Link to documentation](https://jmaldon1.github.io/Musher/index.html)

## Dependencies

1. [Doxygen >1.5.1](https://www.doxygen.nl/index.html) - Generates C++ documentation
2. [Breathe](https://github.com/michaeljones/breathe) - Translate Doxygen docs to Sphinx docs
3. [Sphinx](https://github.com/sphinx-doc/sphinx) - Generates python documentation
4. [C++ dependencies](#dependencies) - Required to build the project

## How to Generate

```sh
python setup.py cmake --docs
```

## Publish to Github Pages

You must install the python module and generate the docs BEFORE running this command.

   1. `pip install -e .`
   2. [Generate docs](#how-to-generate)

```sh
python setup.py publish_docs -m "Added docs for new function"
```

# Cleanup

This will remove all the temporary files/folders created from building and testing this package.

```sh
python setup.py clean
```

# Useful links

Python audio libraries:

* https://github.com/vinta/awesome-python#audio

# Credits

[Essentia](https://github.com/MTG/essentia) - C++ library for audio and music analysis, description and synthesis, including Python bindings.