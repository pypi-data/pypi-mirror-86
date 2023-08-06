[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Open Source Love](https://badges.frapsoft.com/os/gpl/gpl.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Build Status](https://travis-ci.org/WilliamCodeBox/embox.svg?branch=main)](https://travis-ci.org/WilliamCodeBox/embox)
[![codecov](https://codecov.io/gh/WilliamCodeBox/embox/branch/main/graph/badge.svg?token=KIEFL7Q4CV)](https://codecov.io/gh/WilliamCodeBox/embox)

[![PyPI version](https://badge.fury.io/py/embox.svg)](https://badge.fury.io/py/embox)
[![GitHub version](https://badge.fury.io/gh/WilliamCodeBox%2Fembox.svg)](https://badge.fury.io/gh/WilliamCodeBox%2Fembox)
[![Code Lines](https://tokei.rs/b1/github/XAMPPRocky/tokei)](https://github.com/WilliamCodeBox/embox)

# embox

Fundamentals of Electromagnetic with Python

## Install

```bash
> pip search embox
> pip install embox
```

## Developer

### Testing

`embox` is tested by using the [pytest](https://pypi.org/project/pytest/) package, and the test coverage is checked by using the [coverage](https://pypi.org/project/coverage/) package.

A `.coveragerc` config file is created and located in the `embox` package root dir. This config file stores the sub commands `run` and `report` of `coverage`.

Run the following command to test coverage

```bash
coverage run -m pytest
```

Run the following command to show the test coverage report

```bash
coverage report
```
