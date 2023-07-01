import multiprocessing
import os
import subprocess

import more_itertools
from natsort import natsorted

if __name__ == '__main__':
    banner = """\n ██████╗ ██████╗ ███╗   ██╗ ██████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗ ██████╗███████╗
██╔════╝██╔═══██╗████╗  ██║██╔════╝ ██╔══██╗██║   ██║██╔════╝████╗  ██║██╔════╝██╔════╝
██║     ██║   ██║██╔██╗ ██║██║  ███╗██████╔╝██║   ██║█████╗  ██╔██╗ ██║██║     █████╗  
██║     ██║   ██║██║╚██╗██║██║   ██║██╔══██╗██║   ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝  
╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝██║  ██║╚██████╔╝███████╗██║ ╚████║╚██████╗███████╗
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝
                                                                                       
 ██████╗██╗      ██████╗ ███████╗██╗   ██╗██████╗ ███████╗                             
██╔════╝██║     ██╔═══██╗██╔════╝██║   ██║██╔══██╗██╔════╝                             
██║     ██║     ██║   ██║███████╗██║   ██║██████╔╝█████╗                               
██║     ██║     ██║   ██║╚════██║██║   ██║██╔══██╗██╔══╝                               
╚██████╗███████╗╚██████╔╝███████║╚██████╔╝██║  ██║███████╗                             
 ╚═════╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝                             
                                                                                       
 █████╗ ██╗      ██████╗  ██████╗ ██████╗ ██╗████████╗██╗  ██╗███╗   ███╗              
██╔══██╗██║     ██╔════╝ ██╔═══██╗██╔══██╗██║╚══██╔══╝██║  ██║████╗ ████║              
███████║██║     ██║  ███╗██║   ██║██████╔╝██║   ██║   ███████║██╔████╔██║              
██╔══██║██║     ██║   ██║██║   ██║██╔══██╗██║   ██║   ██╔══██║██║╚██╔╝██║              
██║  ██║███████╗╚██████╔╝╚██████╔╝██║  ██║██║   ██║   ██║  ██║██║ ╚═╝ ██║              
╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝              
                                                                                       """
    print(banner)
    print("Welcome to the Congruence Closure Algorithm by Lorenzo Bonanni\n")
    plots = input("Do you want to see plots? [y/N] ")
    if plots == "y":
        plots = True
    elif plots == "n" or plots == "" or plots == "N":
        plots = False

    input_phrase = "INSTRUCTIONS:\n" \
                   "* If you want to solve multiple equations you have two options:\n" \
                   "\t1. Place the SMT files into a directory and then insert the relative path below\n" \
                   "\t\tExample: ./ar_inputs\n" \
                   "\t2. List all the files relative paths below followed by a space\n" \
                   "\t\tExample: ./ar_inputs/input1.smt2 ./ar_inputs/input2.smt2\n" \
                   "* If you want to test the algorithm on the bundled examples follow the procedure described before " \
                   "and insert `./ar_inputs` as directory\n" \
                   "* If you want to test the code only on one equation input the smt file relative paths below\n" \
                   "\tExample: ./ar_inputs/input1.smt2\n\n" \
                   "INPUT: "
    choice = input(input_phrase)
    concurrent = input("Number of parallel Executions? [-1 all cores] ")
    concurrent = int(concurrent)
    if concurrent == -1:
        concurrent = multiprocessing.cpu_count()

    if os.path.isdir(choice):
        BASE_PATH = choice
        files = [BASE_PATH + '/' + f for f in sorted(os.listdir(BASE_PATH)) if '.smt2' in f]
    else:
        files = choice.split(' ')
    flag = ' -p' if plots else ""

    if not os.path.exists('outputs'):
        os.mkdir('outputs')

    if not os.path.exists('outputs/csv'):
        os.mkdir('outputs/csv')

    files = natsorted(files, key=lambda y: y.lower())
    batches = more_itertools.batched(files, concurrent)
    for batch in batches:
        processes = []
        for f in batch:
            args = f'./congruenceClosure {f}{flag}'
            # args = f'python main.py {f}{flag}'
            p = subprocess.Popen(args, shell=True)
            processes.append(p)
        for pe in processes:
            pe.wait()
