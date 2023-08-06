from grebble_flow.processors.base import BaseFlowProcessor


class SimpleProcessor(BaseFlowProcessor):
    name = "simple-flow-base"

    def execute(self, data, *args, **kwargs):
        """
        :param data: Default data description
        """
        for i in range(0, 100):
            yield {"test": i}
