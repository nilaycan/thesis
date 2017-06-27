import os
import sys
import time
import math
import xlrd
from xlrd import open_workbook
import random

#width2height=2.0
area_density=0.05


def bgr(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (float(value)-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    bgr=[]
    bgr.append(b)
    bgr.append(g)
    bgr.append(r)
    return bgr


def write_xml_header(file):
    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    #file.write('<gexf xmlns="http://www.gephi.org/gexf" xmlns:viz="http://www.gephi.org/gexf/viz">\n')
    file.write('<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2" xmlns:viz="http://www.gexf.net/1.2draft/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd">\n')
    #file.write('<graph type="static">\n')
    file.write('  <meta lastmodifieddate="2014-01-30">\n')
    file.write('    <creator>Gephi 0.8.1</creator>\n')
    file.write('    <description></description>\n')
    file.write('  </meta>\n')
    file.write('  <graph defaultedgetype="directed" mode="static">\n')
    file.write('    <attributes class="node" mode="static">\n')
    file.write('      <attribute id="0" title="Type" type="string"/>\n')
    #file.write('      <attribute id="1" title="disease class" type="string"/>\n')
    file.write('      <attribute id="1" title="Remarks" type="string"/></attributes>\n')
    #file.write('<attributes class="node" type="static">\n')
    #file.write('<attribute id="0" title="type" type="string"/>\n')
    #file.write('<attribute id="1" title="disclass" type="string"/>\n')
    #file.write('<attribute id="2" title="Polygon" type="integer"/>\n')
    #file.write('</attributes>\n')
    file.write('    <nodes>\n')

def write_a_node(file,_node_id,_label,_att1,_att2,_pos,_col,_size):
    file.write('      <node id="'+_node_id+'" label="'+_label+'"\n>')
    file.write('        <attvalues>\n')

    #if _att1=="gene":
    #    att1="Mouse Gene"
    #if _att1=="humandisease":
    #    att1="Disease of Class: "+
    #    _att3="3"
    file.write('          <attvalue id="0" value="'+_att1+'"></attvalue>\n')
    file.write('          <attvalue id="1" value="'+_att2+'"></attvalue>\n')
    #file.write('          <attvalue id="2" value="'+_att3+'"></attvalue>\n')
    file.write('        </attvalues>\n')
    file.write('        <viz:position x="'+_pos[0]+'" y="'+_pos[1]+'" z="0.0"></viz:position>\n')
    file.write('        <viz:color b="'+_col[0]+'" g="'+_col[1]+'" r="'+_col[2]+'"></viz:color>\n')
    file.write('        <viz:size value="'+_size+'"></viz:size>\n')
    #file.write('<viz:shape value="triangle"/>\n')
    file.write('      </node>\n')
    #file.write('\n')

print "undirected graph generation human diseases to child affected names via genes"

#can: the name of the workbook, be caution about the format of the book
first_book_name="first_table_corrected_new.xls"
first_book = xlrd.open_workbook(first_book_name)
#can: the name of the active worksheet
ws=first_book.sheet_by_name("Sheet1")

#can:
#can: a python dictionary conneting the genes (as keys=) to the humandiseases (=as values)
#gene2humandis={}
humandis2gene={}
dis_class={}
#can: flag for the while loop to recognize end of the excel sheet
first_line=True
#can: the start row
current_row=1
gene2entrez={}
while first_line:
    try:
        current_entrezid=ws.cell(current_row,0).value
    except:
        first_line=False
    else:
        try:
            current_gene=ws.cell(current_row,1).value.strip()
        except:
            pass
        else:
            gene2entrez[current_gene]=current_entrezid
            current_humandis=ws.cell(current_row,3).value.strip()
            current_disclass=ws.cell(current_row,4).value
            dis_class[str(current_disclass)]=1.0
            #current_tuple=(current_humandis,current_disclass,current_row)
            current_tuple=(current_gene,current_disclass,current_row)
            #if current_gene not in gene2humandis.keys():
            #    gene2humandis[current_gene]=[]
            #gene2humandis[current_gene].append(current_tuple)
            if current_humandis not in humandis2gene.keys():
                humandis2gene[current_humandis]=[]
            humandis2gene[current_humandis].append(current_tuple)
        current_row=current_row+1
for l in range(len(dis_class.keys())):
    dis_class[dis_class.keys()[l]]=float(l)


second_book_name="second_with_parenting.xlsx"
second_book = xlrd.open_workbook(second_book_name)
ws=second_book.sheet_by_name("DENE")

gene2affected={}
mp2id={}
second_line=True
prev_row=current_row
current_row=1
while second_line:
    try:
        current_mp=ws.cell(current_row,0).value
    except:
        second_line=False
    else:
        try:
            current_gene=ws.cell(current_row,2).value.strip()
        except:
            pass
        else:
            current_affected=ws.cell(current_row,1).value
            #current_parent1_mp=str(ws.cell(current_row,3).value)
            #current_parent1_affected=str(ws.cell(current_row,4).value)
            #current_parent2_affected="noparent"
            #try:
            #    current_parent2_mp=str(ws.cell(current_row,5).value)
            #except:
            #    current_parent2_mp="noparent"
            #else:
            #current_parent2_affected=str(ws.cell(current_row,6).value)

            #affected_tuple=(current_affected,prev_row+current_row,current_parent1_mp,current_parent1_affected,current_parent2_mp,current_parent2_affected)
            affected_tuple=(current_mp,current_affected)#,current_parent1_mp,current_parent1_affected,current_parent2_mp,current_parent2_affected)

            if current_gene not in gene2affected.keys():
                gene2affected[current_gene]=[]
            gene2affected[current_gene].append(affected_tuple)
            mp2id[current_mp]=prev_row+current_row
            current_row=current_row+1


gene2geneId={}
prev_row=max(mp2id.values())+1
current_row=1
for gene in gene2affected.keys():
    gene2geneId[gene]=prev_row+current_row
    current_row=current_row+1



no_notaffected_genes=0
max_radius=0
max_disease="some"
total_area=0.0
for gene_tuple_array in humandis2gene.values():
    for gene_tuple in gene_tuple_array:
        current_gene,current_disclass,current_row=gene_tuple
        current_gene,current_disclass,current_row=str(current_gene),str(current_disclass),str(current_row)
        #print current_gene,gene_tuple
        try:
            x=len(gene2affected[current_gene])
        except:
            no_notaffected_genes=no_notaffected_genes+1
        else:
            #if max_radius<x:
            #    max_radius=x
            #    for humandis in gene2humandis[gene]:
            #        max_disease, dummy1, dummy2=humandis
            total_area=total_area+float(x)*float(x)*3.14


#print "the maximum radius and the corresponding disease (number of affected connected to disease) is: "+str(max_radius)+" of "+max_disease
print "total area has been found to be: "+ str(total_area)


#print no_notaffected_genes
#compute heigth
r=math.sqrt(total_area/area_density/3.14)
print "the maximum radius of the window has been found to be "+str(r)

outfile=open("dis2affected.gexf","w")
write_xml_header(outfile)
debugfile=open("debugfile.log","w")
nodedic={}
missing=[]

for humandisease in humandis2gene.keys():
    prev_missing_length=len(missing)
    current_size=0.0
    current_gene_list = []
    for gene_tuple in humandis2gene[humandisease]:
        current_gene,current_disclass,current_row=gene_tuple
        current_gene_list.append(current_gene)
        try:
            current_size=current_size+len(gene2affected[current_gene])
        except:
            missing.append(current_gene)
    current_size=str(current_size)
    first_gene_tuple=humandis2gene[humandisease][0]
    current_gene,current_disclass,current_row=first_gene_tuple
    current_gene, current_att2, current_node_id=str(current_gene),str(current_disclass),str(current_row)
    current_label="Disorder: "+humandisease
    current_att1="Disorder Class: "+current_disclass
    current_att2="# of Mouse Genes: "+str(len(humandis2gene[humandisease]))+" AND "+str(len(missing)-prev_missing_length)+" do / does not have MP Id on Jax Database"+" . "+"Genes are " + ', '.join(current_gene_list)
    #angle=random.uniform(-3.14*2,3.14*2)
    #radius=random.uniform(0,r)
    #current_pos=str(radius*math.cos(angle)),str(radius*math.sin(angle))
    #current_col=bgr(0,len(dis_class.keys()),dis_class[current_att2])
    #current_col[0],current_col[1],current_col[2]=str(current_col[0]),str(current_col[1]),str(current_col[2])
    seperator="**##"
    writenodestring=current_node_id+seperator+current_label+seperator+current_att1+seperator+current_att2+seperator+current_size
    nodedic[current_node_id+seperator+current_label]=writenodestring


print "Total # of nodes appended: "+str(len(nodedic.keys()))
print "# of nodes without MP Id appended: "+str(len(missing))
for k in missing:
    debugfile.write(k+"\n")



from collections import Counter
from itertools import chain

def rowToPairs(sheet, row):
    """covert a sheet row to (affected_system, disease) pairs"""
    affected_system = sheet.cell(row, 1).value.strip()
    diseases = [d.strip() for d in sheet.cell(row, 3).value.split(',')]
    aff_sys_disease_pairs = [(affected_system, disease) for disease in diseases]
    return aff_sys_disease_pairs

def sheet_to_pairs(sheet):
    """convert the sheet to (affected_system, disease) pairs iterable"""
    return (rowToPairs(sheet, row) for row in range(0, sheet.nrows))

def count_affected_in_sheet(sheet):
    unique_pairs = set(chain.from_iterable(sheet_to_pairs(sheet)))
    return Counter(aff_sys for (aff_sys, disease) in unique_pairs)

# doc = open_workbook('second_disease_added.xlsx').sheet_by_index(0)

counter = count_affected_in_sheet(ws)


for humandisease in humandis2gene.keys():
    for gene_tuple in humandis2gene[humandisease]:
        gene,current_disclass,current_row=gene_tuple
        try:
            dummy=len(gene2affected[gene])
        except:
            pass
        else:
            for affected in gene2affected[gene]:
                #current_label, current_node_id,mp1,affected1,mp2,affected2=affected
                current_mp,current_affected=affected
                # current_size=str(50.0)
                current_size = str(counter.get(current_affected))
                #current_att1="Child affected system"
                current_att1="Affected system"
                current_att2=current_affected
                angle=random.uniform(-3.14*2,3.14*2)
                radius=random.uniform(0,r)
                current_pos=str(radius*math.cos(angle)),str(radius*math.sin(angle))
                current_col=str(68),str(68),str(238)
                seperator="**##"
                current_target_node_id=str(mp2id[current_mp])
                current_affected=current_att2
                writenodestring=current_target_node_id+seperator+current_affected+seperator+current_att1+seperator+current_att2+seperator+current_size
                nodedic[current_target_node_id+seperator+current_mp]=writenodestring
                '''
                try:
                    current_parent1_target_node_id=str(mp2id[mp1])
                except:
                    pass
                else:
                    angle=random.uniform(-3.14*2,3.14*2)
                    radius=random.uniform(0,r)
                    current_pos=str(radius*math.cos(angle)),str(radius*math.sin(angle))
                    current_col=str(68),str(68),str(238)
                    seperator="**##"
                    current_att1="Parent affected system"
                    current_att2=affected1
                    mp1="Parent Affected System1: "+mp1.strip('\"')
                    writenodestring=current_parent1_target_node_id+seperator+mp1+seperator+current_att1+seperator+current_att2+seperator+current_size
                    nodedic[current_parent1_target_node_id+seperator+mp1]=writenodestring
                    #write_a_node(outfile,current_parent1_target_node_id,mp1,current_att1,current_att2,current_pos,current_col,current_size)
                if mp2!="noparent":
                    try:
                        current_parent2_target_node_id=str(mp2id[mp2])
                    except:
                        pass
                    else:
                        angle=random.uniform(-3.14*2,3.14*2)
                        radius=random.uniform(0,r)
                        current_pos=str(radius*math.cos(angle)),str(radius*math.sin(angle))
                        current_col=str(68),str(68),str(238)
                        seperator="**##"
                        current_att1="Parent affected system"
                        current_att2=affected2
                        mp2="Parent Affected System2: "+mp2.strip('\"')
                        writenodestring=current_parent2_target_node_id+seperator+mp2+seperator+current_att1+seperator+current_att2+seperator+current_size
                        nodedic[current_parent2_target_node_id+seperator+mp2]=writenodestring
                        #write_a_node(outfile,current_parent2_target_node_id,mp2,current_att1,current_att2,current_pos,current_col,current_size)

                '''
#beneath is outcommented on purpose, since the genes will not be considered as nodes for this version
'''
for gene in gene2affected.keys():
    current_label="Mouse knock-out Gene: "+gene

    current_node_id=str(gene2geneId[gene])
    current_att1="Mouse knock-out Gene"
    try:
        current_att2="Entrez Id: "+str(int(gene2entrez[gene]))
    except:
        current_att2="Entrez Id missing"
    #angle=random.uniform(-3.14*2,3.14*2)
    #radius=random.uniform(0,r)
    #current_pos=str(radius*math.cos(angle)),str(radius*math.sin(angle))
    #current_col=str(168),str(68),str(238)
    seperator="**##"
    current_size=str(len(gene2affected[gene]))
    writenodestring=current_node_id+seperator+current_label+seperator+current_att1+seperator+current_att2+seperator+current_size
    nodedic[gene+seperator+current_label]=writenodestring
'''

for n in sorted(nodedic.keys()):
    seperator="**##"
    current_node_string=nodedic[n]
    current_node_id=current_node_string.split(seperator)[0]
    current_label=current_node_string.split(seperator)[1]
    current_att1=current_node_string.split(seperator)[2]
    current_att2=current_node_string.split(seperator)[3]
    current_size=current_node_string.split(seperator)[4]
    angle=random.uniform(-3.14*2,3.14*2)
    radius=random.uniform(0,r)
    current_pos=str(radius*math.cos(angle)),str(radius*math.sin(angle))
    if current_att1.startswith("Disease Class:")==True:
        current_disclass=current_att1.split("Disease Class: ")[1]
        current_col=bgr(0,len(dis_class.keys()),dis_class[current_disclass])
        current_col[0],current_col[1],current_col[2]=str(current_col[0]),str(current_col[1]),str(current_col[2])
    else:
        if current_att1=="Mouse knock-out Gene":
            current_col=str(9),str(9),str(9)
        else:
          current_col=str(68),str(68),str(238)
    write_a_node(outfile,current_node_id,current_label,current_att1,current_att2,current_pos,current_col,current_size)
outfile.write("    </nodes>\n")

edgedic={}
edge_counter=1
for humandisease in humandis2gene.keys():
    first_gene_tuple=humandis2gene[humandisease][0]
    first_gene,current_disclass,current_row=first_gene_tuple
    first_gene, current_att2, current_dis_source_node_id=str(first_gene),str(current_disclass),str(current_row)
    #above is only required for determining the current_dis_source_node_id
    for gene_tuple in humandis2gene[humandisease]:
        gene,current_disclass,current_row=gene_tuple
        try:
            dummy=len(gene2affected[gene])
        except:
            pass
        else:
            #beneath is outcommented for this version because the edges from the diseases to the genes are not desired for this case
            #current_gene_target_node_id=str(gene2geneId[gene])
            #current_edge_string='      <edge id="'+str(edge_counter)+'" source="'+current_dis_source_node_id+'" target="'+current_gene_target_node_id+'" label="'+gene+'">\n'
            #current_edge_string=current_edge_string+'        <attvalues></attvalues>\n      </edge>\n'
            #edge_counter=edge_counter+1
            #edgedic[current_edge_string]=1.0
            #current_source_node_id=current_gene_target_node_id
            for affected in gene2affected[gene]:
                current_mp,current_affected=affected
                current_mp,current_affected=affected=str(current_mp),str(current_affected)
                current_target_node_id=str(mp2id[current_mp])
                current_edge_string='      <edge id="'+str(edge_counter)+'" source="'+current_dis_source_node_id+'" target="'+current_target_node_id+'" label="'+gene+'">\n'
                current_edge_string=current_edge_string+'        <attvalues></attvalues>\n      </edge>\n'
                edge_counter=edge_counter+1
                edgedic[current_edge_string]=1.0
                #current_label, current_a_target_node_id,mp1,affected1,mp2,affected2=affected
                #current_label, current_a_target_node_id=str(current_label), str(current_a_target_node_id)
                #try:
                #    current_parent1_target_node_id=str(mp2id[mp1])
                #except:
                #    pass
                #else:
                #    current_edge_string='      <edge id="'+str(edge_counter)+'" source="'+current_dis_source_node_id+'" target="'+current_parent1_target_node_id+'" label="'+gene+'">\n'
                #    current_edge_string=current_edge_string+'        <attvalues></attvalues>\n      </edge>\n'
                #    edge_counter=edge_counter+1
                #    edgedic[current_edge_string]=1.0
                #if mp2!="noparent":
                #    try:
                #        current_parent2_target_node_id=str(mp2id[mp2])
                #    except:
                #        pass
                #    else:
                #        current_edge_string='      <edge id="'+str(edge_counter)+'" source="'+current_dis_source_node_id+'" target="'+current_parent2_target_node_id+'" label="'+gene+'">\n'
                #        current_edge_string=current_edge_string+'        <attvalues></attvalues>\n      </edge>\n'
                #        edge_counter=edge_counter+1
                #        edgedic[current_edge_string]=1.0


outfile.write("    <edges>\n")
for e in sorted(edgedic.keys()):
    outfile.write(e)
outfile.write('    </edges>\n')
outfile.write('  </graph>\n')
outfile.write('</gexf>\n')

print "finished"
