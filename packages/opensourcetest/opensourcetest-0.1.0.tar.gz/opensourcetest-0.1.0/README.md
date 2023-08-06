# OpenSourceTest

# [![pyversions](https://img.shields.io/badge/opensourcetest-v0.1.0-brightgreen)](https://pypi.org/project/opensourcetest-test-test/)[![pyversions](https://img.shields.io/badge/pypi-v0.1.0-orange)](https://pypi.org/project/opensourcetest-test-test/)[![pyversions](https://img.shields.io/badge/pytest-5.x-green)](https://docs.pytest.org)[![pyversions](https://img.shields.io/badge/requests-2.x-green)](http://docs.python-requests.org/en/master/ )[![pyversions](https://img.shields.io/badge/allure-2.x-green)](https://docs.qameta.io/allure/  )

`OpenSourceTest`将为您创建更加自由的软件接口测试，不是为了简单而简单，而是为您提供更自由的扩展的，适用于不同功能场景的接口自动化测试框架。

## 设计思想

- 不丢弃轮子本身的优秀特性
- 不过度封装
- 提供更加多的可操作对象给使用者，即时你使用基本框架已经满足需求
- 拥抱开源

## 主要特点

- 继承 [`requests`][requests]的所有强大功能

- 以[`yaml`][yaml]格式定义接口，[`yaml`][yaml]对象自动注入
- 使用[`jmespath`][jmespath]提取和验证[`json`][json]响应
- 完美兼容[`pytest`][pytest]，您可以使用您想使用的任何[`pytest`][pytest]格式
- 完美兼容[`allure`][allure]，您可以使用您想使用的任何[`allure`][allure]命令
- 支持**CLI**命令，直接创建您所需要的项目架构

## OpenSourceTest 社区

欢迎测试小伙伴加群，讨论测试框架技术！

![community](./docs/images/community.jpg)

[json]: http://json.com/
[yaml]: http://www.yaml.org/
[requests]: http://docs.python-requests.org/en/master/
[pytest]: https://docs.pytest.org/
[pydantic]: https://pydantic-docs.helpmanual.io/
[jmespath]: https://jmespath.org/
[allure]: https://docs.qameta.io/allure/