# -* coding: utf-8 -*-

#################################################################################
# This file is part of EVALLIES.                                                #
#                                                                               #
# EVALLIES is a python package for lifelong learning speaker diarization.       #
# Home page: https://git-lium.univ-lemans.fr/Larcher/evallies                   #
#                                                                               #
# EVALLIES is free software: you can redistribute it and/or modify              #
# it under the terms of the GNU LLesser General Public License as               #
# published by the Free Software Foundation, either version 3 of the License,   #
# or (at your option) any later version.                                        #
#                                                                               #
# EVALLIES is distributed in the hope that it will be useful,                   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 #
# GNU Lesser General Public License for more details.                           #
#                                                                               #
# You should have received a copy of the GNU Lesser General Public License      #
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.              #
#                                                                               #
#################################################################################
"""
Copyright 2020-2021 Anthony Larcher, Meysam Shamsi & Yevhenii Propkopalo

    :mod:`lium_baseline.interactive`

"""

import copy
import numpy
import pandas
import scipy
import os

from s4d.clustering.hac_utils import scores2distance
from scipy.cluster import hierarchy as hac
from scipy.spatial.distance import squareform

from .utils import s4d_to_allies
from ..user_simulation import MessageToUser
from ..user_simulation import Request
from s4d.clustering.hac_iv import information
from ..der_single import *

from s4d.diar import Diar
from s4d.scoring import DER
import json

def allies_write_diar(current_diar, filename):
    """

    """
    cdiar = copy.deepcopy(current_diar)
    for idx, seg in enumerate(cdiar):
        cdiar.segments[idx]['start'] = float(seg['start']) / 100.
        cdiar.segments[idx]['stop'] = float(seg['stop']) / 100.


    cdiar.sort(['show', 'start'])
    with open(filename, 'w', encoding="utf8") as fic:
        for line in Diar.to_string_seg(cdiar, time_float=True):
            fic.write(line)


def get_node_spkeakers(node_spk,number_cluster,link):
    """
    get a node and return the all sub cluster id

    :param node_spk: row of the linkage matrix
    :param number_cluster: number in link matrix
    :param link: linkage matrix
    :return: cluster_list: a list of clusters id in link
    """

    if node_spk >= number_cluster:
        cluster_list=get_node_spkeakers(link[int(node_spk-number_cluster)][0],number_cluster,link)+get_node_spkeakers(link[int(node_spk-number_cluster)][1],number_cluster,link)
    else:
        cluster_list=[int(node_spk)]
    return cluster_list


def ask_question(node_to_check, scores,scores_init, current_diar,current_vec, user, file_info,link,selection_criteria="longest"):
    """


    :param node_to_check: row of the linkage matrix to check with the user
    :param scores: the corresponding score object
    :param current_diar: the current diarization
    :param user: the user simulation
    :param link: linkage matrix
    :return: is_same_speaker: a boolean, True if the clustering at this node is approved by the user
    """
 
    # get one segment for each side of the node (if it's a leaf, it's easy, if qe already have a cluster we need to
    # list all segments in this cluster and then find the most central segment in the cluster from the score matrix
    # HERE WE NEED TO FIND TWO indices in the scores.scoremat matrix
    number_cluster=len(scores.modelset)
    node_list1=get_node_spkeakers(node_to_check[0],number_cluster,link)
    node_list2=get_node_spkeakers(node_to_check[1],number_cluster,link)
    #convert node_list to spk_list
    #import pdb
    #pdb.set_trace()     

    spk_list1=[]
    for n in node_list1:
        spk_list1.append(scores.modelset[n])
    spk_list2=[]
    for n in node_list2:
        spk_list2.append(scores.modelset[n])
    
    # From the indices, get the borders of the segments in the Diar object
    seg1=[0,0]
    seg2=[0,0]
    
    if selection_criteria == "longest":
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list1:
                if current_diar[i][4]-current_diar[i][3]>seg1[1]-seg1[0]:
                    seg1[1]=current_diar[i][4]
                    seg1[0]=current_diar[i][3]
            if current_diar[i][1] in spk_list2:
                if current_diar[i][4]-current_diar[i][3]>seg2[1]-seg2[0]:
                    seg2[1]=current_diar[i][4]
                    seg2[0]=current_diar[i][3]
    
    elif selection_criteria == "cluster_center":
        segs_cluster1={}
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list1:
                segs_cluster1[i]=current_vec.stat1[i]
        cluster1_center=numpy.mean(list(segs_cluster1.values()), axis=0)
        min_dis=float('inf')
        for seg in segs_cluster1:
            dis=scipy.spatial.distance.euclidean(segs_cluster1[seg],cluster1_center)
            if dis<min_dis:
                min_dis=dis
                seg1=[current_diar[int(seg)][3],current_diar[int(seg)][4]]
        segs_cluster2={}
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list2:
                segs_cluster2[i]=current_vec.stat1[i]
        cluster2_center=numpy.mean(list(segs_cluster2.values()), axis=0)
        min_dis=float('inf')
        for seg in segs_cluster2:
            dis=scipy.spatial.distance.euclidean(segs_cluster2[seg],cluster2_center)
            if dis<min_dis:
                min_dis=dis
                seg2=[current_diar[int(seg)][3],current_diar[int(seg)][4]]
                
    elif selection_criteria == "cluster_center_plda":
        
        segs_cluster1=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list1:
                segs_cluster1.append(i)
        cluster1_similaritySum=[]
        for i in range(len(segs_cluster1)):
            cluster1_similaritySum.append(0)
            for j in range(len(scores_init.scoremat[i])):
                if j in segs_cluster1 and j!=i:
                     cluster1_similaritySum[i]+=scores_init.scoremat[i][j]
                        
        center1_seg=segs_cluster1[cluster1_similaritySum.index(max(cluster1_similaritySum))]
        seg1=[current_diar[int(center1_seg)][3],current_diar[int(center1_seg)][4]]        
        
        segs_cluster2=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list2:
                segs_cluster2.append(i)
        cluster2_similaritySum=[]
        for i in range(len(segs_cluster2)):
            cluster2_similaritySum.append(0)
            for j in range(len(scores_init.scoremat[i])):
                if j in segs_cluster2 and j!=i:
                     cluster2_similaritySum[i]+=scores_init.scoremat[i][j]
                        
        center2_seg=segs_cluster2[cluster2_similaritySum.index(max(cluster2_similaritySum))]
        seg2=[current_diar[int(center2_seg)][3],current_diar[int(center2_seg)][4]]
        
    elif selection_criteria == "random":
        import random
        segs_cluster1=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list1:
                segs_cluster1.append(i)
        random_seg=random.choice(segs_cluster1)
        seg1=[current_diar[int(random_seg)][3],current_diar[int(random_seg)][4]]
        segs_cluster2=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list2:
                segs_cluster2.append(i)
        random_seg=random.choice(segs_cluster2)
        seg2=[current_diar[int(random_seg)][3],current_diar[int(random_seg)][4]]


        
    elif selection_criteria == "max":
        
        segs_cluster1=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list1:
                segs_cluster1.append(i)
        
        segs_cluster2=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list2:
                segs_cluster2.append(i)
                  
        min_similardis=float('inf')
        for i in segs_cluster1:
            for j in segs_cluster2:
                if scores_init.scoremat[i][j]< min_similardis:
                    min_similardis=scores_init.scoremat[i][j]
                    seg1=[current_diar[i][3],current_diar[i][4]]
                    seg2=[current_diar[j][3],current_diar[j][4]]
                             
        
    elif selection_criteria == "min":
        segs_cluster1=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list1:
                segs_cluster1.append(i)
        
        segs_cluster2=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list2:
                segs_cluster2.append(i)
                  
        max_similardis=-float('inf')
        for i in segs_cluster1:
            for j in segs_cluster2:
                if scores_init.scoremat[i][j]> max_similardis:
                    max_similardis=scores_init.scoremat[i][j]
                    seg1=[current_diar[i][3],current_diar[i][4]]
                    seg2=[current_diar[j][3],current_diar[j][4]]

    elif selection_criteria == "max_noBICHAC":

        segs_cluster1=node_list1
        segs_cluster2=node_list2
        
        #import pdb
        #pdb.set_trace() 
        max_similardis=-float('inf')
        for i in segs_cluster1:
            for j in segs_cluster2:
                if scores_init.scoremat[i][j]> max_similardis:
                    max_similardis=scores_init.scoremat[i][j]
                    seg1=[current_diar[i][3],current_diar[i][4]]
                    seg2=[current_diar[j][3],current_diar[j][4]]


    elif selection_criteria == "ideal":
        segs_cluster1=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list1:
                segs_cluster1.append(i)
        segs_cluster2=[]
        for i in range(len(current_diar)):
            if current_diar[i][1] in spk_list2:
                segs_cluster2.append(i)
        #import pdb
        #pdb.set_trace()  
        root  ='/lium/buster1/prokopalo/EXPE/icassp_hal_baseline/data/ALLIES/eval'
        basename = current_diar[0]['show']
        ref = Diar.read_mdtm(root+'/mdtm/'+basename+'.mdtm')          
        
        if len(ref)!=len(current_diar):
            print ("Error ! number of segment in diar are not same ..."+current_diar[0]['show'])
        dict1 = {}      
        for indx in segs_cluster1:
            if len(ref)>indx:
                if ref[indx]['cluster'] in dict1.keys():
                    dict1[ref[indx]['cluster']]+=(ref[indx]['stop']-ref[indx]['start'])
                else:
                    dict1[ref[indx]['cluster']]=(ref[indx]['stop']-ref[indx]['start'])

        dict2 = {}
        for indx in segs_cluster2:
            if len(ref)>indx:
                if ref[indx]['cluster'] in dict2.keys():
                    dict2[ref[indx]['cluster']]+=(ref[indx]['stop']-ref[indx]['start'])
                else:
                    dict2[ref[indx]['cluster']]=(ref[indx]['stop']-ref[indx]['start'])

        if max(dict2, key = dict2.get) == max(dict1, key = dict1.get):
            return True , 0
        else:
            return False , 0

        #import pdb
        #pdb.set_trace()    

    # For each segments, get the center of the segment in seconds
    t1 =numpy.mean(seg1)/100
    t2 =numpy.mean(seg2)/100
    
    
    # Ask the question to the user
    message_to_user = MessageToUser(file_info,
                                    s4d_to_allies(current_diar),
                                    Request('same', t1, t2))
    hal, answer = user.validate(message_to_user)
    return answer.answer,hal


def check_std_change(node_to_check, scores, current_diar,current_vec,link,question,active=False):
    
    if not active:
        return True
    
    number_cluster=len(scores.modelset)
    node_list1=get_node_spkeakers(node_to_check[0],number_cluster,link)
    node_list2=get_node_spkeakers(node_to_check[1],number_cluster,link)

    spk_list1=[]
    for n in node_list1:
        spk_list1.append(scores.modelset[n])
    spk_list2=[]
    for n in node_list2:
        spk_list2.append(scores.modelset[n])
        
    segs_cluster_mrg={}
    for i in range(len(current_diar)):
        if current_diar[i][1] in spk_list1 or current_diar[i][1] in spk_list2:
            segs_cluster_mrg[i]=current_vec.stat1[i]
    mrg_situation=numpy.mean(numpy.std(list(segs_cluster_mrg.values()), axis=0))

    segs_cluster1_sep={}
    for i in range(len(current_diar)):
        if current_diar[i][1] in spk_list1:
            segs_cluster1_sep[i]=current_vec.stat1[i]
    std_sep1=numpy.std(list(segs_cluster1_sep.values()), axis=0)
    segs_cluster2_sep={}
    for i in range(len(current_diar)):
        if current_diar[i][1] in spk_list2:
            segs_cluster2_sep[i]=current_vec.stat1[i]
    std_sep2=numpy.std(list(segs_cluster2_sep.values()), axis=0)
    sep_situation=numpy.mean(numpy.mean([std_sep1,std_sep2], axis=0))
    
    if question =="separate":
        question_quality= sep_situation<mrg_situation
    elif question =="merge":
        question_quality= sep_situation>mrg_situation
    else:
        print("Question type is not valid ...")
        question_quality=True
        
    return question_quality


def check_der(current_diar,cluster_list,link,root='/lium/buster1/mshamsi/expe/icassp_hal_baseline/data/ALLIES/eval'):
    
    
    cluster_dict = dict()
    merge = list()
    i = 0

    while i < len(link):
#         print("change ... ",link[i])
        # the cluster_list of the 2 clusters
        if len(cluster_list)>int(link[i][0]) and len(cluster_list)>int(link[i][1]): 
            c0 = cluster_list[int(link[i][0])]
            c1 = cluster_list[int(link[i][1])]
            information(merge, i, c0, c1, link[i][2])
            if c1 in cluster_dict:
                # c0 is put in c1, and c1 is not empty
                cluster_dict[c1].append(c0)
            else:
                cluster_dict[c1] = [c0]
            if c0 in cluster_dict:
                # remove c0 key
                cluster_dict[c1] += cluster_dict[c0]
                cluster_dict.pop(c0)
            # add the speaker of the new cluster
            cluster_list.append(c1)
            current_diar.rename('cluster', [c0], c1)
        i += 1
    
    basename = current_diar[0]['show']
    ref = load_mdtm(root+'/mdtm/'+basename+'.mdtm')
    uem = load_uem (root+'/uem/'+basename+'.uem')
    
    if not os.path.isdir(f"./tmp/diar_tmp/"):
        os.makedirs(f"./tmp/diar_tmp/")
    
    allies_write_diar(current_diar, f"./tmp/diar_tmp/hyp_{basename}.mdtm")
    
    hyp = load_mdtm(f"./tmp/diar_tmp/hyp_{basename}.mdtm")
    
    (der, time, map)= compute_der(ref, hyp, uem, {}, 0.250)
    
    return der, time


def active_learning_tree(current_diar,
                         initial_diar,
                         current_vec,
                         scores,
                         scores_init,
                         threshold,
                         user,
                         file_info,
                         clustering_method="complete",
                         selection_method="longest",
                         no_more_clustering = False,
                         no_more_separation = False,
                         process_all_nodes = True,
                         conditional_questioning=False):
    """

    :param current_diar: the segmentation that comes out from the automatic pass
    :param current_vec: StatServer of  vectors not YET normalized
    :param scores: Scores object with symetric matrix of PLDA scores inside
    :param threshold: the clustering threshold
    :param user: user simulation developed in the ALLIES package
    :param clustering_method: complete
    :param selection_method: The method of segment selection for asking quastion from human (could be different for seperation and clustering)
    :param process_all_node: The new stopping creteria for processing whole tree. It changes the limitation of having one line as threshold and lets to consider all branches
    :param conditional_questioning: Usage of reducing std of cluster as condition for asking question
    :return:
    """
#     import pdb
#     pdb.set_trace()
    
    # Perform HAC on the vectors (that shoiuld produce exactly the same segmentation as the one in current diar
    ldiar = copy.deepcopy(current_diar)
    init_diar=copy.deepcopy(initial_diar)
    lscores = copy.deepcopy(scores)
    # get the triangular part of the distances
    distances, th = scores2distance(lscores, threshold)
    distance_sym = squareform(distances)
    
    # t = -1.0 * threshold - min
    # cluster the data
    link = hac.linkage(distance_sym, method=clustering_method)
    
    #code for creation beautiful grafs
    #import pdb
    #pdb.set_trace()
    diar_= copy.deepcopy(initial_diar)
    if False:
        lscores = copy.deepcopy(scores_init)
        scores = copy.deepcopy(scores_init)
        distances, th = scores2distance(lscores, threshold)
        distance_sym = squareform(distances)
        link = hac.linkage(distance_sym, method=clustering_method)
        for i in range (len(diar_)):
            diar_[i]['cluster']=str(i)


    tmp = numpy.zeros((link.shape[0], link.shape[1] + 2))
    tmp[:, :-2] = link
    tmp[:, -2] = link[:, 2] - th
    tmp[:, -1] = numpy.abs(link[:, 2] - th)
    # tmp[:,-2] permet de savoir si on est au dessus du seuil (positif) ou en dessous (négatif)
    # tmp[:, -1] indique la distance au seuil en valeur absolue

    # On trie les regroupements par ordre de proximité au seuil
    # plus proche en premiere ligne
    links_to_check = tmp[numpy.argsort(tmp[:, -1])]

    # On récupère la liste des fusions à faire d'abord.
    final_links = []
    for l in link:
        if l[2] < th:
            final_links.append(l)

    # Maintenant on analyse noeud par noeud du plus proche au plus lointain du seuil de fusion
    # et on gère les deux directions
#     no_more_clustering = False
#     no_more_separation = False
    
    if process_all_nodes:
        separated_list =[]
        separation_list = [] 
        clustering_list = []
    number_cluster = len(scores.scoremat)
    complete_list = list(scores.modelset)
    
    #log the DER
    link_tmp = copy.deepcopy(final_links)
    new_diar_tmp = copy.deepcopy(init_diar)
    cluster_list_tmp = scores.modelset.tolist()
    der, time = check_der(new_diar_tmp,cluster_list_tmp,link_tmp)
    print("Initial DER : ",der)
    
    der_track={"time":time,"der_log":[der],"correction":["initial"],"numQ_clustering":0,"numQ_seperation":0}
    
    for ltc in links_to_check:
        
        # Si on cesse dans les deux directions on sort de la boucle de correction
        if no_more_clustering and no_more_separation:
            break

        elif ltc[-2] < 0:  # On est en dessous du seuil, on a déjà regroupé
            # demande si on sépare: trouve les numéros de deux segments
            # représentatifs des deux cluster déjà regroupés et pose la question
            skip = False
            if process_all_nodes:
                if no_more_separation or set(get_node_spkeakers(ltc[0],number_cluster,link)+get_node_spkeakers(ltc[0],number_cluster,link)).issubset(set(separation_list)) :  # On laisse ensemble
                    skip = True
            else: 
                if no_more_separation:
                    skip = True
            if skip or not check_std_change(ltc, scores, init_diar,current_vec,link,"separate",active=conditional_questioning):
                pass
            else:  # On sépare, concretement on retire la fusion de la liste final_link
                is_same_speaker,_ = ask_question(ltc, scores,scores_init, init_diar,current_vec, user, file_info,link,selection_criteria=selection_method)
                der_track["numQ_seperation"]+=1
                if is_same_speaker:
                    der_track["der_log"].append(der)
                    der_track["correction"].append("None")
                    
                        
#                     print("stop separation ...")
                    if process_all_nodes:
                        separation_list+= get_node_spkeakers(ltc[0],number_cluster,link)
                        separation_list+= get_node_spkeakers(ltc[1],number_cluster,link)
                        if set(complete_list).issubset(set(separation_list)):
                            no_more_separation = True
                    else:
                        no_more_separation = True
    
                       
                else:
                    if process_all_nodes:
                        separated_list+= get_node_spkeakers(ltc[0],number_cluster,link)
                        separated_list+= get_node_spkeakers(ltc[1],number_cluster,link)
#                     print("separate cluster ...")
                    for ii, fl in enumerate(final_links):
                        if numpy.array_equal(fl, ltc[:4]):
                            _ = final_links.pop(ii)
                    link_tmp = copy.deepcopy(final_links)
                    new_diar_tmp = copy.deepcopy(init_diar)
                    cluster_list_tmp = scores.modelset.tolist()
                    der, time = check_der(new_diar_tmp,cluster_list_tmp,link_tmp)
                    der_track["der_log"].append(der)
                    der_track["correction"].append("separate")
                    print("Separate a cluster. new DER : ",der)
                    
                         

        elif ltc[-2] > 0:  # On est au dessous du seuil, on n'a pas encore regroupé
            skip = False
            if process_all_nodes:
                if no_more_clustering or set(get_node_spkeakers(ltc[0],number_cluster,link)+get_node_spkeakers(ltc[0],number_cluster,link)).issubset(set(clustering_list)) :
                    skip = True
                if not set(get_node_spkeakers(ltc[0],number_cluster,link)+get_node_spkeakers(ltc[0],number_cluster,link)).isdisjoint(set(separated_list)):
                    skip = True 
            else:
                if no_more_clustering:
                    skip = True
            if skip or not check_std_change(ltc, scores, init_diar,current_vec,link,"merge",active=conditional_questioning):
                pass

            else:
                is_same_speaker,_ = ask_question(ltc, scores,scores_init, init_diar,current_vec, user, file_info,link,selection_criteria=selection_method)  # true
                der_track["numQ_clustering"]+=1
                if is_same_speaker:  # On fait un nouveau regroupement
#                     print("group clusters ...")
                    final_links.append(ltc[:4])
                    link_tmp = copy.deepcopy(final_links)
                    new_diar_tmp = copy.deepcopy(init_diar)
                    cluster_list_tmp = scores.modelset.tolist()
                    der, time = check_der(new_diar_tmp,cluster_list_tmp,link_tmp)
                    der_track["der_log"].append(der)
                    der_track["correction"].append("cluster")
                    print("Group two clusters. new DER : ",der)
                    
                    
                else:
                    der_track["der_log"].append(der)
                    der_track["correction"].append("None")
                    
                    # On arrête de chercher de ce côté
#                     print("stop grouping ...")
                    if process_all_nodes:
                        clustering_list+= get_node_spkeakers(ltc[0],number_cluster,link)
                        clustering_list+= get_node_spkeakers(ltc[1],number_cluster,link)
                        if set(complete_list).issubset(set(clustering_list)):
                            no_more_clustering = True
                    else:
                        no_more_clustering= True
    
    baselink = copy.deepcopy(link)    
    
    #log the DER
    link = copy.deepcopy(final_links)
    new_diar = copy.deepcopy(init_diar)
    cluster_list = scores.modelset.tolist()
    der, time = check_der(new_diar,cluster_list,link)
    
    print("After corrections, final DER :",der)

    #import pdb
    #pdb.set_trace()

    return False, new_diar, current_vec,der_track



def apply_correction(hyp, scores, c1, c2, method="min"):
    """

    """
    if method == "min":
        hyp = apply_correction_min(hyp, scores, c1, c2)
    elif method == "max":
        hyp = apply_correction_max(hyp, scores, c1, c2)
    elif method == "average":
        hyp = apply_correction_avr(hyp, scores, c1, c2)

    return hyp


def apply_correction_min(hyp,scores,c1,c2):
    c1list=[]
    c2list=[]

    for i in range(len(hyp)):
        if i!=c1 and hyp[i]['cluster'] == hyp[c1]['cluster']:
            c1list.append(i)
        if i!=c2 and hyp[i]['cluster'] == hyp[c2]['cluster']:
            c2list.append(i)

    if len(c1list)==0 and len(c2list)!=0:
        c2_to_c1 = True

    elif len(c2list)==0 and len(c1list)!=0:
        c2_to_c1 = False

    elif len(c1list)==0 and len(c2list)==0:
        c2_to_c1 = True

    else:
        c1dist = []
        c2dist = []
        for i in range(len(c1list)):
            c1dist.append(scores.scoremat[c1][c1list[i]])
        for i in range(len(c2list)):
            c2dist.append(scores.scoremat[c2][c2list[i]])
        if min(c2dist) <  min(c1dist):
            c2_to_c1 = True
        else:
            c2_to_c1 = False

    if c2_to_c1:
        hyp[c1]['cluster'] = hyp[c2]['cluster']
    else:
        hyp[c2]['cluster'] = hyp[c1]['cluster']
    return hyp




def apply_correction_max(hyp,scores,c1,c2):
    c1list=[]
    c2list=[]

    for i in range(len(hyp)):
        if i!=c1 and hyp[i]['cluster'] == hyp[c1]['cluster']:
            c1list.append(i)
        if i!=c2 and hyp[i]['cluster'] == hyp[c2]['cluster']:
            c2list.append(i)

    if len(c1list)==0 and len(c2list)!=0:
        c2_to_c1 = True

    elif len(c2list)==0 and len(c1list)!=0:
        c2_to_c1 = False

    elif len(c1list)==0 and len(c2list)==0:
        c2_to_c1 = True

    else:
        c1dist = []
        c2dist = []
        for i in range(len(c1list)):
            c1dist.append(scores.scoremat[c1][c1list[i]])
        for i in range(len(c2list)):
            c2dist.append(scores.scoremat[c2][c2list[i]])
        if max(c2dist) <  max(c1dist):
            c2_to_c1 = True
        else:
            c2_to_c1 = False

    if c2_to_c1:
        hyp[c1]['cluster'] = hyp[c2]['cluster']
    else:
        hyp[c2]['cluster'] = hyp[c1]['cluster']
    return hyp

def apply_correction_avr(hyp,scores,c1,c2):
    c1list=[]
    c2list=[]

    for i in range(len(hyp)):
        if i!=c1 and hyp[i]['cluster'] == hyp[c1]['cluster']:
            c1list.append(i)
        if i!=c2 and hyp[i]['cluster'] == hyp[c2]['cluster']:
            c2list.append(i)

    if len(c1list)==0 and len(c2list)!=0:
        c2_to_c1 = True

    elif len(c2list)==0 and len(c1list)!=0:
        c2_to_c1 = False

    elif len(c1list)==0 and len(c2list)==0:
        c2_to_c1 = True

    else:
        c1dist = []
        c2dist = []
        for i in range(len(c1list)):
            c1dist.append(scores.scoremat[c1][c1list[i]])
        for i in range(len(c2list)):
            c2dist.append(scores.scoremat[c2][c2list[i]])
        if sum(c2dist)/float(len(c2dist)) <  sum(c1dist)/float(len(c1dist)):
            c2_to_c1 = True
        else:
            c2_to_c1 = False

    if c2_to_c1:
        hyp[c1]['cluster'] = hyp[c2]['cluster']
    else:
        hyp[c2]['cluster'] = hyp[c1]['cluster']
    return hyp

