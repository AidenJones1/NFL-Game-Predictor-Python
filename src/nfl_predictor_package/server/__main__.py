import sys

def main(task: str):
    # TODO: Create module for accessing/saving in directories
    # TODO: Create module for downloading stats
    # TODO: Create module for ELO Rating System
    # TODO: Create module for creating datasets for the model
    # TODO: Create module for machine learning model
    pass

if __name__ == "__main__":
    # Check if an argument exist
    if len(sys.argv) > 1:

        # Check if the first argument is one of two options
        task = sys.argv[1]
        if task in ["--train/test", "--predict"]:
            main(task = task)
            sys.exit()
    
    # Invalid Argument
    print("ERROR: Invalid argument!")