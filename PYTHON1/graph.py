
import os 
import sys
import time 
import math
import xlrd
from xlrd import open_workbook
try:
    import matplotlib.pyplot as plt
except:
    raise


import networkx as nx
from Tkinter import *

def buttonProcessingClick():
    listeSelected = listboxName.curselection()
    itemSelected = listeSelected[0]
    nameSelected = listboxName.get(itemSelected) 
    textGreeting = 'Computing the Ancestor Tree of the breed: ' + nameSelected
    labelText.config(text=textGreeting)
    compute_the_structure(str(nameSelected))
    
class BREED:
    def define_breed(self,_label,_parent_labels):
        self.label=_label
        self.parent_labels=_parent_labels
        self.immature=False
        self.ancestors={}
        self.ancestor_breeds={}
    def append_ancestor(self,_ancestor_level,_ancestor):
        if _ancestor_level not in self.ancestors.keys():
            self.ancestors[_ancestor_level]=[]
            self.ancestors[_ancestor_level].append(_ancestor)
        else:
            self.ancestors[_ancestor_level].append(_ancestor)
    def append_breed_of_ancestor(self,_ancestor_level,_ancestor_breeds):
        if _ancestor_level not in self.ancestor_breeds.keys():
            self.ancestor_breeds[_ancestor_level]=[]
            for i in range(len(_ancestor_breeds)):
                self.ancestor_breeds[_ancestor_level].append(_ancestor_breeds[i])
        else:
            for i in range(len(_ancestor_breeds)):
                self.ancestor_breeds[_ancestor_level].append(_ancestor_breeds[i])
            

class PARENT:
    def define_parent(self,_label):
        self.label=_label
        self.children_labels={}
        self.master_parent=False
        
    def append_children_partner(self,_child_label,_partner_labels):
        self.children_labels[_child_label]=_partner_labels

def compute_the_structure(example):
    debugfile=open("debugfile.log","w")
    for b in breeds.keys():
        if b==example:
            #print b
            olimpos_not_reached=True
            ancestor_level=1
            next_generation=[]
            next_generation.append(breeds[b].parent_labels)
            this_generation=[]
            this_generation.append(b)
            while olimpos_not_reached:
            
                godness_of_parents=[]
                over_next_generation=[]
                breeds[b].append_breed_of_ancestor(ancestor_level,this_generation) 
                this_generation=[]       
                for a in range(len(next_generation)):
                    
                    breeds[b].append_ancestor(ancestor_level,next_generation[a])    
                    
                    for g in next_generation[a]:
                        godness_of_parents.append(parents[g].master_parent)
                        if not parents[g].master_parent:
                            this_generation.append(g)
                            over_next_generation.append(breeds[g].parent_labels)
            
                
                if False in godness_of_parents:
                    pass
                else:
                    olimpos_not_reached=False
                next_generation=over_next_generation
                ancestor_level=ancestor_level+1
    
    for k in breeds[example].ancestors.keys():
        debugfile.write("breed of ancestor "+str(k)+": ("+str(len(breeds[example].ancestor_breeds[k]))+")"+str(breeds[example].ancestor_breeds[k])+"\n")
        debugfile.write("ancestor "+str(k)+": ("+str(len(breeds[example].ancestors[k]))+")"+str(breeds[example].ancestors[k])+"\n")
    
    
            
    debugfile.close()
        
    
    G=nx.Graph()
    
    all_nodes={}
    
    for a in breeds[example].ancestors.keys():
        for b in range(len(breeds[example].ancestor_breeds[a])):
                current_pairs=[]
                current_pairs.append(breeds[example].ancestor_breeds[a][b])
                for k in breeds[example].ancestors[a][b]:
                    current_pairs.append(k)
                        #print l
                #print current_pairs        
                for k in range(1,len(current_pairs)):
                    G.add_edge(current_pairs[0],current_pairs[k],key="ancestor",weight=0.6)
                    for l in range(1,len(current_pairs)):
                        G.add_edge(current_pairs[l],current_pairs[k],key="parent",weight=0.4)
                for p in current_pairs:
                        all_nodes[p]=1

    
    for n in all_nodes.keys():
            G.add_node(n)
    pos=nx.spring_layout(G,weight='weight',iterations=150)
    
    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
    elarge_labels=dict([((u,v,),d['key'])for u,v,d in G.edges(data=True) if d['weight'] >0.5])
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]
    esmall_labels=dict([((u,v,),d['key'])for u,v,d in G.edges(data=True) if d['weight'] <=0.5])
    #allnodes=[(u,v) for (u,v) in G.nodes()]
    
    nodes=[(u) for (u) in G.nodes()]
    breed_node=[(u) for (u) in G.nodes() if u==example]
    master_nodes=[(u) for (u) in G.nodes() if u in parents.keys() if parents[u].master_parent==True]
    
    
    nx.draw_networkx_edges(G,pos,edgelist=elarge,width=2,edge_color='r')
    
    nx.draw_networkx_edges(G,pos,edgelist=esmall,width=3,alpha=0.5,edge_color='b',style='dashed')

    
    nx.draw_networkx_nodes(G,pos,nodelist=nodes,node_size=250,node_color='w')
    nx.draw_networkx_nodes(G,pos,nodelist=breed_node,node_size=250,node_color='g')
    nx.draw_networkx_nodes(G,pos,nodelist=master_nodes,node_size=250,node_color='b')
    nx.draw_networkx_labels(G,pos,font_size=15,font_family='sans-serif')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=esmall_labels,font_size=10)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=elarge_labels,font_size=10)
    plt.axis('off')
    plt.savefig("weighted_graph.png") # save as png
    plt.show() # display
input_filename="parenting_modified.xlsx"
xl_workbook = xlrd.open_workbook(input_filename)
ws=xl_workbook.sheet_by_name("parenting")

current_row=1
breed_line=True
#parent_labels={}

parents={}
breeds={}
while breed_line:
    try:
        current_breed_label=ws.cell(current_row,0).value
    except:
        breed_line=False
    else:
        current_child_description=ws.cell(current_row,1).value
        current_parent_labels=[]
        for i in range(2,5):
           current_parent_label=ws.cell(current_row,i).value
           if current_parent_label!="NA":
                current_parent_labels.append(current_parent_label)
        current_breed=BREED()
        current_breed.define_breed(current_breed_label,current_parent_labels)
        breeds[current_breed_label]=current_breed
        for p in current_parent_labels:
            if p not in parents.keys():
                current_parent=PARENT()
                current_parent.define_parent(p)
                current_parent.append_children_partner(current_breed_label,current_parent_labels)
                parents[p]=current_parent
            else:
                parents[p].append_children_partner(current_breed_label,current_parent_labels)
        current_row=current_row+1
    
numberofmasterparents=0
for p in parents.keys():
        if p not in breeds.keys():
            parents[p].master_parent=True
            numberofmasterparents=numberofmasterparents+1
        elif p in parents[p].children_labels.keys():
            parents[p].master_parent=True
            numberofmasterparents=numberofmasterparents+1
        
# Generation of Windows
tkWindow = Tk()
tkWindow.title('JAX INFORMATICS PHENOTYPING TREE')
tkWindow.geometry('600x700')
# Frame Listbox
frameListbox = Frame(master=tkWindow, bg='#FBD975')
frameListbox.place(x=5, y=5, width=800, height=800)
# Frame processing
frameOutput = Frame(master=tkWindow, bg='#D5E88F')
frameOutput.place(x=5, y=505, width=800, height=100)
# Frame processing
frameProcessing = Frame(master=tkWindow, bg='#FBD975')
frameProcessing.place(x=5, y=535, width=500, height=250)
# Controllvariable
text = StringVar()
# Listbox
listboxName = Listbox(master=frameListbox, selectmode='browse')
for b in sorted(breeds.keys()):
    listboxName.insert('end', b)

listboxName.place(x=75, y=5, width=300, height=500)
# Label Text
labelText = Label(master=frameOutput, bg='white')
labelText.place(x=75, y=5, width=500, height=20)
# Button
buttonProcess = Button(master=frameProcessing, text='Show Ancestors of Selected Phenotype', command=buttonProcessingClick)
buttonProcess.place(x=75, y=5, width=500, height=20)
# Activate the Windows
tkWindow.mainloop()
        
