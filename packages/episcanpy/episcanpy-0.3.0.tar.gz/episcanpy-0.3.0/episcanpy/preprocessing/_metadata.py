import anndata as ad
import pandas as pd

def load_metadata(adata, metadata_file, path='', separator=';', remove_index_str = None):
    """
    Load observational metadata in adata.obs.
    Input metadata file as csv/txt and the adata object to annotate.

    first raw of the metadata file is considered as a header
    first column contain the cell name

    Paramters
    ---------

    adata: initial AnnData object

    metadata_file: csv file containing as a first column the cell names and in the
        rest of the columns any king of metadata to load

    path: pathe to the metadata file

    separator: ';' or "\t", character used to split the columns
    
    remove_index_str: a list of string to be removed in the index of AnnData object.
    Default value is None. For example, if the index is ['/path/to/file1.txt','/path/to/file2.txt']
    and remove_index_str = ['/path/to/','.txt'], then the index of AnnData object 
    will be changed to ['file1','file2']
    
    Return
    ------
    Annotated AnnData 
    """
    # dict_annot = {}
    # with open(path+metadata_file) as f:
    #     head = f.readline().strip().split(separator)
    #     file = f.readlines()
    # for key in head:
    #     dict_annot[key] = []
    # data = [line.strip().split(separator) for line in file]
    # for name in adata.obs_names:
    #     # this line is not always true. It depends on how the format of the data are
    #     name = name.split('.')[0]
    #     found = False
    #     for line in data:
    #         if name == line[0]:
    #             i = 0
    #             for key in head:
    #                 dict_annot[key].append(line[i])
    #                 i += 1 
    #             found = True
    #             continue
    #     # if we could not find annotations
    #     if found == False:
    #         for key in head:
    #             dict_annot[key].append('NA')
    # for key in head:
    #     adata.obs[key] = dict_annot[key]
    metadata = pd.read_csv(path+metadata_file, sep = "\t", header = 0)
    str_index = adata.obs.index
    if remove_index_str:
        for value in remove_index_str:
            str_index = str_index.str.replace(value,'',regex=False)
    df = pd.DataFrame('NA', index=str_index, columns=metadata.columns)
    for key,value in metadata.iterrows():
        try:
            df[value.index[0]][value[0]] =  value[0]
            df[value.index[1]][value[0]] =  value[1]
        except:
            continue
    adata.obs.index = str_index
    for key in df.columns:
        adata.obs[key] = df[key]

### function to optimize running time

def find_genes(adata, gtf_file_name, path='', extension=5000,
               key_added='gene_name', feature_coordinates=None, copy=True):
    """
    Given a gtf file, you can match peak coordinates (stored in adata.var_names or
    in a var annotation) to genes.
    The peak annotation has to be written as chr1:20000-20500 or chr1_20000_20500.
    the corresponding gene (if any) will be sotred in a var annotation 
    It extend the search to match a gene to an window of + and - extensions size(5kb
    for example).
    """
    #start = time.time()

    # load the gtf file
    gtf_file = []
    with open(gtf_file_name) as f:
        for line in f:
            if line[0] != '#':
                gtf_file.append(line)
    gtf_file = pd.DataFrame([l.split('\t') for l in gtf_file])
    gtf_file.columns = ['Chromosome', 'source', 'gene_type', 'Start', 'End',
                   'NA', 'Strand', 'NA2', 'extra_info'] 
    
    del gtf_file['NA'], gtf_file['NA2']
    
    # extract the variable names
    feature_annot = adata.var
    if feature_coordinates ==None:
        feature_names = adata.var_names.tolist()
    else:
        feature_names = adata.var[feature_coordinates]
    
    # format the feature name
    start_feature = []
    end_feature = []
    chrom_feature = []
    for feature in feature_names:
        if ':' in feature: # if the feature is a Granger coordinate.
            feature2 = feature.split(':')
            w = [int(x) for x in feature2[1].split('-')]
        else:
            feature2 = feature.split('_')
            w = [int(x) for x in feature2[1:]]
        chrom_feature.append(feature2[0][3:])
        start_feature.append(w[0])
        end_feature.append(w[1])
    
    adata.var['Index'] = range(0,len(chrom_feature))
    adata.var['Chromosome'] = chrom_feature
    adata.var['Start'] = start_feature
    adata.var['End'] = end_feature
    adata.var['name_feature'] = adata.var_names.tolist()
    #adata.var['chrom_feature'] = chrom_feature
    adata.var['start_ext'] = [x-extension for x in start_feature]
    adata.var['end_ext'] = [x+extension for x in end_feature]
    #adata.var['Strand'] = len(end_feature)*['+']
    
    
    # match the feature with 
    gtf = pr.PyRanges(gtf_file)
    del gtf_file
    adata_var = pr.PyRanges(chromosomes=adata.var.loc[:,'Chromosome'], #strands=adata.var.loc[:,'strand_feature'],
               starts=adata.var.loc[:,'start_ext'], ends=adata.var.loc[:,'end_ext'])
    
    merge = gtf.join(adata_var, suffix="_ext")
    merge = merge.dfs
    overlap3 = pd.concat([merge[key] for key in merge.keys()])
    overlap3['Index'] = overlap3.index
    overlap4 = overlap3.sort_values(['Chromosome', 'Start_ext', 'End_ext', 'Index'])
     
    #print(time.time()-start)
    
    adata.var = adata.var.sort_values(['Chromosome', 'start_ext', 'end_ext'])
    adata_var = pr.PyRanges(adata.var)
    tot_gene_annot = []
    for chrom in list(set(adata.var['Chromosome'])):
        index_gtf = 0
        #next_index = 0
        #curr_adata = adata_var[chrom].df
        overlap3 = pd.concat([merge[key] for key in [(chrom, '+'), (chrom, '-')]])
        overlap3['Index'] = overlap3.index
        overlap3 = overlap3.sort_values(['Chromosome', 'Start_ext', 'End_ext', 'Index'])
        overlap_chrom = overlap3['Start_ext'].tolist()
        #for line_adata in curr_adata[['start_ext']].iterrows():
        for line_adata in adata_var[chrom].df[['start_ext']].iterrows():
            gene_annot = []
            for start_gtf in overlap_chrom[index_gtf:]:
                if start_gtf == line_adata[1][0]:
                    gene_annot.append(overlap3.iloc[index_gtf])
                    index_gtf += 1
                    continue
                else:
                    #index_gtf = next_index
                    break
                
            if gene_annot == []:
                tot_gene_annot.append(('NA'))
            else:
                tot_gene_annot.append(tuple(gene_annot))
        #print(chrom, time.time()-start)
    
    
    adata.var[key_added] = tot_gene_annot
    adata.var.sort_values(['Index'])
    #print(time.time()-start)
    return(tot_gene_annot, overlap4)
