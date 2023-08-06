"""
# cdk-noob

A demo construct library created with Projen

# Example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

stack = cdk.Stack(app, "my-demo-stack")

Noob(stack, "Noob")
```

# AWS SSO

Configure your `default` AWS_PROFILE with AWS SSO

```sh
aws configure sso --profile default
```

Configure `credential_process` for the `default` profile

```sh
aws configure set credential_process ${PWD}/.devcontainer/bin/aws-sso-credential-process
```

export `AWS_SHARED_CREDENTIALS_FILE`

```sh
export AWS_SHARED_CREDENTIALS_FILE=~/.aws/config
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

import aws_cdk.aws_ec2
import aws_cdk.core


class Noob(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdk-noob.Noob"):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: 
        """
        props = NoobProps(vpc=vpc)

        jsii.create(Noob, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return jsii.get(self, "endpoint")


@jsii.data_type(
    jsii_type="cdk-noob.NoobProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class NoobProps:
    def __init__(self, *, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None) -> None:
        """
        :param vpc: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NoobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Noob",
    "NoobProps",
]

publication.publish()
