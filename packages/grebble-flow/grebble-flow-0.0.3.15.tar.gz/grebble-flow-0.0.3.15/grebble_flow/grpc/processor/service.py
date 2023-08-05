import json

from grebble_flow.grpc.processor import processor_pb2_grpc, processor_pb2
from grebble_flow.managment.manager import FlowManager


class ProcessorService(processor_pb2_grpc.ProcessorServicer):
    def __init__(self, *args, **kwargs):
        self.flow_manager = FlowManager()

    def Execute(self, request, context):
        # get the string from the incoming request
        flow_name = request.flowName
        data = request.data

        try:
            data = json.loads(data)
        except:
            pass
        for item in self.flow_manager.run(flow_name, data):
            yield processor_pb2.FlowResponse(
                jsonString=json.dumps(item), streamEnd=False
            )

        yield processor_pb2.FlowResponse(jsonString="", streamEnd=True)
