class CubeSolver:
    def __init__(self):
        raise NotImplementedError
    
    def to_json(self):
        raise NotImplementedError

    def get_params_string(self):
        raise NotImplementedError
    
    def pause(self):
        raise NotImplementedError

    def resume(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def export_results(self, indeces:list[int] = None):
        raise NotImplementedError
    
    def get_log_info(self):
        raise NotImplementedError