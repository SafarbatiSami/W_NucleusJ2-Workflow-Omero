import sys
import os
import shutil
import subprocess
from subprocess import call
from cytomine.models import Job
from biaflows import CLASS_OBJSEG, CLASS_SPTCNT, CLASS_PIXCLA, CLASS_TRETRC, CLASS_LOOTRC, CLASS_OBJDET, CLASS_PRTTRK, CLASS_OBJTRK
from biaflows.helpers import BiaflowsJob, prepare_data, upload_data, upload_metrics, get_discipline
import time
import shutil
# Assuming biom3d has relevant classes/functions you need to import


def main(argv):
    
    with BiaflowsJob.from_cli(argv) as bj:
        
        bj.job.update(status=Job.RUNNING, progress=0, statusComment="Initialisation...")
        # Assuming these environment variables are set correctly
        img_dir = bj.parameters.img_dir
        msk_dir = bj.parameters.msk_dir
        num_classes = bj.parameters.num_classes
        description = bj.parameters.desc
        
 
        # Construct the command to run biom3d
        cmd = [
            "python", "-m", "biom3d.preprocess_train",
            "--img_dir", img_dir,
            "--msk_dir", msk_dir,
            "--num_classes", str(num_classes),
            "--desc", description
        ]


        status = subprocess.run(cmd)

        if status.returncode != 0:
            print("Running Cellpose failed, terminate")
            sys.exit(1)
                # 5. Pipeline finished

        bj.job.update(progress=100, status=Job.TERMINATED, status_comment="Finished.")

if __name__ == "__main__":
    main(sys.argv[1:])
