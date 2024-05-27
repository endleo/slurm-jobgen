#!/bin/python3

import json
import os

with open("config.json") as config_file:
    conf = json.load(config_file)

    for machine in conf["machines"]:
        os.makedirs(f"jobs/{machine['name']}", exist_ok=True)
        os.makedirs(f"results/{machine['name']}", exist_ok=True)
        for run in machine["runs"]:
            with open(f"jobs/{machine['name']}/{run['name']}.sh", mode="w+") as batchfile:
                batchfile.write("#!/bin/bash\n\n")

                # slurm parameters that are the same for every script on the machine, e.g. partition
                for p in machine["sbatch_params"]:
                    batchfile.write(f"#SBATCH {p}\n")

                # slurm parameters that are specific for this run
                if "additional_sbatch_params" in run:
                    for p in run["additional_sbatch_params"]:
                        batchfile.write(f"#SBATCH {p}\n")
                batchfile.write(f"#SBATCH -N {run['n_nodes']}\n")
                batchfile.write(f"#SBATCH --ntasks-per-node={run['n_tasks']}\n")
                batchfile.write(f"#SBATCH --time={run['time']}\n")
                batchfile.write("\n")

                if "setup_commands" in run:
                    for p in run["setup_commands"]:
                        batchfile.write(f"{p}\n")

                batchfile.write(f"srun {run['exec_path']}")
                if "exec_params" in run:
                    for p in run["exec_params"]:
                        batchfile.write(f" {p}")
                if "no_output" in run and run["no_output"]:
                    continue
                batchfile.write(f" > results/{machine['name']}/{run['name']}_$SLURM_JOB_ID.txt\n")