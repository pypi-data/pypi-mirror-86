#!/usr/bin/python


import subprocess, time
import tempfile
from shutil import which
import warnings
import os

#  On import check dependencies
dependencies = [which('RNAfold') is not None,
                which('RNAsubopt') is not None,
                which('RNAeval') is not None]
if False in dependencies:
    warnings.warn('RBS Calculator Vienna is missing dependency ViennaRNA!')
#  End dependency check

debug=0

#Class that encapsulates all of the functions from NuPACK 2.0
class ViennaRNA(dict):

    debug_mode = 0
    RT = 0.61597 #gas constant times 310 Kelvin (in units of kcal/mol)
    param_file = f"-P {os.path.dirname(os.path.realpath(__file__))}/rna_turner1999.par "


    def __init__(self,Sequence_List,material = "rna37"):

        self.ran = 0

        import re
        import random
        import string

        exp = re.compile('[ATGCU]',re.IGNORECASE)

        for seq in Sequence_List:
            if exp.match(seq) == None:
                error_string = "Invalid letters found in inputted sequences. Only ATGCU allowed. \n Sequence is \"" + str(seq) + "\"."
                raise ValueError(error_string)

        self["sequences"] = Sequence_List
        self["material"] = material
        self.install_location = os.path.dirname(os.path.realpath(__file__))

        random.seed(time.time())

        with tempfile.NamedTemporaryFile(delete=False) as temp_file_maker:
            self.prefix = temp_file_maker.name

    def mfe(self, strands, constraints, Temp , dangles, outputPS = False):

        self["mfe_composition"] = strands
        
        Temp = float(Temp)
        if Temp <= 0: raise ValueError("The specified temperature must be greater than zero.")

        seq_string = "&".join(self["sequences"])
        constraints = None
        if constraints is None:
            input_string = seq_string + "\n" 
        else: 
            input_string = seq_string + "\n" + constraints + "\n"

        #write sequence file 
        handle = open(self.prefix,"w")
        handle.write(input_string)
        handle.close()

        #Set arguments
        material = self["material"]

        if material == 'rna1999':
            param_file = f"-P {self.install_location}/rna_turner1999.par "
        else:
            param_file = ''

        if dangles is "none":
            dangles = " -d0 "
        elif dangles is "some":
            dangles = " -d1 "
        elif dangles is "all":
            dangles = " -d2 "

        if outputPS:
            outputPS_str = " "
        else:
            outputPS_str = " --noPS "
            
        if constraints is None:
            args = outputPS_str + dangles + param_file + self.prefix

        else:
            args = outputPS_str + dangles + "-C " + param_file + self.prefix


        #Call ViennaRNA C programs
        cmd = "RNAfold"
        #print(cmd + args)

        output = subprocess.Popen(cmd + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True) #newlines argument was added because subprocess.popen was appending b's to the list output (byte stuff? I dont totally understand)
        std_out = output.communicate()[0]
        #output.tochild.write(input_string)

        while output.poll() is None:
            try:
                output.wait()
                time.sleep(0.001)
            except:
                break

        #if debug == 1: print(output.stdout.read())

        #Skip the unnecessary output lines
        #line = output.stdout.read()
        #print(std_out)

        line = std_out
        words = line.split()
        #print("These are the mfe value for " + str(words))
        bracket_string = words[1]
        #print(bracket_string)
        #print("This is the bracket string " + str(bracket_string))
        (strands,bp_x, bp_y) = self.convert_bracket_to_numbered_pairs(bracket_string)
        #print(strands, bp_x, bp_y)

        energy = float(words[len(words)-1].replace(")","").replace("(","").replace("\n",""))

        self["program"] = "mfe"
        self["mfe_basepairing_x"] = [bp_x]
        self["mfe_basepairing_y"] = [bp_y]
        self["mfe_energy"] = [energy]
        self["totalnt"]=strands

        #print "Minimum free energy secondary structure has been calculated."

    def subopt(self, strands, constraints, energy_gap, Temp = 37.0, dangles = "some", outputPS = False):

        self["subopt_composition"] = strands

        if Temp <= 0: raise ValueError("The specified temperature must be greater than zero.")

        material = self["material"]
        if material == 'rna1999':
            param_file = f"-P {self.install_location}/rna_turner1999.par "
        else:
            param_file = ''

        seq_string = "&".join(self["sequences"])
        #seq_string = self["sequences"][0]

        #print(f'SEQ STRING: {seq_string}')
        if constraints is None:
            input_string = seq_string + "\n" 
        else: 
            input_string = seq_string + "\n" + constraints + "&........." "\n"

        #print(self.prefix)
        with open(self.prefix + '.txt', 'w') as handle:
            handle.write(input_string)

        #Set arguments
        material = self["material"]

        if dangles is "none":
            dangles = " -d0 "
        elif dangles is "some":
            dangles = " -d1 "
        elif dangles is "all":
            dangles = " -d2 "

        if outputPS:
            outputPS_str = ""
        else:
            outputPS_str = " -noPS "
        #Call ViennaRNA C programs

        cmd = "RNAsubopt"
        energy_gap = energy_gap + 2.481
        if constraints is None:
            args = " -e " + str(energy_gap) + " -T " + str(Temp) + dangles + "--sorted --en-only " + param_file + " < " + self.prefix + '.txt'
        else:
            args = " -e " + str(energy_gap) + " -T " + str(Temp) + dangles + "--sorted --en-only " + "-C " + param_file + " < " + self.prefix + '.txt'

        #print(self.prefix)
        #print(cmd + args)
        output = subprocess.Popen(cmd + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True) #newlines argument was added because subprocess.popen was appending b's to the list output (byte stuff? I dont totally understand)
        std_out = output.communicate()[0]
        #output.tochild.write(input_string)

        while output.poll() is None:
            try:
                output.wait()
                time.sleep(0.001)
            except:
                break

        if debug == 1: print(output.stdout.read())

        #Skip unnecessary line
        #line = output.std_out.readline()
        line = std_out

        self["subopt_basepairing_x"] = []
        self["subopt_basepairing_y"] = []
        self["subopt_energy"] = []
        self["totalnt"]=[]

        counter=0  # TODO: Test to see if the latest version of VIENNA requires this workaround
        #print(f"Line: {line}")
        findings = line.split("\n")
        findings = findings[1:]
        findings = [x.split() for x in findings]
        #print(findings)
        for finding in findings:
            if len(finding) != 2:
                continue
            if len(self["sequences"]) > 1:
                binding_positions = finding[0]
                binding_positions = binding_positions.split("&")
                if ")" not in binding_positions[1] and "(" not in binding_positions[1]:
                    #print("This binding site is fake")
                    continue
                else:
                    self["subopt_energy"].append(float(finding[1]))
                    (strands, bp_x, bp_y) = self.convert_bracket_to_numbered_pairs(finding[0])
                    #print(strands, bp_x, bp_y)
                    self["subopt_basepairing_x"].append(bp_x)
                    self["subopt_basepairing_y"].append(bp_y)
            else:
                self["subopt_energy"].append(float(finding[1]))
                (strands, bp_x, bp_y) = self.convert_bracket_to_numbered_pairs(finding[0])
                self["subopt_basepairing_x"].append(bp_x)
                self["subopt_basepairing_y"].append(bp_y)


        self["subopt_NumStructs"] = counter

        self["program"] = "subopt"

        #print "Minimum free energy and suboptimal secondary structures have been calculated."

    def energy(self, strands, base_pairing_x, base_pairing_y, Temp = 37.0, dangles = "all"):

        self["energy_composition"] = strands

        if Temp <= 0: raise ValueError("The specified temperature must be greater than zero.")
        seq_string = "&".join(self["sequences"])
        strands = [len(seq) for seq in self["sequences"]]
        bracket_string = self.convert_numbered_pairs_to_bracket(strands,base_pairing_x,base_pairing_y)
        input_string = seq_string + "\n" + bracket_string + "\n"

        #print(seq_string,strands, bracket_string, input_string)

        handle = open(self.prefix,"w")
        handle.write(input_string)
        handle.close()

        #Set arguments
        material = self["material"]
        if dangles is "none":
            dangles = " -d0 "
        elif dangles is "some":
            dangles = " -d1 "
        elif dangles is "all":
            dangles = " -d2 "

        if material == 'rna1999':
            param_file = f"-P {self.install_location}/rna_turner1999.par "
        else:
            param_file = ''

        #Call ViennaRNA C programs
        cmd = "RNAeval"
        args = dangles + param_file + self.prefix
        #print(cmd + args)

        output = subprocess.Popen(cmd + args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True) #newlines argument was added because subprocess.popen was appending b's to the list output (byte stuff? I dont totally understand)


        while output.poll() is None:
            try:
                output.wait()
                time.sleep(0.001)
            except:
                break

        #if debug == 1: print output.fromchild.read()
        std_out = output.communicate()[0]
        #print(std_out)

        self["energy_energy"] = []        

        line = std_out
        words = line.split()
        #print(line, words)
        if not words:
            raise ValueError('Could not catch the output of RNAeval. Is Vienna installed and in your PATH?')
        energy = float(words[-1].replace("(","").replace(")","").replace("\n",""))

        self["program"] = "energy"
        self["energy_energy"].append(energy)
        self["energy_basepairing_x"] = [base_pairing_x]
        self["energy_basepairing_y"] = [base_pairing_y]

        return energy

    def convert_bracket_to_numbered_pairs(self,bracket_string):

        all_seq_len = len(bracket_string)
        #print(all_seq_len)
        bp_x = []
        bp_y = []
        strands = []

        for y in range(bracket_string.count(")")):
            bp_y.append([])
            #print(bp_y)

        last_nt_x_list = []
        counter=0
        num_strands=0
        #print(bracket_string)
        for (pos,letter) in enumerate(bracket_string[:]):
            if letter is ".":
                counter += 1

            elif letter is "(":
                bp_x.append(pos-num_strands)
                last_nt_x_list.append(pos-num_strands)
                counter += 1

            elif letter is ")":
                nt_x = last_nt_x_list.pop() #nt_x is list of "(" except last entry
                #print('this is the last_nt_x_list ' + str(last_nt_x_list.pop()))
                nt_x_pos = bp_x.index(nt_x) 
                bp_y[nt_x_pos] = pos-num_strands
                counter += 1

            elif letter is "&":
                strands.append(counter)
                counter=0
                num_strands+=1

            else:
                print("Error! Invalid character in bracket notation.")
    

        if len(last_nt_x_list) > 0:
            print("Error! Leftover unpaired nucleotides when converting from bracket notation to numbered base pairs.")

        strands.append(counter)
        if len(bp_y) > 1:
            bp_x = [pos+1 for pos in bp_x[:]] #Shift so that 1st position is 1
            bp_y = [pos+1 for pos in bp_y[:]] #Shift so that 1st position is 1
            #print("subopt bp_x " + str(bp_x))
            #print("subopt bp_y " + str(bp_y))
        
        return (strands,bp_x, bp_y)

    def convert_numbered_pairs_to_bracket(self,strands,bp_x,bp_y):

        bp_x = [pos-1 for pos in bp_x[:]] #Shift so that 1st position is 0
        bp_y = [pos-1 for pos in bp_y[:]] #Shift so that 1st position is 0

        bracket_notation = []
        counter=0
        for (strand_number,seq_len) in enumerate(strands):
            if strand_number > 0: bracket_notation.append("&")
            for pos in range(counter,seq_len+counter):
                if pos in bp_x:
                    bracket_notation.append("(")
                elif pos in bp_y:
                    bracket_notation.append(")")
                else:
                    bracket_notation.append(".")
            counter+=seq_len

        return "".join(bracket_notation)

'''
if __name__ == "__main__":

    sequences = ["TCTGGCAGGGACCTGCACACGGATTGTGTGTGTTCCAGAGATGATAAAAAAGGAGTTAGTCTTGGTATGAGTAAAGGAGAAGAACTTTTCACTGGAGTTGTCCCAATTCTTGTTGAATTAGATGGTGATGTTAATGGGCACAAATTTTCTGTCAGTGGAGAGGGTG"] #,"acctcctta"]
    len(sequences) #,"acctcctta"]
    const_str = None

    test = ViennaRNA(sequences, material = "rna37")
    print(test)
    #dangles = "none"
    #constraints = none

    test.mfe([1], constraints = const_str , dangles = "none", Temp = 37.0)

    bp_x = test["mfe_basepairing_x"][0]
    bp_y = test["mfe_basepairing_y"][0]
    strands = test["totalnt"]
    bracket_string = test.convert_numbered_pairs_to_bracket(strands,bp_x,bp_y)
    print(bracket_string)

    (strands,bp_x, bp_y) = test.convert_bracket_to_numbered_pairs(bracket_string)

    print("Strands = ", strands)
    print("bp_x = ", bp_x)
    print("bp_y = ", bp_y)

    print(test.energy(strands, bp_x, bp_y, dangles = "all"))
    test.subopt(strands,const_str,0.5,dangles = "all")
    print(test)

#    print bracket_string
#    print test.convert_numbered_pairs_to_bracket(strands,bp_x,bp_y)
'''