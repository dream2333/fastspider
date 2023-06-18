from fastspider.pipeline import Pipeline


class ExamplePipeline1(Pipeline):

    def process_item(self, item):
        print("管道1")
        print(item.astuple())

    
class ExamplePipeline2(Pipeline):

    def process_item(self, item):
        print("管道2")
        return item