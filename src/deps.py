_chain = None

def set_chain(chain):  # called at startup
    global _chain
    _chain = chain

def get_chain():
    assert _chain is not None, "QA chain not initialized"
    return _chain