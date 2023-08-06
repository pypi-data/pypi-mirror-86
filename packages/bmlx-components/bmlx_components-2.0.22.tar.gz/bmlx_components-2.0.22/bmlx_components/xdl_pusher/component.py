from bmlx.flow import (
    Component,
    ComponentSpec,
    ExecutorClassSpec,
    DriverClassSpec,
    ExecutionParameter,
    ChannelParameter,
    Channel,
)
from bmlx.execution.driver import BaseDriver
from bmlx_components import custom_artifacts
from typing import Text, Optional, List
from bmlx_components.xdl_pusher.executor import PusherExecutor
from bmlx.execution.launcher import Launcher


class PusherSpec(ComponentSpec):
    """ Pusher spec """

    PARAMETERS = {
        "model_name": ExecutionParameter(
            type=(str, Text),
            optional=False,
            description="模型名称"
        ),
        "emb_collection": ExecutionParameter(
            type=(str, Text),
            optional=False,
            description="模型的sparse embedding文件的配送collection"
        ),
        "graph_collection": ExecutionParameter(
            type=(str, Text), optional=False,
            description="模型的图结构相关部分的配送collection"
        ),
        "fg_collection": ExecutionParameter(
            type=(str, Text), optional=False,
            description="模型使用的 fg 配置所属的配送collection"),
        "fg_name": ExecutionParameter(
            type=(str, Text), optional=False,
            description="特征预处理文件名称"),
        "resource_processor": ExecutionParameter(
            type=(str, Text), optional=True,
            description="使用老版本resource发布时候的处理方式，默认为 DELIVER-V1"
        ),
        "author": ExecutionParameter(
            type=(str, Text), optional=False, description="配送需要填写负责人邮箱"),
        "namespace": ExecutionParameter(
            type=(str, Text),
            optional=True,
            description="命名空间"
        ),
        "product_namespace": ExecutionParameter(
            type=(str, Text), optional=False
        ),
        "test_env": ExecutionParameter(
            type=bool,
            optional=True,
            description="是否为测试环境"
        ),
        "skip_stale_model_hour": ExecutionParameter(
            type=int,
            optional=True,
            description="比当前时间早多少小时的数据训练出来的模型不会发布"
        ),
        "disable_skip_execution": ExecutionParameter(
            type=bool,
            optional=True,
            description="是否默认为skip(用户不需要填写)"),
    }

    INPUTS = {
        "converted_model": ChannelParameter(
            type=custom_artifacts.ConvertedModel,
            description="转化后的在线模型地址"
        )
    }
    OUTPUTS = {"output": ChannelParameter(type=custom_artifacts.PushedModel, description="待推送模型")}


class Pusher(Component):
    SPEC_CLASS = PusherSpec

    EXECUTOR_SPEC = ExecutorClassSpec(PusherExecutor)

    DRIVER_SPEC = DriverClassSpec(BaseDriver)

    def __init__(
        self,
        converted_model: Channel,
        model_name: Text,
        emb_collection: Text,
        graph_collection: Text,
        fg_collection: Text,
        fg_name: Text,
        product_namespace: Text,  # cannon 发布的namespace，业务线+"_" +应用名
        author: Optional[Text] = None,
        resource_processor: Optional[Text] = None,
        namespace: Optional[Text] = "default",
        skip_stale_model_hour: Optional[int] = 72,  # 比当前时间早多少小时的数据训练出来的模型不会发布
        test_env: bool = False,
        disable_skip_execution: bool = False,
        instance_name: Optional[Text] = None,
    ):
        if not product_namespace:
            raise ValueError("Empty product_namespace, should be {业务线}_{应用名}")
        if not converted_model:
            raise ValueError("Empty pushed model")
        if not model_name:
            raise ValueError("Empty model name")
        if not emb_collection:
            raise ValueError("Empty emb_collection name")
        if not graph_collection:
            raise ValueError("Empty graph collection name")
        if not fg_collection:
            raise ValueError("Empty fg collection name")
        if not fg_name:
            raise ValueError("Empty fg name")

        resource_processor = resource_processor or "DELIVER-V1"
        author = author or "bmlx@bigo.sg"

        output = Channel(
            artifact_type=custom_artifacts.PushedModel,
            # 注意！！！ 这里的 name 填充为model_name，用于显示在模型中心上
            artifacts=[custom_artifacts.PushedModel(name=model_name)],
        )

        spec = PusherSpec(
            converted_model=converted_model,
            model_name=model_name,
            emb_collection=emb_collection,
            graph_collection=graph_collection,
            fg_collection=fg_collection,
            fg_name=fg_name,
            resource_processor=resource_processor,
            author=author,
            namespace=namespace,
            product_namespace=product_namespace,
            skip_stale_model_hour=skip_stale_model_hour,
            test_env=test_env,
            disable_skip_execution=disable_skip_execution,
            output=output,
        )

        super(Pusher, self).__init__(spec=spec, instance_name=instance_name)

    def get_launcher_class(self, ctx):
        return Launcher

    def skip_execution(self, pipeline_execution, exec_properties) -> bool:
        if (
            not exec_properties["disable_skip_execution"]
            and not pipeline_execution.deployment_running
        ):
            return True
        else:
            return False
