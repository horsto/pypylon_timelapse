# Populate jobs
from datetime import datetime
from dj_schemas import *

if __name__ == "__main__":
    print('############ Similarity ############')
    Similarity.populate(display_progress=True, reserve_jobs=True, suppress_errors=True, order="random")
