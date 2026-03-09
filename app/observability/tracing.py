from opentelemetry import trace

tracer = trace.get_tracer("manusage.rag")

def start_rag_span(name: str):
    return tracer.start_as_current_span(name)
