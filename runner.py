import os
import subprocess

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
                   "\t\tExample: ./ar_inputs/input1.smt ./ar_inputs/input2.smt\n" \
                   "* If you want to test the algorithm on the bundled examples follow the procedure described before " \
                   "and insert `./ar_inputs` as directory\n" \
                   "* If you want to test the code only on one equation input the smt file relative paths below\n" \
                   "\tExample: ./ar_inputs/input1.smt\n\n" \
                   "INPUT: "
    choice = input(input_phrase)
    if os.path.isdir(choice):
        BASE_PATH = choice
        files = [BASE_PATH+'/'+f for f in sorted(os.listdir(BASE_PATH)) if '.smt2' in f]
    else:
        files = choice.split(' ')
    flag = ' -p' if plots else ""

    if not os.path.exists('outputs'):
        os.mkdir('outputs')

    for f in sorted(files):
        args = f'./congruenceClosure {f}{flag}'
        # args = f'python main.py {f}{flag}'
        p = subprocess.Popen(args, shell=True)
        p.wait()
