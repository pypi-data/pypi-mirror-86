from . import sim_template_pb2_grpc as importStub

class SimTemplateService(object):

    def __init__(self, router):
        self.connector = router.get_connection(SimTemplateService, importStub.SimTemplateStub)

    def createRuleFix(self, request, timeout=None):
        return self.connector.create_request('createRuleFix', request, timeout)
