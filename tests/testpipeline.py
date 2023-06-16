from pipeline import BasePipeline


class TestPipeline1(BasePipeline):

    def process_item(self, item):
        print(item.astuple())

    
class TestPipeline2(BasePipeline):

    def process_item(self, item):
        print("管道2")
        return item