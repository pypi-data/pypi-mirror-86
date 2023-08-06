import json
import logging
import logging.config
import os
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / '..'))

import geofileops.geofileops as geofileops

def main():
    
    ##### Init #####
    # Init logging
    script_dir = Path(__file__).resolve().parent
    with open(script_dir / 'logging.json', 'r') as log_config_file:
        log_config_dict = json.load(log_config_file)
    logging.config.dictConfig(log_config_dict)
    logger = logging.getLogger()
    
    # Prepare output path
    tolerance = 0.20
    input_path = Path(r"X:\GIS\GIS DATA\Percelen_ALP\Vlaanderen\Perc_VL_2020_2020-10-05\perc_2020_met_k_2020-10-05.gpkg")
    output_path = input_path.parent / f"{input_path.stem}_simpl{input_path.suffix}"
    
    ##### Go! #####
    logger.info("Start")
    geofileops.simplify(
            input_path=input_path,
            output_path=output_path,
            tolerance=tolerance,
            force=True)
    logger.info("Ready")

if __name__ == '__main__':
    main()
