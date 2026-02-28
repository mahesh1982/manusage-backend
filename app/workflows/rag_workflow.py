from langgraph.graph import StateGraph

class RAGWorkflow:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def build(self):
        graph = StateGraph()
        graph.add_node("retrieve", self.pipeline.retriever.search)
        graph.add_node("generate", self.pipeline.run)
        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "generate")
        return graph.compile()
