"""
[![NPM version](https://badge.fury.io/js/cdk-alps-spec-rest-api.svg)](https://badge.fury.io/js/cdk-alps-spec-rest-api)
[![PyPI version](https://badge.fury.io/py/cdk-alps-spec-rest-api.svg)](https://badge.fury.io/py/cdk-alps-spec-rest-api)
![Release](https://github.com/mmuller88/cdk-alps-spec-rest-api/workflows/Release/badge.svg)

# CDK Alps Spec Rest Api

CDK Construct library constructed with the help of Pahud https://www.youtube.com/watch?v=cTsSXYOYQPw&t=2s <3.

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

stack = cdk.Stack(app, "my-demo-stack", env=env)

AlpsSpecRestApi(stack, "AlpsSpecRestApi")
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class AlpsSpecRestApi(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-alps-spec-rest-api.AlpsSpecRestApi",
):
    def __init__(self, scope: aws_cdk.core.Construct, id: builtins.str) -> None:
        """
        :param scope: -
        :param id: -
        """
        props = AlpsSpecRestApiProps()

        jsii.create(AlpsSpecRestApi, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-alps-spec-rest-api.AlpsSpecRestApiProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class AlpsSpecRestApiProps:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlpsSpecRestApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AlpsSpecRestApi",
    "AlpsSpecRestApiProps",
]

publication.publish()
