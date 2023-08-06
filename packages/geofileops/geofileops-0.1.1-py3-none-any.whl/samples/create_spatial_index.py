import json
import logging
import logging.config
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / '..'))

from geofileops import geofile

def main():
    
    # Init logging
    script_dir = Path(__file__).resolve().parent
    with open(script_dir / 'logging.json', 'r') as log_config_file:
        log_config_dict = json.load(log_config_file)
    logging.config.dictConfig(log_config_dict)
    #logger = logging.getLogger()
    
    # Go!
    path=r"X:\Monitoring\OrthoSeg\sealedsurfaces\output_vector\sealedsurfaces_BEFL_2019_ofw_18\sealedsurfaces_BEFL_2019_ofw_18.gpkg"
    geofile.create_spatial_index(path=path, layer=None)

if __name__ == '__main__':
    main()
