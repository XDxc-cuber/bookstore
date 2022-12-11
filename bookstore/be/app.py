import os, sys

if __name__ == "__main__":
    this_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(this_path)
    sys.path.append(parent_path)
    
    from be import serve
    serve.be_run()
