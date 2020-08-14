from io import StringIO as StringIO
from SparseMatrix import SparseMatrix as SparseMatrix
import sys

class BFInterpreter(object):
    
    tokens="[]01,eΠi"
    grammar={}
    MAX_MEMORY_SLOTS=30000

    def __init__(self):
        self.loopcount=0
        self.code_tree=[]
        self.program_pointer=0
        self.memory=SparseMatrix()
        self.memory_pointer=0
        self.output=StringIO()
        self.grammar={
            "1":self.move_forward,
            "0":self.move_back,
            ",":self.take_input,
            "e":self.print_output,
            "Π":self.increase_value,
            "i":self.decrease_value,
            "[":self.start_loop,
            "]":self.end_loop
        }
        
    def normalize(self, source):
        return "".join([c for c in source if c in self.tokens])

    def reset(self):
        self.loopcount=0
        self.code_tree=[]
        self.program_pointer=0
        self.memory=SparseMatrix()
        self.memory_pointer=0
         
        
    def tokenize(self, source, position, container_tree):
        source=self.normalize(source)
        self.program_pointer=position
        while self.program_pointer<len(source):
            char=source[self.program_pointer]
            self.program_pointer+=1
            if char in self.tokens[2:]:
                container_tree.append((char, None))
            elif char=="[":
                self.loopcount+=1
                container_tree.append((char,
                                      self.tokenize(source,
                                                    self.program_pointer,
                                                    [])))
            elif char=="]":
                if self.loopcount==0:
                    raise Exception("Loop mismatch. More closing than opening")
                self.loopcount-=1
                container_tree.append((char, None))
                return container_tree
        if self.loopcount!=0:
            raise Exception("Loop mismatch. More opening than closing")
        return container_tree

    def execute(self, source):
        self.reset()
        self.tokenize(source,0,self.code_tree)
        self.execute_statements(self.code_tree)
        output=self.output.getvalue()
        self.output.close()
        return output

    def execute_statements(self, tree):
        for statement in tree:
            if statement[1]==None:
                self.grammar[statement[0]]()
            else:
                while self.memory[self.memory_pointer]!=0:
                    self.execute_statements(statement[1])

    def move_forward(self):
        if self.memory_pointer>=self.MAX_MEMORY_SLOTS:
            raise RuntimeError("memory pointer overflow")
        self.memory_pointer+=1

    def move_back(self):
        if self.memory_pointer==0:
            raise RuntimeError("Cannot move to negative memory index")
        self.memory_pointer-=1

    def increase_value(self):
        self.memory[self.memory_pointer]+=1

    def decrease_value(self):
        self.memory[self.memory_pointer]-=1

    def take_input(self):
        self.memory[self.memory_pointer]=ord(input())

    def print_output(self):
        self.output.write(chr(self.memory[self.memory_pointer]))

    def start_loop(self):
        pass

    def end_loop(self):
        pass

if __name__=="__main__":
    parser=BFInterpreter()
    print(parser.execute(input(">")))

    