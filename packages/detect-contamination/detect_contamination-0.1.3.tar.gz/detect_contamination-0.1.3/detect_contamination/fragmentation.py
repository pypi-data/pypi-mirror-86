import math    
import tempfile
import datetime

# parameters are sequence file_name, fragment length and overlapping length
def fragmentation(filename,length,overlap,index, path):
    #length can not be less than 1 
    sequence_length = 0
    if length <= 0:
        raise ValueError("Invalid fragmentation length")
    #overlap can not be less than 1 or greater than fragment length
    if overlap < 0 or overlap >= length:
        raise ValueError("Invalid overlapping length")
    
    #open input file
    f = open(filename,"r");  

    seqs = []
    commands = []
    res_files = []

    #new fasta file is named by note after >
    r = tempfile.NamedTemporaryFile(
                    suffix=".fa", 
                    mode="w", 
                    delete=False,
                )

    n=0
    num_fragments = 0
    frag =""
    previou=""
    while(1):      
        #read char by char
        c = f.read(1)
        
        if(c == ">"):
            while(1):
                tmp = f.read(1)
                if tmp == "\n":
                    break
            frag =""
            previou=""
            continue;           
        
        #if c is new line ignore
        if(c == "\n"):
            continue
        #if is end of file
        #combine with previous fragmentation
        #and reduce to required length    
        if(c == ""):
            if n == 0:
                raise ValueError("Fragment length can't be greater than sequence length");    
            else:
                if(len(frag) > overlap):    
                    last = previous + frag
                    out=">fragment" + str(n) + "\n" + last[-length:] + "\n"
                    r.write(out)
                break
        
        #if sequence is not nucleotide sequence then raise error
        #else new char is added to fragmention
        if c not in ["A","G","C","T","a","g","c","t","N"]:  
            raise ValueError("This sequence is not a nucleotide sequence");      
        else:    
            frag += c
        
        #when frag hits the required length
        if(len(frag) == length):            
            #output is printed in output file
            out=">fragment" + str(n) + "\n" + frag + "\n"
            sequence_length += len(frag)
            r.write(out)
            num_fragments += 1
            n = n + 1
            previous = frag
            if(overlap == 0):
                frag = "";            
            else:    
                frag = frag[-overlap:];    

    #primary = tempfile.NamedTemporaryFile(
    #                            suffix=".fasta",
    #                            mode="w",
    #                            delete=False,
    #                        )

    #now = datetime.now()

    #current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)

    #print(len(seqs))
    #for file in seqs:
    #    #print(file)
    #    with open(file, 'r') as filename:
    #        for line in filename:
    #            primary.write(line)

    r.close()
    f.close();    
    return seqs, n, sequence_length, r.name

