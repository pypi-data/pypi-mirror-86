"""
A SNP data structure and related stuff.
"""
import os, sys
import copy, csv, math
import re
from palos.ProcessOptions import  ProcessOptions
from palos.utils import dict_map, importNumericArray, figureOutDelimiter, \
    PassingData, getColName2IndexFromHeader, openGzipFile
from palos.db import TableClass

pa_has_characters = re.compile(r'[a-zA-Z_]')

num = importNumericArray()
numpy = num

#2008-05-06 ab2number and number2ab is for 384-illumina data
ab2number = {'N': 0,
    'NA': 0,
    'A': 1,
    'B': 2,
    'H': 3}

number2ab = {0: 'NA',
    1: 'A',
    2: 'B',
    3: 'H'}

#2008-09-22 A:T, C:G complement group in number
number2complement = {-1:-1, 0:0, 1:4, 4:1, 2:3, 3:2}
#2008-01-06
nt2complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

def reverseComplement(inputSeqStr=""):
    """
    2012.8.20
        vast superior to nt2complement
    """
    from Bio.Seq import Seq
    from Bio.Alphabet import generic_dna
    my_dna = Seq(inputSeqStr, generic_dna)
    return my_dna.reverse_complement().tostring()

#2008-05-12	a common NA set
NA_set = set([0, 'NA', 'N', -2, '|'])

# 2009-6-5 add lower-case letter to the dictionary
nt2number = {'|': -2,	#2008-01-07 not even tried. 'N'/'NA' is tried but produces inconclusive result.
    '-': -1,	#deletion
    'N': 0,
    'NA': 0,
    'n': 0,
    'na': 0,
    'X': 0,
    'x': 0,
    None: 0,
    'A': 1,
    'a': 1,
    'C': 2,
    'c': 2,
    'G': 3,
    'g': 3,
    'T': 4,
    't': 4,
    'AA': 1,
    'aa': 1,
    'CC': 2,
    'cc': 2,
    'GG': 3,
    'gg': 3,
    'TT': 4,
    'tt': 4,
    'AC': 5,
    'CA': 5,
    'M': 5,
    'm': 5,
    'AG': 6,
    'GA': 6,
    'R': 6,
    'r': 6,
    'AT': 7,
    'TA': 7,
    'W': 7,
    'w': 7,
    'CG': 8,
    'GC': 8,
    'S': 8,
    's': 8,
    'CT': 9,
    'TC': 9,
    'Y': 9,
    'y': 9,
    'GT': 10,
    'TG': 10,
    'K': 10,
    'k': 10
    }

# 2009-5-19 map nucleotide to number while ignoring heterozygous calls
nt2number_without_het = {'|': -2,	#2008-01-07 not even tried. 'N'/'NA' is tried but produces inconclusive result.
    '-': -1,	#deletion
    'N': 0,
    'NA': 0,
    None: 0,
    'A': 1,
    'C': 2,
    'G': 3,
    'T': 4,
    'AC':0,
    'CA':0,
    'M':0,
    'AG':0,
    'GA':0,
    'R':0,
    'AT':0,
    'TA':0,
    'W':0,
    'CG':0,
    'GC':0,
    'S':0,
    'CT':0,
    'TC':0,
    'Y':0,
    'GT':0,
    'TG':0,
    'K':0
    }

number2nt = {-2: '|',	#2008-01-07 not even tried. 'N'/'NA' is tried but produces inconclusive result.
    -1: '-',
    0: 'NA',
    num.nan: 'NA',	#2008-12-03	data_matrix might contain num.nan as NA
    1:'A',
    2:'C',
    3:'G',
    4:'T',
    5:'AC',
    6:'AG',
    7:'AT',
    8:'CG',
    9:'CT',
    10:'GT'
    }

#2013.07.03 for diploids
number2di_nt = {-2: '|',	#2008-01-07 not even tried. 'N'/'NA' is tried but produces inconclusive result.
    -1: '-',
    0: 'NA',
    num.nan: 'NA',	#2008-12-03	data_matrix might contain num.nan as NA
    1:'AA',
    2:'CC',
    3:'GG',
    4:'TT',
    5:'AC',
    6:'AG',
    7:'AT',
    8:'CG',
    9:'CT',
    10:'GT'
    }

#2009-6-5 dictionary used in output FASTA format which doesn't recognize two-letter heterozygous representation
number2single_char_nt = {-2: '|',	#2008-01-07 not even tried. 'N'/'NA' is tried but produces inconclusive result.
    -1: '-',
    0: 'N',
    num.nan: 'N',	#2008-12-03	data_matrix might contain num.nan as NA
    1:'A',
    2:'C',
    3:'G',
    4:'T',
    5:'M',
    6:'R',
    7:'W',
    8:'S',
    9:'Y',
    10:'K'
    }
    
    
number2color = {-1:(0,0,0), 0:(255,255,255), 1:(0,0,255), 2:(0,255,0), 3:(255,0,0), 4:(122,0,122), 5:(122,122,0), 6:(122,255,255), 7:(122,122,122), 8:(255,122,0), 9:(255,255,122), 10:(122,122,255) }

#2007-04-16 entry[i,j] means whether nucleotide i and j matches. 0(NA) matches everything. singleton(1-4) matches itself and the doublet containing it. doublet(5-10) matches only itself.
nt_number_matching_matrix = [[1, 1,1,1,1,1, 1,1,1,1,1],
    [1, 1,0,0,0,1, 1,1,0,0,0],
    [1, 0,1,0,0,1, 0,0,1,1,0],
    [1, 0,0,1,0,0, 1,0,1,0,1],
    [1, 0,0,0,1,0, 0,1,0,1,1],
    [1, 1,1,0,0,1, 0,0,0,0,0],
    [1, 1,0,1,0,0, 1,0,0,0,0],
    [1, 1,0,0,1,0, 0,1,0,0,0],
    [1, 0,1,1,0,0, 0,0,1,0,0],
    [1, 0,1,0,1,0, 0,0,0,1,0],
    [1, 0,0,1,1,0, 0,0,0,0,1]]

def calDistOfTwoHetCallsInNumber(call1, call2, hetHalfMatchDistance=0.5):
    """
    2011-10-20
        add argument hetHalfMatchDistance
    2011-10-18
        calculate distance between calls.
            0 = same. 1 = full distance. 0.5 half match.
        one or both calls could be heterozygous
    """
    if call1==call2:
        return 0
    else:
        call1_nt = number2nt[call1]
        call2_nt = number2nt[call2]
        call1_nt_set = set()
        for nt in call1_nt:
            call1_nt_set.add(nt)
        
        call2_nt_set = set()
        for nt in call2_nt:
            call2_nt_set.add(nt)
        intersectionSet = call1_nt_set&call2_nt_set
        if len(intersectionSet)>0:	#one haplotype matches
            return hetHalfMatchDistance
        else:	#completely different
            return 1

def get_nt_number2diff_matrix_index(number2nt):
    """
    2009-5-18
        only the integer-type keys in number2nt, which contains num.nan in it now. 
    2008-05-19
        moved from variation.src.common
    2008-01-01 copied from CmpAccession2Ecotype.py
    2007-10-31/2008-01-07
        nucleotide number ranges from -2 to 10.
        the diff_matrix_index ranges from 0 to 12.
    """
    sys.stderr.write("Getting nt_number2diff_matrix_index from nt2number ...")
    nt_number2diff_matrix_index = {}
    number_nt_ls = []
    for number, nt in number2nt.items():
        if type(number)==int:	#2009-5-18 number2nt contains num.nan
            number_nt_ls.append([number,nt])
    number_nt_ls.sort()
    for i in range(len(number_nt_ls)):
        nt_number2diff_matrix_index[number_nt_ls[i][0]] = i
    sys.stderr.write("Done.\n")
    return nt_number2diff_matrix_index

def RawSnpsData_ls2SNPData(rawSnpsData_ls, report=0, use_nt2number=0, snpIDAsString=True):
    """
    2013.07.03 added argument snpIDAsString
        True: row_id = 'chr_pos'
        False: row_id = (chr, pos)
    2012.8.20 bugfix
        generate snpData in the end.
    2008-05-19
        this returns a SNPData in same orientation as rawSnpsData_ls, SNP (row) X Strain (column).
        apply transposeSNPData after this if another orientation is favored.
    2008-05-19
        swap accession id and array id in col_id. now accession_id in 1st
    2008-05-11
        adapts RawSnpsData(bjarni's SNP data structure) to SNPData
        
        combine all chromsomes together
    """
    if report:
        sys.stderr.write("Converting RawSnpsData_ls to SNPData ...")
    nt_dict_map = lambda x: nt2number[x]
    row_id_ls = []; col_id_ls=[]; data_matrix=[]
    for i in range(len(rawSnpsData_ls)):
        rawSnpsData = rawSnpsData_ls[i]
        chromosome = rawSnpsData.chromosome
        if i==0:	#only need once
            for j in range(len(rawSnpsData.accessions)):
                if rawSnpsData.arrayIds:
                    col_id = (rawSnpsData.accessions[j], rawSnpsData.arrayIds[j])
                else:
                    col_id = rawSnpsData.accessions[j]
                col_id_ls.append(col_id)
        for j in range(len(rawSnpsData.positions)):
            if use_nt2number:
                data_row = map(nt_dict_map, rawSnpsData.snps[j])
            else:
                data_row = rawSnpsData.snps[j]
            data_matrix.append(data_row)
            if snpIDAsString:
                snpID = "%s_%s"%(chromosome, rawSnpsData.positions[j])
            else:
                snpID = (chromosome, rawSnpsData.positions[j])
            row_id_ls.append(snpID)
    if report:
        sys.stderr.write("Done.\n")
    snpData = SNPData(row_id_ls = row_id_ls, col_id_ls=col_id_ls, data_matrix=data_matrix)
    return snpData

def transposeSNPData(snpData, report=0):
    """
    2008-12-03
        newSnpData.processRowIDColID() after row_id_ls and col_id_ls are given
        also copy strain_acc_list and category_list over to newSnpData
    2008-05-18
        use num.int8 to keep memory small in num.transpose(num.array(snpData.data_matrix, num.int8))
    2008-05-18
        no more copy.deepcopy(snpData), data_matrix takes too long and too much memory
    05/12/08 fix a bug (return snpData)
    2008-05-11
    """
    if report:
        sys.stderr.write("Transposing SNPData ...")
    from palos import importNumericArray, SNPData
    num = importNumericArray()
    #copy except data_matrix
    import copy
    newSnpData = SNPData()
    """
    for option_tuple in SNPData.option_default_dict:
        var_name = option_tuple[0]
        if var_name!='data_matrix':
            setattr(newSnpData, var_name, copy.deepcopy(getattr(snpData, var_name)))
    """
    newSnpData.row_id_ls = copy.deepcopy(snpData.col_id_ls)
    newSnpData.col_id_ls = copy.deepcopy(snpData.row_id_ls)
    # 2012.8.20 snpData.strain_acc_list could be 1st column of each entry in snpData.row_id_ls, and thus 1st column of newSnpData.col_id
    #newSnpData.strain_acc_list = copy.deepcopy(snpData.strain_acc_list)
    #newSnpData.category_list = copy.deepcopy(snpData.category_list)
    
    newSnpData.processRowIDColID()	#2008-12-02	processRowIDColID() after row_id_ls and col_id_ls are given
    if isinstance(snpData.data_matrix, list):
        newSnpData.data_matrix = num.transpose(num.array(snpData.data_matrix, num.int8))
    else:	#assume it's array type already. Numeric/numarray has ArrayType, but numpy doesn't
        newSnpData.data_matrix = num.transpose(snpData.data_matrix)
    if report:
        sys.stderr.write("Done.\n")
    return newSnpData

def SNPData2RawSnpsData_ls(snpData, use_number2nt=1, need_transposeSNPData=0, report=0, mask_untouched_deleltion_as_NA=1):
    """
    2009-6-17
        stop masking deletion as NA
    2008-05-19
        the transformation assumes snpData is in the orientation of SNP(row_id_ls) X Strain (col_id_ls). if not, toggle need_transposeSNPData=1.
    2008-05-18
        add mask_untouched_deleltion_as_NA. turned on by default because bjarni's RawSnpsData structure only recognizes NA, A, T, C, G
        if col_id in newSnpData.col_id_ls is tuple of size >1, the 2nd one  in the tuple is taken as array id.
    2008-05-12
        reverse of RawSnpsData_ls2SNPData
        
        adapts SNPData (Yu's SNP data structure) to RawSnpsData(bjarni's SNP data structure)
        
        split into different chromsomes
    """
    if report:
        sys.stderr.write("Converting SNPData to RawSnpsData_ls ...")
    from variation.src.io.snpsdata import RawSnpsData
    
    if need_transposeSNPData:
        newSnpData = transposeSNPData(snpData, report=report)
    else:
        newSnpData = snpData
    
    accessions = []
    arrayIds = []
    accession_id = None	#default
    array_id = None	#default
    for col_id in newSnpData.col_id_ls:
        if isinstance(col_id, tuple):
            if len(col_id)>0:
                accession_id = col_id[0]
            if len(col_id)>1:
                array_id = col_id[1]
        else:
            accession_id = col_id
        accessions.append(accession_id)
        if array_id is not None:
            arrayIds.append(array_id)
    
    if mask_untouched_deleltion_as_NA:
        number2nt[-2] = 'NA'	#mask -2 (untouched) as 'NA'
        #number2nt[-1] = 'NA'	#mask -1 (deletion) as 'NA'
    number2nt_dict_map = lambda x: number2nt[x]
    rawSnpsData_ls = []
    
    rawSnpsData = RawSnpsData(accessions=accessions, arrayIds=arrayIds)
    rawSnpsData.snps = []
    rawSnpsData.positions = []
    row_id0 = newSnpData.row_id_ls[0]
    old_chromosome = row_id0.split('_')[:1]
    rawSnpsData.chromosome = old_chromosome
    rawSnpsData_ls.append(rawSnpsData)
    rawSnpsData_ls_index = 0
    for i in range(len(newSnpData.row_id_ls)):
        row_id = newSnpData.row_id_ls[i]
        new_chromosome, position = row_id.split('_')[:2]
        position = int(position)
        if new_chromosome!=old_chromosome:
            rawSnpsData = RawSnpsData(accessions=accessions, arrayIds=arrayIds)
            rawSnpsData.snps = []
            rawSnpsData.positions = []
            rawSnpsData_ls.append(rawSnpsData)
            rawSnpsData_ls_index += 1
            rawSnpsData.chromosome = new_chromosome
            old_chromosome = new_chromosome
        rawSnpsData_ls[rawSnpsData_ls_index].positions.append(position)
        if use_number2nt:
            data_row = map(number2nt_dict_map, newSnpData.data_matrix[i])
        else:
            data_row = newSnpData.data_matrix[i]
        rawSnpsData_ls[rawSnpsData_ls_index].snps.append(data_row)
    if report:
        sys.stderr.write("Done.\n")
    return rawSnpsData_ls

def write_data_matrix(data_matrix, output_fname, header, strain_acc_list, category_list, rows_to_be_tossed_out=None, \
            cols_to_be_tossed_out=None, nt_alphabet=0, transform_to_numpy=0,\
            discard_all_NA_rows=0, strain_acc2other_info=None, delimiter='\t', \
            predefined_header_row=['strain', 'duplicate', 'latitude', 'longitude', 'nativename', 'stockparent', 'site', 'country']):
    """
    Arguments:
        strain_acc_list (and category_list) are initial 2 columns in the output.
        rows_to_be_tossed_out is a set or dict with row index in it. cols_to_be_tossed_out is similar structure.
    2010-4-22
        set transform_to_numpy default to 0, it's problematic when a 2D list containing character 'NA' 
            is converted into a numpy array. This renders the whole 2D list
            being converted into a character numpy array.
    2008-05-19
        add output_fname in report
    2008-05-12
        copied from __init__.py
    2008-05-08
        include more options from dbSNP2data.py's write_data_matrix()
    2008-05-06
        add transform_to_numpy
    2008-04-02
        extracted from variation.src.FilterStrainSNPMatrix to be standalone.
    """
    sys.stderr.write("Writing data_matrix to %s ..."%(output_fname))
    if rows_to_be_tossed_out==None:
        rows_to_be_tossed_out = set()
    if cols_to_be_tossed_out==None:
        cols_to_be_tossed_out = set()

    writer = csv.writer(openGzipFile(output_fname, 'w'), delimiter=delimiter)
    
    if header:
        new_header = [header[0], header[1]]
        if strain_acc2other_info:
            no_of_fields = len(strain_acc2other_info[strain_acc2other_info.keys()[0]])
            for i in range(no_of_fields):
                new_header.append(predefined_header_row[2+i])
        for i in range(2, len(header)):
            if i-2 not in cols_to_be_tossed_out:
                new_header.append(header[i])
        writer.writerow(new_header)
    
    #figure out no_of_rows, no_of_cols
    if type(data_matrix)==list and transform_to_numpy:	#2008-02-06 transform the 2D list into array
        data_matrix = numpy.array(data_matrix)
        #data_matrix = numpy.array(data_matrix,dtype="int8")
        no_of_rows, no_of_cols = data_matrix.shape
    else:
        no_of_rows = len(data_matrix)
        if no_of_rows>0:
            no_of_cols = len(data_matrix[0])
        else:
            no_of_cols = 0
    
    no_of_all_NA_rows = 0
    for i in range(no_of_rows):
        if discard_all_NA_rows and sum(data_matrix[i]==0)==no_of_cols:	# 2010-1-24, in numerical representation of nucleotides, 0 = NA.
            no_of_all_NA_rows += 1
            continue
        if i not in rows_to_be_tossed_out:
            new_row = [strain_acc_list[i], category_list[i]]
            if strain_acc2other_info:
                new_row += strain_acc2other_info[strain_acc_list[i]]
            for j in range(no_of_cols):
                if j not in cols_to_be_tossed_out:
                    if nt_alphabet:
                        new_row.append(number2nt[data_matrix[i][j]])
                    else:
                        new_row.append(data_matrix[i][j])
            writer.writerow(new_row)
    del writer
    sys.stderr.write("%s NA rows. Done.\n"%no_of_all_NA_rows)

def read_data(inputFname, input_alphabet=0, turn_into_integer=1, double_header=0, delimiter=None, \
            matrix_data_type=int, ignore_het=0,\
            data_starting_col=2, row_id_key_set=None, row_id_hash_func=None, col_id_key_set=None, col_id_hash_func=None):
    """
    2010-4-26
        report the number of data rows and total number of points read in.
    2010-3-31
        add 2 arguments:
            col_id_key_set: only retain columns whose keys are in this set 
            col_id_hash_func: a function that maps the original col-id (=row[0:2]) from inputFname to the one in col_id_key_set
    2009-12-11
        add 2 arguments:
            row_id_key_set: only retain rows whose keys are in this set 
            row_id_hash_func: a function that maps the original row-id (=row[0:2]) from inputFname to the one in row_id_key_set
    2009-10-12
        add argument data_starting_col, specifying which column (index from 0) the data starts from. default is 2 (3rd column).
    2009-10-11
        scope of try ... except is expanded to include the whole for loop.
    2009-8-19
        if turn_into_integer==1 and matrix_data_type==int and characters were found in the 1st entry of the data row, use the nucleotide2number map.
        turn_into_integer is beyond its literal meaning. It's a flag to turn the input into a numerical type (= matrix_data_type).
        
        eg:
        
        #read a phenotype matrix. turn_into_integer=2 because it's not nucleotides
        header_phen, strain_acc_list_phen, category_list_phen, data_matrix_phen = read_data(inputFname, turn_into_integer=2, \
            matrix_data_type=float)
        phenData = SNPData(header=header_phen, strain_acc_list=strain_acc_list_phen, data_matrix=data_matrix_phen)
        
    2009-5-20
        add argument ignore_het, which upon toggled, instructs the function to use nt2number_without_het to map nucleotides to number.
    2009-3-21
        add '-' into vocabulary of p_char and append '$' requiring the entry ends with any characters in that vocabulary
    2009-2-18
        no 'e' or 'E' among the letters to be checked in the 1st column in order to decide whether to cast it into matrix_data_type
        because 'e' or 'E' could be used in scientific number.
        a better version is only to check whether nucleotide letters are in it, because nt2number is used if the check is positive.
    2008-08-29
        put the handling of each row into a "try ... except ..."
    2008-08-07
        turn_into_integer has to be toggled as well as p_char() detects character before nt2number is used.
    2008-08-03
        if p_char() detects character but dict_map() via nt2number fails to convert every entry in the row, turn data_row back to original un-converted.
    2008-07-11
        use p_char to judge whether there is character in the data, then use nt2number to convert them.
        input_alphabet is deprecated.
    2008-05-21
        add matrix_data_type, default=int. data_row = map(matrix_data_type, data_row)
    2008-05-18
        copied from FilterStrainSNPMatrix.py
        if delimiter not specified, call figureOutDelimiter()
    2008-05-12
        add delimiter
    2008-05-07
        add option double_header
    2007-03-06
        different from the one from SelectStrains.py is map(int, data_row)
    2007-05-14
        add input_alphabet
    2007-10-09
        add turn_into_integer
    """
    sys.stderr.write("Reading data from %s ..."%inputFname)
    if ignore_het:
        nt2number_mapper = nt2number_without_het
    else:
        nt2number_mapper = nt2number
    def ignore_het_func(x):
        if x>4:
            return 0
        else:
            return x
    if delimiter is None:
        delimiter = figureOutDelimiter(inputFname)
    reader = csv.reader(openGzipFile(inputFname), delimiter=delimiter)
    
    header = next(reader)
    # 2010-3-31 pick the columns according to col_id_key_set
    col_id_ls = header[data_starting_col:]
    no_of_cols = len(col_id_ls)
    col_index_ls = range(no_of_cols)
    if col_id_key_set is not None:
        new_col_id_ls = []
        new_col_index_ls = []
        for i in range(no_of_cols):
            col_id = col_id_ls[i]
            if col_id_hash_func is not None:
                col_id_key = col_id_hash_func(col_id)
            else:
                col_id_key = col_id
            if col_id_key in col_id_key_set:
                new_col_id_ls.append(col_id)
                new_col_index_ls.append(i)
        col_id_ls = new_col_id_ls
        col_index_ls = new_col_index_ls
        sys.stderr.write("%s columns out of %s in col_id_key_set (%s items) are retained."%(
            len(col_index_ls), \
            no_of_cols, len(col_id_key_set) ))
    # 2010-3-31 adjust the header
    header = header[:data_starting_col] + col_id_ls
    if double_header:
        second_header = next(reader)
        second_header = second_header[:data_starting_col] + [second_header[i+data_starting_col] for i in col_index_ls]
        header = zip(second_header,header)
    
    data_matrix = []
    strain_acc_list = []
    category_list = []
    import re
    p_char = re.compile(r'[a-df-zA-DF-Z\-]$')
    #no 'e' or 'E', used in scientific number, add '-' and append '$'
    i = 0
    no_of_data_points = 0	#2010-4-26
    try:
        for row in reader:
            if len(col_index_ls)==0:
                sys.stderr.write("Warning: data matrix is empty.\n")
                break
            i += 1
            row_id = tuple(row[0:2])
            if row_id_key_set is not None:	# 2009-12-11 use it to filter rows
                if row_id_hash_func is not None:
                    row_id_key = row_id_hash_func(row_id)
                else:
                    row_id_key = row_id
                if row_id_key not in row_id_key_set:
                    continue
            strain_acc_list.append(row[0])
            category_list.append(row[1])
            original_data_row = row[data_starting_col:]
            if col_id_key_set is not None:
                # 2010-3-31 only pick a few rows
                original_data_row = [original_data_row[i] for i in col_index_ls]
            
            data_row = original_data_row
            no_of_snps = len(data_row)
            p_char_used = 0
            #whether p_char is used depends on condition below (nucleotides were transformed into integers).
            if p_char.search(data_row[0]) and turn_into_integer==1 and matrix_data_type==int:
                data_row = dict_map(nt2number_mapper, data_row)
                p_char_used = 1
                if no_of_snps!=len(data_row):
                    sys.stderr.write('\n dict_map() via nt2number_mapper only maps %s out of %s entries from this row, %s ..., to integer. Back to original data.\n'%\
                                    (len(data_row), no_of_snps, repr(row[:5])))
                    data_row = original_data_row	#back to original data_row
                    p_char_used = 0
            
            if turn_into_integer and not p_char_used:
                #if p_char_used ==1, it's already integer.
                new_data_row = []
                for data_point in data_row:
                    if data_point=='NA' or data_point=='':
                        new_data_row.append(num.nan)
                    else:
                        new_data_row.append(matrix_data_type(data_point))
                #data_row = map(matrix_data_type, data_row)
                data_row = new_data_row
                if ignore_het:
                    #2009-5-20 for data that is already in number format, use this function to remove hets
                    data_row = map(ignore_het_func, data_row)
            no_of_data_points += len(data_row)
            data_matrix.append(data_row)
    except:
        sys.stderr.write('Except type: %s\n'%repr(sys.exc_info()))
        import traceback
        traceback.print_exc()
        # sys.stderr.write("Row no: %s.\n"%(i))
        sys.stderr.write("Row no: %s. %s ....\n"%(i, repr(row[:10])))
        raise
    del reader
    no_of_rows = len(data_matrix)
    if no_of_rows>0:
        no_of_cols = no_of_data_points/float(no_of_rows)
    else:
        no_of_cols=None
    sys.stderr.write("%s rows, %s columns, %s data points. Done.\n"%(no_of_rows, no_of_cols, no_of_data_points))
    return header, strain_acc_list, category_list, data_matrix


def readAdjacencyListDataIntoMatrix(inputFname=None, rowIDHeader=None,
    colIDHeader=None, rowIDIndex=None, colIDIndex=None,
    dataHeader=None, dataIndex=None, hasHeader=True, defaultValue=None,
    dataConvertDictionary=None,
    matrixDefaultDataType=None, asymmetric=False):
    """
    
    similar to readAdjacencyListDataIntoMatrix() but now the M[i,j]!=M[j,i].
    return a SNPData
    
    i.e.
        from palos import SNP
        import numpy
        snpData = SNP.readAdjacencyListDataIntoMatrix(inputFname=inputFname,
            rowIDHeader='Sample', colIDHeader='SNP', \
            rowIDIndex=None, colIDIndex=None, \
            dataHeader='Geno', dataIndex=None, hasHeader=True, defaultValue=0, \
            dataConvertDictionary=SNP.nt2number, matrixDefaultDataType=numpy.int, asymmetric=True)
        snpData.tofile(outputFname)
        
        #read in the IBD check result
        self.ibdData = SNP.readAdjacencyListDataIntoMatrix(inputFname=self.plinkIBDCheckOutputFname, \
                            rowIDHeader="IID1", colIDHeader="IID2", \
                            rowIDIndex=None, colIDIndex=None, \
                            dataHeader="PI_HAT", dataIndex=None, hasHeader=True)
        
        #read in kinship
        self.ibdData = SNP.readAdjacencyListDataIntoMatrix(
            inputFname=self.pedigreeKinshipFilePath, \
                            rowIDHeader=None, colIDHeader=None, \
                            rowIDIndex=0, colIDIndex=1, \
                            dataHeader=None, dataIndex=2, hasHeader=False)
        
    """
    sys.stderr.write("Reading a matrix out of an adjacency-list based file %s ..."%(inputFname))
    from palos import MatrixFile
    import numpy
    if defaultValue is None:
        defaultValue = numpy.nan
    
    reader = MatrixFile(path=inputFname)
    if hasHeader:
        header = next(reader)
        col_name2index = getColName2IndexFromHeader(header)
        if rowIDIndex is None and rowIDHeader:
            rowIDIndex = col_name2index.get(rowIDHeader)
        if colIDIndex is None and colIDHeader:
            colIDIndex = col_name2index.get(colIDHeader)
        if dataIndex is None and dataHeader:
            dataIndex = col_name2index.get(dataHeader)
    
    row_id2index  = {}
    if asymmetric:
        col_id2index = {}
    else:
        col_id2index = row_id2index
    row_id_ls = []
    if asymmetric:
        col_id_ls = []
    else:
        col_id_ls = row_id_ls
    idPair2data = {}
    counter = 0
    for row in reader:
        rowID = row[rowIDIndex]
        if rowID not in row_id2index:
            row_id2index[rowID] = len(row_id2index)
            row_id_ls.append(rowID)
        colID = row[colIDIndex]
        if colID not in col_id2index:
            col_id2index[colID] = len(col_id2index)
            col_id_ls.append(colID)
        data = row[dataIndex]
        if dataConvertDictionary:
            #2012.8.24 supply a dictionary here to map
            data = dataConvertDictionary[data]
        idPair = (rowID, colID)
        if idPair in idPair2data:
            sys.stderr.write("Warning idPair %s already in idPair2data with value=%s. overwritten with new data=%s.\n"%\
                            (repr(idPair), idPair2data.get(idPair), data))
        idPair2data[idPair] = data
        counter += 1
    
    no_of_rows = len(row_id2index)
    no_of_cols = len(col_id2index)
    filledFraction = len(idPair2data)/float((no_of_rows*no_of_cols))
    
    sys.stderr.write("%s pairs of data (input number of data=%s). number of unique row ids=%s, col ids=%s. %.3f filled.\n"%\
                    (len(idPair2data), counter, no_of_rows, no_of_cols, filledFraction))
    if matrixDefaultDataType is None:
        matrixDefaultDataType = numpy.float32
    
    dataMatrix = numpy.zeros([no_of_rows, no_of_cols], dtype=matrixDefaultDataType)
    dataMatrix[:] = defaultValue
    for idPair, data in  idPair2data.items():
        rowID = idPair[0]
        colID = idPair[1]
        id1_index = row_id2index.get(rowID)
        id2_index = col_id2index.get(colID)
        dataMatrix[id1_index][id2_index] = data
        if not asymmetric:
            dataMatrix[id2_index][id1_index] = data
    
    maskedMatrix = numpy.ma.array(dataMatrix, mask=numpy.isnan(dataMatrix))
    return SNPData(row_id_ls=row_id_ls, col_id_ls=col_id_ls, data_matrix=maskedMatrix)

def getKey2ValueFromMatrixLikeFile(inputFname=None, keyHeaderLs=None,
    valueHeaderLs=None, keyIndexLs=None, valueIndexLs=None, \
    hasHeader=True, valueDataType=None):
    """
    2012.8.22
        return a dictionary. key is a tuple of keyHeaderLs. value is conent of valueHeaderLs
    """
    sys.stderr.write("Getting a dictionary out of  %s ..."%(inputFname))
    from palos import MatrixFile
    
    reader = MatrixFile(path=inputFname)
    if hasHeader:
        header = next(reader)
        col_name2index = getColName2IndexFromHeader(header)
        if keyIndexLs is None and keyHeaderLs:
            keyIndexLs = []
            for keyHeader in keyHeaderLs:
                keyIndexLs.append(col_name2index.get(keyHeader))
        if valueIndexLs is None and valueHeaderLs:
            valueIndexLs = []
            for valueHeader in valueHeaderLs:
                valueIndexLs.append(col_name2index.get(valueHeader))
    
    counter = 0
    key2Value = {}
    for row in reader:
        counter += 1
        keyLs = []
        for keyIndex in keyIndexLs:
            keyLs.append(row[keyIndex])
        if len(keyLs)>1:
            key = tuple(keyLs)
        else:
            key = keyLs[0]
        valueLs = []
        for valueIndex in valueIndexLs:
            valueLs.append(row[valueIndex])
        if valueDataType:
            valueLs = map(valueDataType, valueLs)
        if len(valueLs)==1:
            value = valueLs[0]
        else:
            value = valueLs
        if key in key2Value:
            sys.stderr.write("Warning key %s already in key2Value with value=%s. overwritten with new data=%s.\n"%\
                            (repr(key), key2Value.get(key), repr(value)))
        key2Value[key] = value
    sys.stderr.write(" %s data in key2Value.\n"%(len(key2Value)))
    return key2Value


class SNPData(object):
    """
        example usages:
        
            snpData1 = SNPData(input_fname=self.input_fname1, turn_into_array=1, ignore_2nd_column=1)
            
            snpData1 = SNPData(input_fname=self.input_fname1, turn_into_array=1)
            
            CNVQCData = SNPData(input_fname=input_fname, turn_into_array=1, ignore_2nd_column=1, data_starting_col=2, turn_into_integer=False)
            
            header, strain_acc_list, category_list, data_matrix = read_data(self.input_fname, delimiter=delimiter)
            snpData = SNPData(header=header, strain_acc_list=strain_acc_list, category_list=category_list,\
                            data_matrix=data_matrix)
            
            covariateData = SNPData(row_id_ls=row_id_ls, col_id_ls=new_col_id_ls, data_matrix=data_matrix, ploidy=1)
            
            #2013.05.31 beagle format is different orientation and in nucleotides,
            # turn_into_integer=0 or 1 (default) is up to user
            beagleData = SNPData(row_id_ls=locusIDList, col_id_ls=sampleIDList, data_matrix=data_matrix, ploidy=2,\
                matrix_orientation=2, turn_into_integer=0)
            
            # 2010-3-22 read in the kinship matrix
            kinshipData = SNPData(input_fname=kinship_output_fname, ignore_2nd_column=1, matrix_data_type=float)
            
            # 2009-12-11, only retain rows whose ecotype IDs are in ecotype_id_set			
            ecotype_id_set = set(ecotype_id_ls)
            def row_id_hash_func(row_id):
                return int(row_id[0])
            snpData = SNPData(input_fname=inputFname, turn_into_array=1, row_id_key_set=ecotype_id_set, row_id_hash_func=row_id_hash_func)
    2013.05.31
        added argument ploidy, which affects self.row_id2index or self.col_id2index , depending on another new argument
            matrix_orientation
        Multi-ploidy (ploidy>1) assumes haplotypes of same individual are adjacent to each other.
        Row/Column index for each sample records only index of the 1st haplotype of each individual. 
    2009-5-20
        add argument ignore_het which is passed to read_data() when data_matrix is not given to ignore heterozygous calls.
        It'll only be functional when data_matrix is not given upon SNPData initialization.
    2008-05-19
        either directly specify row_id_ls, col_id_ls, data_matrix
            (if strain_acc_list and category_list is given rather than row_id_ls and col_id_ls, row_id_ls and col_id_ls will be formed from them).
        or give input_fname and associated options to read data from file.
    2008-05-18 moved from variation.src.QC_250k
        add more arguments, input_fname, turn_into_array, ignore_2nd_column
    """
    report = 0
    option_default_dict = {('row_id_ls', 0, ): None,\
                            ('col_id_ls', 0, ): None,\
                            ('header', 0, ): None,\
                            ('strain_acc_list', 0, ): None,\
                            ('category_list', 0, ): None,\
                            ('data_matrix', 0, ): None,\
                            
                            ('input_fname', 0, ): None,\
                            ('input_alphabet',0, int): 0,\
                            ('turn_into_integer', 0, int): 1,\
                            ('double_header', 0, int):0, \
                            ('ignore_2nd_column', 0, int): [0, '', 0, 'Ignore category_list, the 2nd column.'],\
                            ('turn_into_array', 0 ,): [0, '', 0, 'Turn the data_matrix into array'],\
                            ('ploidy', 1, int): [1, '', 1, 'ploidy of the organism described here. ploidy=#genotype-columns for one individual'],\
                            ('min_probability', 0, float): -1,\
                            ('call_method_id', 0, int): -1,\
                            ('col_id2id', 0, ):None,\
                            ('max_call_info_mismatch_rate', 0, float): 1,\
                            ('snps_table', 0, ): None,\
                            ('matrix_data_type', 0, ): int,\
                            ('matrix_orientation', 1, int): [1, '', 1, '1: rows are samples, columns are loci, Yu-format; 2: rows are loci, columns are samples'],\
                            ('ignore_het', 0, int): [0, '', 0, 'Ignore the heterozygous genotypes'],\
                            ('data_starting_col', 0, int): [2, '', 0, 'which column the data starts from'],\
                            ('debug', 0, int): [0, '', 0, 'turn on the debug flag']}
    def __init__(self, row_id_key_set=None, row_id_hash_func=None, col_id_key_set=None, col_id_hash_func=None, **keywords):
        """
        2013.3.6 added allele_sequence2allele_number & allele_number2allele_sequence
        2010-4-21 ignore_2nd_column is applied before processRowIDColID(). not just after read_data() is run.
        2009-12-11
            add 2 arguments (col_id_key_set and col_id_hash_func) to be passed to read_data()
        2010-3-22
            argument turn_into_integer does not just turn data into integer. It's about whether to cast data to type matrix_data_type.
            argument matrix_data_type is only used in read_data().
        2009-12-11
            add 2 arguments (row_id_key_set and row_id_hash_func) to be passed to read_data()
        """
        self.ad = ProcessOptions.process_function_arguments(keywords, self.option_default_dict, error_doc=self.__doc__, \
                                                        class_to_have_attr=self, howto_deal_with_required_none=2)
        # 2013.3.7 to encode the allele-sequence in numbers. check PolymorphismTableFile.py 
        self.allele_sequence2allele_number = {}
        self.allele_number2allele_sequence = {}
        
        #read it from file
        if self.isDataMatrixEmpty(self.data_matrix) and isinstance(self.input_fname,str):
            if os.path.isfile(self.input_fname):
                self.header, self.strain_acc_list, self.category_list, self.data_matrix = read_data(self.input_fname, self.input_alphabet, \
                                                                            self.turn_into_integer, self.double_header, \
                                                                            matrix_data_type=self.matrix_data_type,\
                                                                            ignore_het=self.ignore_het,\
                                                                            data_starting_col=self.data_starting_col,\
                                                                            row_id_key_set=row_id_key_set,\
                                                                            row_id_hash_func=row_id_hash_func,\
                                                                            col_id_key_set=col_id_key_set,\
                                                                            col_id_hash_func=col_id_hash_func)
            else:
                sys.stderr.write("Error: File %s is not a file.\n"%self.input_fname)
        # 2010-4-21 ignore_2nd_column is applied before processRowIDColID(). not just after read_data() is run.
        if self.ignore_2nd_column: 
            self.category_list = None
        self.processRowIDColID()
    
    @classmethod
    def isDataMatrixEmpty(cls, data_matrix):
        """
        2009-10-07
            if data_matrix is character numpy.array, "==''" won't work while "is ''" works in if-condition.
        2008-08-21
            make it a classmethod
        2008-08-19
            common function to judge whether data_matrix is empty
        """
        if data_matrix is '':	# 2009-10-07 if data_matrix is character numpy.array, "==''" won't work while "is ''" works.
            return True
        elif data_matrix is None:
            return True
        elif hasattr(data_matrix, '__len__') and len(data_matrix)==0:
            return True
        else:
            return False
        
    def isSNPId(self):
        """
        2011-5-6
            returns if the cols are in chr_pos or snpid format
        """
        isSNP = True
        if len(self.col_id_ls) > 0:
            try:
                int(self.col_id_ls[0])
            except:
                isSNP = False
        return isSNP
    
    def processRowIDColID(self):
        """
        2016.04 stop force-converting data_matrix into int8
        2010-2-27
            restore the strain_acc_list if it's None.
            fix a small bug in it:
                check whether row_id_ls[0] is of type tuple or list before taking its first element  
        2008-12-03
            this function is called in __init__(). deal with the case that this class is initialized without any argument,
                which means self.row_id_ls and self.col_id_ls are None.
        2008-09-07
            if turn the data_matrix into array, do not force num.int8 type.
        2008-09-05
            generate id2index for both row and column
        2008-06-02
            correct a bug here, opposite judgement of self.data_matrix
        """
        if not self.isDataMatrixEmpty(self.data_matrix) and self.turn_into_array:
            
            self.data_matrix = num.array(self.data_matrix) #, dtype="int8"
        
        if self.row_id_ls is None and self.strain_acc_list is not None:
            self.row_id_ls = []
            for i in range(len(self.strain_acc_list)):
                if self.category_list is not None:
                    row_id = (self.strain_acc_list[i], self.category_list[i])
                else:
                    row_id = self.strain_acc_list[i]
                self.row_id_ls.append(row_id)
        
        if self.strain_acc_list is None and self.row_id_ls is not None:	#2010-2-25 restore the strain_acc_list if it's None.
            if ( type(self.row_id_ls[0])== tuple or type(self.row_id_ls[0])==list ) and len(self.row_id_ls[0])==2:
                self.strain_acc_list = [row[0] for row in self.row_id_ls]
            else:
                self.strain_acc_list = [row for row in self.row_id_ls]
        
        self.row_id2row_index = {}
        if self.row_id_ls:	#2008-12-03
            for i in range(len(self.row_id_ls)):
                row_id = self.row_id_ls[i]
                if self.matrix_orientation==1:	#2013.05.31
                    row_index = i*self.ploidy
                else:
                    row_index = i
                self.row_id2row_index[row_id] = row_index
        
        if self.col_id_ls is None and self.header is not None:
            self.col_id_ls = []
            for i in range(2,len(self.header)):
                col_id = self.header[i]
                self.col_id_ls.append(col_id)
        
        self.col_id2col_index = {}
        if self.col_id_ls:	#2008-12-03
            for i in range(len(self.col_id_ls)):
                col_id = self.col_id_ls[i]
                if self.matrix_orientation==2:	#2013.05.31
                    col_index = i*self.ploidy
                else:
                    col_index = i
                self.col_id2col_index[col_id] = col_index
    
    def fromfile(self, input_fname, **keywords):
        """
        2008-05-19
            initialize structure from a file in Strain X SNP format. 1st two columns are about strains.
            for keywords. check read_data()
        """
        self.header, self.strain_acc_list, self.category_list, self.data_matrix = read_data(input_fname, **keywords)
        if self.ignore_2nd_column:
            self.category_list = None
        self.processRowIDColID()
        
    def tofile(self, output_fname, **keywords):
        """
        2008-06-02
            either strain_acc_list or category_list could be None
            try to fill them both
        2008-05-18
            keywords is same as write_data_matrix()
        """
        if self.header is None:
            self.header = ['', '']
            for col_id in self.col_id_ls:
                if isinstance(col_id, tuple):
                    if len(col_id)>1:
                        col_id = '%s_%s'%(col_id[0], col_id[1])	#chromosome, position
                    else:
                        col_id = col_id[0]
                self.header.append(col_id)
        if self.strain_acc_list is None or self.category_list is None:
            strain_acc_list = []
            category_list = []
            for row_id in self.row_id_ls:
                strain_acc = None
                category = None
                if isinstance(row_id, tuple):
                    if len(row_id)>0:
                        strain_acc = row_id[0]
                    if len(row_id)>1:
                        category = row_id[1]
                else:
                    strain_acc = row_id
                if category == None:
                    category = strain_acc	#make them same if category is not available
                strain_acc_list.append(strain_acc)
                category_list.append(category)
            if self.strain_acc_list is None:
                self.strain_acc_list = strain_acc_list
            if self.category_list is None:
                self.category_list = category_list
        write_data_matrix(self.data_matrix, output_fname, self.header, self.strain_acc_list, self.category_list, **keywords)
    
    def PCAOnDataMatrix(self, outputFname=None, noOfPCsToOutput=4, toNormalize=False):
        """
        2016.03.28 added argument "normalize"
        2012.8.24
        """
        sys.stderr.write("Carrying out PCA on data_matrix ...")
        from palos.algorithm.PCA import PCA
        #T, P, explained_var = pca_module.PCA_svd(phenData_trans.data_matrix, standardize=True)
        T, P, explained_var = PCA.eig(self.data_matrix, toNormalize=toNormalize)	#normalize=True causes missing value in the covariance matrix
        if outputFname:
            #import csv
            #writer = csv.writer(open(outputFname, 'w'), delimiter='\t')
            from palos.io import MatrixFile
            writer = MatrixFile(outputFname, mode='w', delimiter='\t')


            header = ['rowID|string', 'DummyTime|string']
            for i in range(noOfPCsToOutput):
                header.append('PC%s'%(i+1))
            writer.writeHeader(header)
            for i in range(min(len(self.row_id_ls), T.shape[0])):
                row_id = self.row_id_ls[i]
                if hasattr(T, 'mask'):
                    TVector = T[i, 0:noOfPCsToOutput].tolist()
                else:
                    TVector = T[i,0:noOfPCsToOutput]
                data_row = [row_id, '2011'] + list(TVector)
                writer.writeRow(data_row)
            del writer
        sys.stderr.write("Done.\n")
        return PassingData(T=T, P=P, explained_var=explained_var)
    
    def reOrderRowsGivenNewRowIDList(self, row_id_ls=None):
        """
        2012.8.24
        """
        snpData = SNPData(row_id_ls=copy.deepcopy(row_id_ls), col_id_ls=copy.deepcopy(self.col_id_ls),\
                        data_matrix=copy.deepcopy(self.data_matrix))
        for i in range(len(row_id_ls)):
            row_id = row_id_ls[i]
            
            oldRowIndex = self.row_id2row_index.get(row_id)
            snpData.data_matrix[i,:] = self.data_matrix[oldRowIndex, :]
        return snpData

    def reOrderColsGivenNewCOlIDList(self, col_id_ls=None):
        """
        2012.8.24
        """
        snpData = SNPData(row_id_ls=copy.deepcopy(self.row_id_ls), col_id_ls=copy.deepcopy(col_id_ls), \
                        data_matrix=copy.deepcopy(self.data_matrix))
        for i in range(len(col_id_ls)):
            col_id = col_id_ls[i]
            
            oldColIndex = self.col_id2col_index.get(col_id)
            snpData.data_matrix[:, i] = self.data_matrix[:, oldColIndex]
        return snpData
    
    @classmethod
    def removeRowsByMismatchRate(cls, snpData, row_id2NA_mismatch_rate, max_mismatch_rate=1):
        """
        2010-3-31
            call keepRowsByRowIndex() to do the actual work.
        2008-05-19
            more robust handling given max_mismatch_rate
        2008-05-19
        """
        sys.stderr.write("Removing rows whose mismatch_rate >%s ..."%(max_mismatch_rate))
        if max_mismatch_rate>=0 and max_mismatch_rate<1:
            row_id_wanted_set = set()	#extra computing time a bit, but to save memory
            for row_id in snpData.row_id_ls:
                if row_id in row_id2NA_mismatch_rate and row_id2NA_mismatch_rate[row_id][1]<=max_mismatch_rate and row_id2NA_mismatch_rate[row_id][1]>=0:
                    row_id_wanted_set.add(row_id)
        elif max_mismatch_rate>=1:	#every row is wanted
            row_id_wanted_set = set(snpData.row_id_ls)
        else:
            row_id_wanted_set = set()
        no_of_rows = len(row_id_wanted_set)
        row_index_ls = []
        for i in range(len(snpData.row_id_ls)):
            row_id = snpData.row_id_ls[i]
            if row_id in row_id_wanted_set:
                row_index_ls.append(i)
        no_of_rows_filtered_by_mismatch = len(snpData.row_id_ls)-no_of_rows
        sys.stderr.write("%s rows filtered by mismatch. Now call keepRowsByRowIndex() to do actual work.\n"%(no_of_rows_filtered_by_mismatch))
        return cls.keepRowsByRowIndex(snpData, row_index_ls)
    
    @classmethod
    def removeRowsByNARate(cls, snpData, max_NA_rate=1):
        """
        2010-3-31
            call keepRowsByRowIndex() to do the actual work.
        2008-05-19
            add is_cutoff_max to FilterStrainSNPMatrix.remove_rows_with_too_many_NAs
        2008-05-19
            if max_NA_rate out of [0,1) range, no calculation
        2008-05-19
        """
        sys.stderr.write("Removing rows whose NA_rate >%s ..."%(max_NA_rate))
        if max_NA_rate<1 and max_NA_rate>=0:
            remove_rows_data = cls._remove_rows_with_too_many_NAs(snpData.data_matrix, max_NA_rate, is_cutoff_max=1)
            rows_with_too_many_NAs_set = remove_rows_data.rows_with_too_many_NAs_set
        elif max_NA_rate>=1:	#no row has too many NA sets
            rows_with_too_many_NAs_set = set()
        else:
            rows_with_too_many_NAs_set = set(range(len(snpData.row_id_ls)))
        row_index_ls = []
        for i in range(len(snpData.row_id_ls)):
            row_id = snpData.row_id_ls[i]
            if i not in rows_with_too_many_NAs_set:
                row_index_ls.append(i)
        no_of_rows_filtered_by_na = len(rows_with_too_many_NAs_set)
        sys.stderr.write("%s rows filtered by NA. Now call keepRowsByRowIndex() to do actual work.\n"%(no_of_rows_filtered_by_na))
        return cls.keepRowsByRowIndex(snpData, row_index_ls)
    
    @classmethod
    def keepRowsByRowID(cls, snpData, row_id_ls):
        """
        2010-3-31
            call keepRowsByRowIndex() to do the actual work.
        2010-2-2
            fix the bug that newSnpData was initiated with an empty row_id_ls, which results in an empty row_id2row_index.
        2009-05-19
            keep certain rows in snpData given row_id_ls
        """
        sys.stderr.write("Keeping rows given row_id_ls ...")
        no_of_rows = len(row_id_ls)
        row_id_wanted_set = set(row_id_ls)
        row_index_ls = []
        for i in range(len(snpData.row_id_ls)):
            row_id = snpData.row_id_ls[i]
            if row_id in row_id_wanted_set:
                row_index_ls.append(i)
        no_of_rows_removed = len(snpData.row_id_ls)-no_of_rows
        sys.stderr.write("%s rows discarded. Now call keepRowsByRowIndex() to do actual work.\n"%(no_of_rows_removed))
        return cls.keepRowsByRowIndex(snpData, row_index_ls)
    
    def removeRowsNotInTargetSNPData(self, tgSNPData):
        """
        2010-4-1
            removes rows whose ids are not in tgSNPData.row_id_ls
        """
        sys.stderr.write("Removing rows not in 2nd snpData ...")
        row_index_ls = []
        tg_snp_row_id_set = set(tgSNPData.row_id_ls)
        no_of_total  = len(self.row_id_ls)
        for i in range(no_of_total):
            row_id = self.row_id_ls[i]
            if row_id in tg_snp_row_id_set:
                row_index_ls.append(i)
        no_of_rows_kept = len(row_index_ls)
        sys.stderr.write("%s out of %s rows kept. Now call keepRowsByRowIndex() to do actual work.\n"%(no_of_rows_kept, no_of_total))
        return self.keepRowsByRowIndex(self, row_index_ls)
    
    def getSortedNegativeMissingCount(self, row_id2missing_data, to_be_removed_row_id_set):
        """
        """
        negative_missing_count_row_id_ls = []
        for row_id, missing_data in row_id2missing_data.items():
            if row_id not in to_be_removed_row_id_set:
                negative_missing_count = -missing_data.missing_count
                negative_missing_count_row_id_ls.append((negative_missing_count, row_id))
        negative_missing_count_row_id_ls.sort()
        return negative_missing_count_row_id_ls
    
    def removeRowsSoThatMatrixHasNoMissingData(self, missingDataValue=-1):
        """
        2012.2.17
            the matrix has to be symmetric.
            
            a greedy algorithm.
            #. it starts by removing the row with the most missing cells
                #. update the missing count for all other rows that have missing data in their pairing with that removed row/column (symmetric matrix)
            #.
        """
        sys.stderr.write("Removing row/column(s) so that no missing cells exist in the data matrix ...  ")
        from palos import PassingData
        row_id2missing_data = {}
        no_of_missing_cells = 0
        no_of_rows = len(self.row_id_ls)
        no_of_cols = len(self.col_id_ls)
        if no_of_rows!=no_of_cols:
            sys.stderr.write("matrix is not symmetric. no_of_rows=%s, no_of_cols=%s. Skip.\n"%(no_of_rows, no_of_cols))
            return
        for i in range(no_of_rows):
            for j in range(i+1, no_of_rows):
                if self.data_matrix[i][j]==missingDataValue:
                    row_i_id = self.row_id_ls[i]
                    row_j_id = self.row_id_ls[j]
                    if row_i_id not in row_id2missing_data:
                        row_id2missing_data[row_i_id] = PassingData(missing_index_ls=[], missing_count=0)
                    if row_j_id not in row_id2missing_data:
                        row_id2missing_data[row_j_id] = PassingData(missing_index_ls=[], missing_count=0)
                    row_id2missing_data[row_i_id].missing_index_ls.append(j)
                    row_id2missing_data[row_i_id].missing_count += 1
                    row_id2missing_data[row_j_id].missing_index_ls.append(i)
                    row_id2missing_data[row_j_id].missing_count += 1
                    
                    no_of_missing_cells += 1
        
        sys.stderr.write("%s missing cells.\n"%(no_of_missing_cells))
        
        to_be_removed_row_id_set = set()
        negative_missing_count_row_id_ls = self.getSortedNegativeMissingCount(row_id2missing_data, to_be_removed_row_id_set)
        
        while len(negative_missing_count_row_id_ls)>0 and negative_missing_count_row_id_ls[0][0]<0:
            negative_missing_count, row_id = negative_missing_count_row_id_ls.pop(0)
            to_be_removed_row_id_set.add(row_id)
            missing_index_ls = row_id2missing_data.get(row_id).missing_index_ls
            for row_index in missing_index_ls:
                row_id = self.row_id_ls[row_index]
                if row_id not in to_be_removed_row_id_set:	#otherwise it's already removed
                    row_id2missing_data[row_id].missing_count -= 1
            negative_missing_count_row_id_ls = self.getSortedNegativeMissingCount(row_id2missing_data, to_be_removed_row_id_set)
        
        new_row_id_ls = []
        slice_index_ls = []
        for i in range(no_of_rows):
            row_id = self.row_id_ls[i]
            if row_id in to_be_removed_row_id_set:
                continue
            else:
                slice_index_ls.append(i)
                new_row_id_ls.append(row_id)
        newSNPData = SNPData(row_id_ls=new_row_id_ls, col_id_ls=new_row_id_ls, data_matrix = self.data_matrix[slice_index_ls,:][:,slice_index_ls])
        
        sys.stderr.write("\t %s rows to be removed.\n"%(len(to_be_removed_row_id_set)))
        return newSNPData
    
    @classmethod
    def keepRowsWhoseOneColMatchValue(cls, snpData, col_id, col_value):
        """
        2010-03-26
            select rows based on the value of one column
        """
        sys.stderr.write("Keeping rows whose column %s has this value %s ..."%(col_id, col_value))
        col_index = snpData.col_id2col_index[col_id]
        row_index_ls = []
        for i in range(len(snpData.row_id_ls)):
            if snpData.data_matrix[i,col_index] == col_value:
                row_index_ls.append(i)
        no_of_rows_kept = len(row_index_ls)
        no_of_rows_tossed = len(snpData.row_id_ls) - no_of_rows_kept
        sys.stderr.write("%s rows kept, %s rows tossed.\n"%(no_of_rows_kept, no_of_rows_tossed))
        return cls.keepRowsByRowIndex(snpData, row_index_ls)
    
    @classmethod
    def keepRowsByRowIndex(cls, snpData, row_index_ls):
        """
        2010-3-26
            initiate the data matrix with the same type as snpData.data_matrix (to deal with  character arrays) or it's a list
        2010-2-2
            fix the bug that newSnpData was initiated with an empty row_id_ls, which results in an empty row_id2row_index.
            keep certain rows in snpData given row_index_ls
        """
        sys.stderr.write("Keeping rows given row_index_ls ...")
        no_of_rows = len(row_index_ls)
        row_index_wanted_set = set(row_index_ls)
        
        no_of_cols = len(snpData.col_id_ls)
        new_col_id_ls = copy.deepcopy(snpData.col_id_ls)
        new_row_id_ls = []
        if type(snpData.data_matrix) == list:
            new_data_matrix = []
        else:
            new_data_matrix = num.copy(snpData.data_matrix[:no_of_rows,:no_of_cols])	# 2010-3-26 make sure it's of same data type
            #new_data_matrix = num.zeros([no_of_rows, no_of_cols], snpData.data_matrix.dtype)
        row_index = 0
        for i in range(len(snpData.row_id_ls)):
            row_id = snpData.row_id_ls[i]
            if i in row_index_wanted_set:
                new_row_id_ls.append(row_id)
                if type(new_data_matrix)==list:
                    new_data_matrix.append(snpData.data_matrix[i])
                else:
                    new_data_matrix[row_index] = snpData.data_matrix[i]
                row_index += 1
        newSnpData = SNPData(col_id_ls=new_col_id_ls, row_id_ls=new_row_id_ls, data_matrix=new_data_matrix,\
                            turn_into_array=snpData.turn_into_array, ignore_2nd_column=snpData.ignore_2nd_column, \
                            data_starting_col=snpData.data_starting_col, turn_into_integer=snpData.turn_into_integer)
        newSnpData.no_of_rows_removed = len(snpData.row_id_ls)-no_of_rows
        sys.stderr.write("%s rows discarded. Done.\n"%(newSnpData.no_of_rows_removed))
        return newSnpData
    
    @classmethod
    def removeColsByMismatchRate(cls, snpData, col_id2NA_mismatch_rate, max_mismatch_rate=1):
        """
        2010-2-2
            fix the bug that newSnpData was initiated with an empty col_id_ls, which results in an empty col_id2col_index.
        2008-05-19
            more robust handling given max_mismatch_rate
            fix a bug. mismatch rate could be -1 which is no-comparison
        2008-05-19
        """
        sys.stderr.write("Removing cols whose mismatch_rate >%s ..."%(max_mismatch_rate))
        if max_mismatch_rate>=0 and max_mismatch_rate<1:
            col_id_wanted_set = set()	#extra computing time a bit, but to save memory
            for col_id in snpData.col_id_ls:
                if col_id in col_id2NA_mismatch_rate and col_id2NA_mismatch_rate[col_id][1]<=max_mismatch_rate and col_id2NA_mismatch_rate[col_id][1]>=0:
                    col_id_wanted_set.add(col_id)
        elif max_mismatch_rate>=1:
            col_id_wanted_set = set(snpData.col_id_ls)
        else:
            col_id_wanted_set = set()
        
        no_of_cols = len(col_id_wanted_set)
        no_of_rows = len(snpData.row_id_ls)
        newSnpData = SNPData(col_id_ls=[], row_id_ls=snpData.row_id_ls)
        newSnpData.data_matrix = num.zeros([no_of_rows, no_of_cols], num.int8)
        col_index = 0
        for i in range(len(snpData.col_id_ls)):
            col_id = snpData.col_id_ls[i]
            if col_id in col_id_wanted_set:
                newSnpData.col_id_ls.append(col_id)
                newSnpData.data_matrix[:,col_index] = snpData.data_matrix[:,i]
                col_index += 1
        newSnpData.no_of_cols_filtered_by_mismatch = len(snpData.col_id_ls)-no_of_cols
        newSnpData.processRowIDColID()	# 2010-2-2 to initiate a new row_id2row_index since row_id_ls is changed
        sys.stderr.write("%s columns filtered by mismatch. Done.\n"%(newSnpData.no_of_cols_filtered_by_mismatch))
        return newSnpData
    
    
    @classmethod
    def _remove_rows_with_too_many_NAs(cls, data_matrix, row_cutoff=0, cols_with_too_many_NAs_set=None, NA_set=set([0, -2]), \
                                    debug=0, is_cutoff_max=0):
        """
        2013.07.03 rename row_index2no_of_NAs to row_index2missing_fraction
        2013.1.16 moved from variation/src/qc/FilterStrainSNPMatrix
        2008-05-19
            if is_cutoff_max=1, anything > row_cutoff is deemed as having too many NAs
            if is_cutoff_max=0 (cutoff is minimum), anything >= row_cutoff is deemed as having too many NAs
        2008-05-12
            made more robust
            add cols_with_too_many_NAs_set
            add NA_set
        2008-05-08
            become classmethod
        """
        sys.stderr.write("Removing rows with NA rate >= %s ..."%(row_cutoff))
        no_of_rows, no_of_cols = data_matrix.shape
        rows_with_too_many_NAs_set = set()
        total_cols_set = set(range(no_of_cols))
        if cols_with_too_many_NAs_set:
            cols_to_be_checked = total_cols_set - cols_with_too_many_NAs_set
        else:
            cols_to_be_checked = total_cols_set
        row_index2missing_fraction = {}
        for i in range(no_of_rows):
            no_of_NAs = 0.0
            for j in cols_to_be_checked:
                if data_matrix[i][j] in NA_set:
                    no_of_NAs += 1
            if no_of_cols!=0:
                NA_ratio = no_of_NAs/no_of_cols
            else:
                NA_ratio = 0.0
            row_index2missing_fraction[i] = NA_ratio
            if is_cutoff_max:
                if NA_ratio > row_cutoff:
                    rows_with_too_many_NAs_set.add(i)
            else:
                if NA_ratio >= row_cutoff:
                    rows_with_too_many_NAs_set.add(i)
        if debug:
            print
            print('rows_with_too_many_NAs_set')
            print(rows_with_too_many_NAs_set)
        passingdata = PassingData(rows_with_too_many_NAs_set=rows_with_too_many_NAs_set, row_index2missing_fraction=row_index2missing_fraction)
        sys.stderr.write("%s strains removed, done.\n"%len(rows_with_too_many_NAs_set))
        return passingdata
    
    @classmethod
    def _remove_cols_with_too_many_NAs(cls, data_matrix, col_cutoff=0, rows_with_too_many_NAs_set=None, NA_set=set([0, -2]), \
                                    debug=0, is_cutoff_max=0):
        """
            argument rows_with_too_many_NAs_set is used to exclude rows in calculating NA rate for each column
        2013.07.03 rename col_index2no_of_NAs to col_index2missing_fraction
        2013.1.16 moved from variation/src/qc/FilterStrainSNPMatrix
        2008-05-19
            if is_cutoff_max=1, anything > row_cutoff is deemed as having too many NAs
            if is_cutoff_max=0 (cutoff is minimum), anything >= row_cutoff is deemed as having too many NAs
        2008-05-12
            classmethod
            more robust, standardize
            add NA_set
        """
        sys.stderr.write("Removing columns with NA rate>=%s ..."%col_cutoff)
        no_of_rows, no_of_cols = data_matrix.shape
        cols_with_too_many_NAs_set = set()
        total_rows_set = set(range(no_of_rows))
        if rows_with_too_many_NAs_set:
            rows_to_be_checked = total_rows_set - rows_with_too_many_NAs_set
        else:
            rows_to_be_checked = total_rows_set
        
        col_index2missing_fraction = {}
        
        for j in range(no_of_cols):
            no_of_NAs = 0.0
            for i in rows_to_be_checked:
                if data_matrix[i][j] in NA_set:
                    no_of_NAs += 1
            if no_of_rows!=0:
                NA_ratio = no_of_NAs/no_of_rows
            else:
                NA_ratio = 0.0
            col_index2missing_fraction[j] = NA_ratio
            if is_cutoff_max:
                if NA_ratio > col_cutoff:
                    cols_with_too_many_NAs_set.add(j)
            else:
                if NA_ratio >= col_cutoff:
                    cols_with_too_many_NAs_set.add(j)
        if debug:
            print
            print('cols_with_too_many_NAs_set')
            print(cols_with_too_many_NAs_set)
        passingdata = PassingData(cols_with_too_many_NAs_set=cols_with_too_many_NAs_set, col_index2missing_fraction=col_index2missing_fraction)
        sys.stderr.write("%s cols removed, done.\n"%(len(cols_with_too_many_NAs_set)))
        return passingdata
    
    @classmethod
    def removeColsByNARate(cls, snpData, max_NA_rate=1):
        """
        2010-2-2
            fix the bug that newSnpData was initiated with an empty col_id_ls, which results in an empty col_id2col_index.
        2008-05-19
            add is_cutoff_max to FilterStrainSNPMatrix.remove_cols_with_too_many_NAs()
        2008-05-19
            if max_NA_rate out of [0,1) range, no calculation
        2008-05-19
        """
        sys.stderr.write("Removing cols whose NA_rate >%s ..."%(max_NA_rate))
        if max_NA_rate<1 and max_NA_rate>=0:
            remove_cols_data = cls._remove_cols_with_too_many_NAs(snpData.data_matrix, max_NA_rate, is_cutoff_max=1)
            cols_with_too_many_NAs_set = remove_cols_data.cols_with_too_many_NAs_set
        elif max_NA_rate>=1:
            cols_with_too_many_NAs_set = set()
        else:
            cols_with_too_many_NAs_set = set(range(len(snpData.col_id_ls)))
        
        no_of_cols = len(snpData.col_id_ls)-len(cols_with_too_many_NAs_set)
        no_of_rows = len(snpData.row_id_ls)
        newSnpData = SNPData(row_id_ls=snpData.row_id_ls, col_id_ls=[])
        newSnpData.data_matrix = num.zeros([no_of_rows, no_of_cols], num.int8)
        col_index = 0
        for i in range(len(snpData.col_id_ls)):
            col_id = snpData.col_id_ls[i]
            if i not in cols_with_too_many_NAs_set:
                newSnpData.col_id_ls.append(col_id)
                newSnpData.data_matrix[:,col_index] = snpData.data_matrix[:,i]
                col_index += 1
        newSnpData.processRowIDColID()	# to initiate a new row_id2row_index since row_id_ls is changed
        newSnpData.no_of_cols_filtered_by_na = len(cols_with_too_many_NAs_set)
        sys.stderr.write("%s columns filtered by NA. Done.\n"%(newSnpData.no_of_cols_filtered_by_na))
        return newSnpData
    
    @classmethod
    def removeColsByMAF(cls, snpData, min_MAF=1, NA_set =set([0, 'NA', 'N', -2, '|'])):
        """
        2012.2.29
            added the NA_set argument
        2008-05-29
            remove SNPs whose MAF is lower than min_MAF
        """
        sys.stderr.write("Removing cols whose MAF <%s ..."%(min_MAF))
        
        no_of_rows = len(snpData.data_matrix)
        no_of_cols = len(snpData.data_matrix[0])
        allele2index_ls = []
        allele2count_ls = []
        allele_index2allele_ls = []
        col_id_to_be_kept_ls = []
        no_of_SNPs_with_more_than_2_alleles = 0
        for j in range(no_of_cols):
            col_id = snpData.col_id_ls[j]
            allele2index_ls.append({})
            allele2count_ls.append({})
            allele_index2allele_ls.append({})
            allele_index2allele = allele_index2allele_ls[j]
            for i in range(no_of_rows):
                allele = snpData.data_matrix[i][j]
                if allele in NA_set:
                    allele_index = num.nan	#numpy.nan is better than -2
                elif allele not in allele2index_ls[j]:
                    allele_index = len(allele2index_ls[j])
                    allele2index_ls[j][allele] = allele_index
                    allele2count_ls[j][allele] = 1
                    allele_index2allele[allele_index] = allele
                else:
                    allele_index = allele2index_ls[j][allele]
                    allele2count_ls[j][allele] += 1
                #if cls.report and allele_index>1:
                #	sys.stderr.write("%s (more than 2) alleles at SNP %s (id=%s).\n"%((allele_index+1), j, snpData.col_id_ls[j]))
            if len(allele2count_ls[j])>2:
                no_of_SNPs_with_more_than_2_alleles += 1
                if cls.report:
                    sys.stderr.write("Warning: more than 2 alleles at SNP %s (id=%s).\n"%(j, snpData.col_id_ls[j]))
            MAF = min(allele2count_ls[j].values())/float(sum(allele2count_ls[j].values()))
            """
            print(MAF)
            print(j)
            print(snpData.col_id_ls[j])
            print(allele2count_ls[j])
            """
            if MAF>=min_MAF:
                col_id_to_be_kept_ls.append(col_id)
        
        newSnpData = cls.keepColsByColID(snpData, col_id_to_be_kept_ls)
        newSnpData.no_of_cols_removed = no_of_cols - len(col_id_to_be_kept_ls)
        sys.stderr.write("%s columns filtered by min_MAF and %s SNPs with >2 alleles. Done.\n"%(newSnpData.no_of_cols_removed, no_of_SNPs_with_more_than_2_alleles))
        return newSnpData
    
    @classmethod
    def removeMonomorphicCols(cls, snpData, NA_set =set([0, 'NA', 'N', -2, '|'])):
        """
        2012.2.29
            added the NA_set argument
        2010-2-2
            fix the bug that newSnpData was initiated with an empty col_id_ls, which results in an empty col_id2col_index.
        2008-05-19
        """
        sys.stderr.write("Removing monomorphic cols ...")
        no_of_rows, no_of_cols = snpData.data_matrix.shape
        #NA_set = set([0,-1,-2])
        col_index_wanted_ls = []
        for j in range(no_of_cols):
            non_negative_number_set = set()
            for i in range(no_of_rows):
                number = snpData.data_matrix[i][j]
                if number not in NA_set:
                    non_negative_number_set.add(number)
            if len(non_negative_number_set)>1:	#not monomorphic
                col_index_wanted_ls.append(j)
        
        newSnpData = SNPData(row_id_ls=snpData.row_id_ls, col_id_ls=[])
        newSnpData.data_matrix = num.zeros([no_of_rows, len(col_index_wanted_ls)], num.int8)
        col_index = 0
        for i in col_index_wanted_ls:
            col_id = snpData.col_id_ls[i]
            newSnpData.col_id_ls.append(col_id)
            newSnpData.data_matrix[:,col_index] = snpData.data_matrix[:,i]
            col_index += 1
        newSnpData.processRowIDColID()	# to initiate a new row_id2row_index since row_id_ls is changed
        newSnpData.no_of_monomorphic_cols = no_of_cols-len(newSnpData.col_id_ls)
        sys.stderr.write("%s monomorphic columns. Done.\n"%(newSnpData.no_of_monomorphic_cols))
        return newSnpData
    
    @classmethod
    def keepColsByColID(cls, snpData, col_id_ls=None, dataType=num.int8):
        """
        2012.9.1 add argument dataType
        2010-2-2
            fix the bug that newSnpData was initiated with an empty col_id_ls, which results in an empty col_id2col_index.
        2009-05-29
            keep certain columns in snpData given col_id_ls
        """
        sys.stderr.write("Keeping columns given col_id_ls ...")
        no_of_cols = len(col_id_ls)
        col_id_wanted_set = set(col_id_ls)
        
        no_of_rows = len(snpData.row_id_ls)
        newSnpData = SNPData(row_id_ls=copy.deepcopy(snpData.row_id_ls), col_id_ls=[])
        newSnpData.data_matrix = num.zeros([no_of_rows, no_of_cols], dataType)
        col_index = 0
        for j in range(len(snpData.col_id_ls)):
            col_id = snpData.col_id_ls[j]
            if col_id in col_id_wanted_set:
                newSnpData.col_id_ls.append(col_id)
                newSnpData.data_matrix[:,col_index] = snpData.data_matrix[:, j]
                col_index += 1
        newSnpData.no_of_cols_removed = len(snpData.col_id_ls)-no_of_cols
        newSnpData.processRowIDColID()	# to initiate a new row_id2row_index since row_id_ls is changed
        sys.stderr.write("%s columns discarded. Done.\n"%(newSnpData.no_of_cols_removed))
        return newSnpData
    
    def convertSNPIDToChrPos(self, db):
        """
        2013.3.6 bugfix
        2011-03-10 (not tested)
            assuming col_id is Snps.id, and convert them into chr_pos through db (stock_250k).
            If col_id is already chr_pos format, no conversion.
            A new SNPData is generated in the end.
        """
        #2011-2-27 translate the db_id into chr_pos because the new StrainXSNP dataset uses db_id to identify SNPs.
        # but if col-id is already chr_pos, it's fine.
        new_col_id_ls = []
        data_matrix_col_index_to_be_kept = []
        for i in range(len(self.col_id_ls)):
            snp_id = self.col_id_ls[i]
            chr_pos = db.get_chr_pos_given_db_id2chr_pos(snp_id,)
            if chr_pos is not None:
                data_matrix_col_index_to_be_kept.append(i)
                new_col_id_ls.append(chr_pos)
        
        # to remove no-db_id columns from data matrix
        #data_matrix = numpy.array(self.data_matrix)
        data_matrix = self.data_matrix[:, data_matrix_col_index_to_be_kept]
        
        no_of_rows = len(self.row_id_ls)
        newSnpData = SNPData(row_id_ls=copy.deepcopy(self.row_id_ls), col_id_ls=new_col_id_ls)
        newSnpData.data_matrix = data_matrix
        no_of_cols = len(newSnpData.col_id_ls)
        newSnpData.no_of_cols_removed = len(self.col_id_ls)-no_of_cols
        newSnpData.processRowIDColID()	# to initiate a new row_id2row_index since row_id_ls is changed
        sys.stderr.write("%s columns discarded.\n"%(newSnpData.no_of_cols_removed))
        return newSnpData
    
    @classmethod
    def convertHetero2NA(cls, snpData):
        """
        2009-5-29
            bug: previously, no_of_hets includes NA calls. now it doesn't
        2008-06-02
            Convert all heterozygous calls and untouched in the file into NA.
            deletion is not converted
        """
        sys.stderr.write("Converting Hetero calls to NA ...")
        no_of_hets = 0
        newSnpData = SNPData(row_id_ls=snpData.row_id_ls, col_id_ls=snpData.col_id_ls)
        no_of_rows, no_of_cols = snpData.data_matrix.shape
        newSnpData.data_matrix = num.zeros([no_of_rows, no_of_cols], num.int8)
        for i in range(no_of_rows):
            for j in range(no_of_cols):
                if snpData.data_matrix[i][j]<=4 and snpData.data_matrix[i][j]>=1:
                    newSnpData.data_matrix[i][j] = snpData.data_matrix[i][j]
                elif snpData.data_matrix[i][j]==-1:	#but not -2 (untouched), -1=deletion
                    newSnpData.data_matrix[i][j] = snpData.data_matrix[i][j]
                elif snpData.data_matrix[i][j]>4:	#-2 and 0 all converted to 0 by default
                    no_of_hets += 1
        sys.stderr.write("%s heterozygous calls. Done.\n"%no_of_hets)
        return newSnpData
    
    @classmethod
    def removeSNPsWithMoreThan2Alleles(cls, snpData):
        """
        2010-2-2
            fix the bug that newSnpData was initiated with an empty col_id_ls, which results in an empty col_id2col_index.
        2008-08-05
            NA and -2 (not touched) are not considered as an allele
        """
        sys.stderr.write("Removing SNPs with more than 2 alleles ...")
        no_of_rows, no_of_cols = snpData.data_matrix.shape
        col_index_wanted_ls = []
        for j in range(no_of_cols):
            allele_set = set(snpData.data_matrix[:,j])
            if 0 in allele_set:	#remove NA if it's there
                allele_set.remove(0)
            if -2 in allele_set:	#remove -2 as well
                allele_set.remove(-2)
            if len(allele_set)==2:	#polymorphic
                col_index_wanted_ls.append(j)
        
        newSnpData = SNPData(row_id_ls=snpData.row_id_ls, col_id_ls=[])
        newSnpData.data_matrix = num.zeros([no_of_rows, len(col_index_wanted_ls)], num.int8)
        col_index = 0
        for i in col_index_wanted_ls:
            col_id = snpData.col_id_ls[i]
            newSnpData.col_id_ls.append(col_id)
            newSnpData.data_matrix[:,col_index] = snpData.data_matrix[:,i]
            col_index += 1
        newSnpData.processRowIDColID()	# to initiate a new row_id2row_index since row_id_ls is changed
        newSnpData.no_of_cols_removed = no_of_cols-len(newSnpData.col_id_ls)
        sys.stderr.write("%s columns removed. Done.\n"%(newSnpData.no_of_cols_removed))
        return newSnpData
    
    def fill_in_snp_allele2index(self, diploid_allele, allele2index):
        """
        2008-09-05
            used in calLD
        """
        if diploid_allele>4:
            nt = number2nt[diploid_allele]
            allele1 = nt2number[nt[0]]
            allele2 = nt2number[nt[1]]
        else:
            allele1 = allele2 = diploid_allele
        if allele1 not in allele2index:
            allele2index[allele1] = len(allele2index)
        if allele2 not in allele2index:
            allele2index[allele2] = len(allele2index)
        return allele1, allele2
    
    def calLD(self, col1_id, col2_id):
        """
        2008-09-05
            adapted from variation.src.misc's LD.calculate_LD class
            only deal with 2-allele loci
            skip if either is NA, or if both are heterozygous (not phased)
        """
        snp1_index = self.col_id2col_index[col1_id]
        snp2_index = self.col_id2col_index[col2_id]
        counter_matrix = num.zeros([2,2])	#only 2 alleles
        snp1_allele2index = {}
        snp2_allele2index = {}
        for k in range(len(self.row_id_ls)):
            snp1_allele = self.data_matrix[k][snp1_index]
            snp2_allele = self.data_matrix[k][snp2_index]
            if snp1_allele!=0 and snp2_allele!=0 and not (snp1_allele>4 and snp2_allele>4):	#doesn't allow both loci are heterozygous
                snp1_allele1, snp1_allele2 = self.fill_in_snp_allele2index(snp1_allele, snp1_allele2index)
                snp2_allele1, snp2_allele2 = self.fill_in_snp_allele2index(snp2_allele, snp2_allele2index)
                counter_matrix[snp1_allele2index[snp1_allele1],snp2_allele2index[snp2_allele1]] += 1
                counter_matrix[snp1_allele2index[snp1_allele2],snp2_allele2index[snp2_allele2]] += 1
        PA = sum(counter_matrix[0,:])
        Pa = sum(counter_matrix[1,:])
        PB = sum(counter_matrix[:,0])
        Pb = sum(counter_matrix[:,1])
        total_num = float(PA+Pa)
        try:
            PA = PA/total_num
            Pa = Pa/total_num
            PB = PB/total_num
            Pb = Pb/total_num
            PAB = counter_matrix[0,0]/total_num
            D = PAB-PA*PB
            PAPB = PA*PB
            PAPb = PA*Pb
            PaPB = Pa*PB
            PaPb = Pa*Pb
            Dmin = max(-PAPB, -PaPb)
            Dmax = min(PAPb, PaPB)
            if D<0:
                D_prime = D/Dmin
            else:
                D_prime = D/Dmax
            r2 = D*D/(PA*Pa*PB*Pb)
        except:	#2008-01-23 exceptions.ZeroDivisionError, Dmin or Dmax could be 0 if one of(-PAPB, -PaPb)  is >0 or <0
            sys.stderr.write('Unknown except, ignore: %s\n'%repr(sys.exc_info()[0]))
            return None
        allele_freq = (min(PA, Pa),min(PB, Pb))
        return_data = PassingData()
        return_data.D = D
        return_data.D_prime = D_prime
        return_data.r2 = r2
        return_data.allele_freq = allele_freq
        return_data.snp_pair_ls = (col1_id, col2_id)
        return_data.no_of_pairs = total_num
        return return_data
    
    def calGeneralLD(self, col1_id, col2_id):
        """
        2010-9-30
            like calLD() but doesn't require the alleles are encoded in integer according to nt2number.
        """
        from palos.algorithm import LD
        snp1_index = self.col_id2col_index[col1_id]
        snp2_index = self.col_id2col_index[col2_id]
        return LD.calLD(self.data_matrix[:, snp1_index], self.data_matrix[:, snp2_index])
        
    
    def calRowPairwiseDist(self, NA_set =set([0, 'NA', 'N', -2, '|']), ref_row_id=None, assumeBiAllelic=False,
                        outputFname=None, hetHalfMatchDistance=0.5):
        """
        2011-10-20
            call function calDistOfTwoHetCallsInNumber()
            add argument hetHalfMatchDistance (default = 0.5). it's applied between two heterozygous calls or one het + one homo.
            
        2011-3-31
            add argument outputFname
                if given, output row_id2pairwise_dist to it.
        2010-10-23
            add argument NA_set and ref_row_id
        2009-4-18
            calculate distance between all rows except itself.
            only calculate half non-redundant pairs.
        """
        sys.stderr.write("Calculating row-wise pairwise distance ...")
        row_id2pairwise_dist = {}
        counter = 0
        
        for i in range(len(self.row_id_ls)):
            row_id1 = self.row_id_ls[i]
            pairwise_dist = []
            for j in range(i+1, len(self.row_id_ls)):
                row_id2 = self.row_id_ls[j]
                if ref_row_id is not None and row_id1!=ref_row_id and row_id2!=ref_row_id:
                    #ignore this pair if neither of them is ref_row_id
                    continue
                no_of_mismatches = 0.0
                no_of_non_NA_pairs = 0
                for col_index in range(len(self.col_id_ls)):
                    row_i_allele = self.data_matrix[i][col_index]
                    row_j_allele = self.data_matrix[j][col_index]
                    if row_i_allele not in NA_set and row_j_allele not in NA_set:
                        no_of_non_NA_pairs += 1
                        if row_i_allele == row_j_allele:
                            no_of_mismatches += 0
                        elif assumeBiAllelic:
                            #one of them is heterozygous. can't be both heterozygous.
                            #assuming there is one kind of heterozygous and each locus is biallelic.
                            #no_of_mismatches += 0.5
                            no_of_mismatches += calDistOfTwoHetCallsInNumber(row_i_allele, row_j_allele, \
                                                                            hetHalfMatchDistance=hetHalfMatchDistance)
                        elif row_i_allele != row_j_allele:
                            no_of_mismatches += 1
                if no_of_non_NA_pairs>0:
                    mismatch_rate = no_of_mismatches/float(no_of_non_NA_pairs)
                else:
                    mismatch_rate = -1
                    if self.debug:
                        sys.stderr.write("\t no valid(non-NA) pairs between %s and %s.\n"%(row_id1, row_id2))
                pairwise_dist.append([mismatch_rate, row_id2, no_of_mismatches, no_of_non_NA_pairs])
            pairwise_dist.sort()
            row_id2pairwise_dist[row_id1] = pairwise_dist
        sys.stderr.write("Done.\n")
        if outputFname is not None:	#2011-3-31
            self.outputRowPairwiseDist(row_id2pairwise_dist, outputFname)
        return row_id2pairwise_dist
    
    @classmethod
    def outputRowPairwiseDist(cls, row_id2pairwise_dist=None, outputFname=None):
        """
        2011-3-31
            function to output row_id2pairwise_dist (data structure from calRowPairwiseDist())
        """
        sys.stderr.write("Outputting row pairwise distance to %s ... "%outputFname)
        import csv
        writer = csv.writer(open(outputFname, 'w'), delimiter='\t')
        for row_id, pairwise_dist in row_id2pairwise_dist.items():
            for dist in pairwise_dist:
                mismatch_rate, row_id2, no_of_mismatches, no_of_non_NA_pairs = dist[:4]
                data_row = [row_id, row_id2, mismatch_rate, no_of_mismatches, no_of_non_NA_pairs]
                writer.writerow(data_row)
        del writer
        sys.stderr.write("Done.\n")
    
    def calFractionOfLociCarryingNonRefAllelePerRow(self, ref_allele=0, NA_set =set([0, 'NA', 'N', -2, '|'])):
        """
        2010-10-23
            for example, after the SNP alleles are converted into bi-allelic, 0 is ancestral, 1 is derived,
                the fraction returned here would the fraction of derived alleles one row has.
        """
        sys.stderr.write("Calculating fraction of loci with allele !=%s for each row ..."%(ref_allele))
        row_id2fractionData = {}
        counter = 0
        
        for i in range(len(self.row_id_ls)):
            row_id1 = self.row_id_ls[i]
            no_of_mismatches = 0
            no_of_non_NA_pairs = 0
            for col_index in range(len(self.col_id_ls)):
                if self.data_matrix[i][col_index] not in NA_set:
                    no_of_non_NA_pairs += 1
                    if self.data_matrix[i][col_index] != ref_allele:
                        no_of_mismatches += 1
            if no_of_non_NA_pairs>0:
                mismatch_rate = no_of_mismatches/float(no_of_non_NA_pairs)
            else:
                mismatch_rate = -1
                if self.debug:
                    pass
            row_id2fractionData[row_id1] = [mismatch_rate, no_of_mismatches, no_of_non_NA_pairs]
        sys.stderr.write("Done.\n")
        return row_id2fractionData
    
    def convertSNPAllele2Index(self, report=0, **keywords):
        """
        2008-12-03
            set in_major_minor_order to True
        2008-12-02
            code body moved to convert2Binary()
            call convert2Binary with in_major_minor_order=False.
        2008-11-20
            newSnpData also copies self.strain_acc_list and self.category_list over.
        2008-09-07
            Convert SNP matrix into index (0,1,2...) is assigned as first-encounter, first-assign. if only two alleles, it's binary.
            heterozygote is regarded as a different allele.
        """
        return self.convert2Binary(report=report, in_major_minor_order=True, **keywords)
    
    def getRowIndexGivenRowID(self, row_id=None, row_key_index=0, ):
        """
        2010-3-31
            a helper function to find out the index of the row whose id matches row_id.
                deal with the fact that row_id could be a tuple or just one single data item
        """
        inherent_row_id_type = type(self.row_id_ls[0])
        if type(row_id)==list:	# turn it into tuple. list is not hashable. can't be used as row_id2row_index.get(row_id).
            row_id = tuple(row_id)
        designated_row_id_type = type(row_id)
        row_index = None
        if inherent_row_id_type == designated_row_id_type:	#both are same type. easy
            row_index = self.row_id2row_index.get(row_id)
        elif inherent_row_id_type == tuple and designated_row_id_type != tuple:
            for row_id in self.row_id2row_index:
                if row_id==row_id[row_key_index]:
                    row_index = self.row_id2row_index.get(row_id)
                    break
        elif inherent_row_id_type != tuple and designated_row_id_type == tuple:	#use the first element of row_id as key
            row_index = self.row_id2row_index.get(row_id[row_key_index])
        return row_index
    
    def getColIndexLsGivenQuerySet(self, query_set=None, colIDHashFunction=None):
        """
        Example:
            # phenotype_method_id_set is a set of interger phenotype method ids.
            from OutputPhenotype import OutputPhenotype
            col_index_to_return_ls = phenData.getColIndexLsGivenQuerySet(phenotype_method_id_set, \
                                                                    colIDHashFunction=OutputPhenotype.extractPhenotypeIDFromMethodIDName)
        
        2010-4-21
            a helper function to find out index of a column whose id (colIDHashFunction may be applied) is in query_set.
            a different mechanism than getRowIndexGivenRowID().
        """
        index_ls = []
        for col_id, col_index in self.col_id2col_index.items():
            if colIDHashFunction:
                col_id = colIDHashFunction(col_id)
            if col_id in query_set:	# found it
                index_ls.append(col_index)
        return index_ls
    
    def getColDataGivenColName(self, col_name, convert_type=None):
        """
        2010-4-16
            get one column data given col_name
        """
        return self.getColVectorGivenColID(col_id=col_name, convert_type=convert_type)

    def getColVectorGivenColID(self, col_id=None, convert_type=None):
        """
        2012.8.22
            similar to getColDataGivenColName, but more robust. the latter is not deleted for backwards compatiblity.
        """
        col_index = self.col_id2col_index.get(col_id)
        if col_index is not None:
            data_ls = self.data_matrix[:, col_index]
            if convert_type is not None:
                data_ls = map(convert_type, data_ls)
        else:
            data_ls = None
        return data_ls
    
    def getRowVectorGivenRowID(self, row_id=None, convert_type=None):
        """
        2012.8.22 row-version of  getColVectorGivenColID()
        """
        row_index = self.row_id2row_index.get(row_id)
        if row_index is not None:
            data_ls = self.data_matrix[row_index, :]
            if convert_type is not None:
                data_ls = map(convert_type, data_ls)
        else:
            data_ls = None
        return data_ls
    
    def getCellDataGivenRowColID(self, row_id=None, col_id=None):
        """
        2012.8.21
            helper function
        """
        row_index = self.row_id2row_index.get(row_id)
        col_index = self.col_id2col_index.get(col_id)
        if row_index is not None and col_index is not None:
            return self.data_matrix[row_index][col_index]
        else:
            return None
    
    def setCellDataGivenRowColID(self, row_id=None, col_id=None, data=None):
        """
        2012.8.21
            helper function
        """
        row_index = self.row_id2row_index.get(row_id)
        col_index = self.col_id2col_index.get(col_id)
        if row_index is not None and col_index is not None:
            self.data_matrix[row_index][col_index] = data
            return True
        else:
            return False
        
    def get_kinship_matrix(self):
        """
        2011-4-25
            moved from variation/src/Association.py
        2009-2-9
            make it classmethod
        2008-11-11
            only for binary data_matrix. identity_vector[k]=1 only when data_matrix[i,k]=data_matrix[j,k]
        """
        sys.stderr.write("Calculating kinship matrix .... ")
        no_of_rows, no_of_cols = self.data_matrix.shape
        kinship_matrix = numpy.identity(no_of_rows, numpy.float)
        for i in range(no_of_rows):
            for j in range(i+1, no_of_rows):
                #only for binary data_matrix. identity_vector[k]=1 only when data_matrix[i,k]=data_matrix[j,k]
                identity_vector = self.data_matrix[i,:]*self.data_matrix[j,:]+ (1-self.data_matrix[i,:])*(1-self.data_matrix[j,:])
                kinship_matrix[i,j] = sum(identity_vector)/float(no_of_cols)
                kinship_matrix[j,i] = kinship_matrix[i,j]
        sys.stderr.write("Done.\n")
        return kinship_matrix
    
    def codeGenotypeFromThisRowAsAllele(self, row_id_as_major_allele=None, allele_code=0, old_NA_notation_set=set([0, -2])):
        """
        2010-3-31
            use the genotypes from one row as major allele (code=allele_code) for all SNPs
            a function used by convert2Binary()
        """
        sys.stderr.write("Coding the genotype from row id=%s as allele %s ..."%(row_id_as_major_allele, allele_code))
        allele2index_ls = []
        allele_index2allele_ls = []
        row_index = self.getRowIndexGivenRowID(row_id_as_major_allele)
        no_of_coded = 0
        no_of_cols = 0
        if row_index:
            genotype_ls = self.data_matrix[row_index]
            no_of_cols = len(genotype_ls)
            for j in range(no_of_cols):
                genotype = genotype_ls[j]
                allele2index_ls.append({})
                allele_index2allele_ls.append({})
                if genotype not in old_NA_notation_set:	#exclude NA
                    no_of_coded += 1
                    allele2index_ls[j][genotype] = allele_code
                    allele_index2allele_ls[j][allele_code] = genotype
        sys.stderr.write("%s out of %s coded.\n"%(no_of_coded, no_of_cols))
        return allele2index_ls, allele_index2allele_ls
    
    def convert2Binary(self, report=0, in_major_minor_order=True, NA_notation=num.nan, alleleStartingIndex=0,\
                    row_id_as_major_allele=None, old_NA_notation_set=set([0, -2])):
        """
        Examples:
            # code the alleles as 0 and 1 in major and minor order. 
            snpData.convert2Binary()
            
            # code the alleles as 1 and 2 instead of 0 and 1 and NOT in major and minor order. new NA_notation is 0.
            snpData.convert2Binary(in_major_minor_order=False, NA_notation=0, alleleStartingIndex=1)
        
            # code the alleles in a way that genotypes from row "6909" are regarded as major allele.
            # argument in_major_minor_order is invalid in this scenario. 
            snpData.convert2Binary(row_id_as_major_allele="6909")
            
        2010-3-31
            add argument row_id_as_major_allele to assign the major allele to genotypes from certain row.
                It could be a tuple or the first column of row_id. self.getRowIndexGivenRowID() is used to handle the id-matching.
                This argument automatically invalidates argument in_major_minor_order.
            add argument old_NA_notation_set to denote which are regarded as NA in the input data.
        2010-2-28
            add argument NA_notation, default is num.nan.
            add argument alleleStartingIndex, which is the index of the first allele encountered for one SNP.
            Watch the combination of argument in_major_minor_order & NA_notation.
                If NA_notation is not num.nan and there's missing data in this SNPdata, chances are that some SNPs will have
                    major & minor allele swapped in the initial phase and their codes have to be reversed.
                    The current algorithm will mess up the NA encoding in this case.
                If there's no missing data in this SNPdata, it doesn't matter.
        2008-12-02
            based on the old convertSNPAllele2Index()
        """
        if row_id_as_major_allele is not None:
            allele2index_ls, allele_index2allele_ls = self.codeGenotypeFromThisRowAsAllele(row_id_as_major_allele,\
                                                                                        old_NA_notation_set=old_NA_notation_set)
        else:
            allele2index_ls = []
            allele_index2allele_ls = []
        sys.stderr.write("Converting SNP matrix to Binary ...")
        no_of_hets = 0
        newSnpData = SNPData(row_id_ls=self.row_id_ls, col_id_ls=self.col_id_ls)
        newSnpData.strain_acc_list = self.strain_acc_list
        newSnpData.category_list = self.category_list
        no_of_rows = len(self.data_matrix)
        no_of_cols = len(self.data_matrix[0])
        newSnpData.data_matrix = num.zeros([no_of_rows, no_of_cols], num.int8)
        
        allele2count_ls = []
        NA_notation_report = False	# 2010-3-9 report NA_notation problem only once.
        for j in range(no_of_cols):
            if len(allele2index_ls)<j+1:
                allele2index_ls.append({})
            if len(allele_index2allele_ls)<j+1:
                allele_index2allele_ls.append({})
            allele2count_ls.append({})
            allele_index2allele = allele_index2allele_ls[j]
            for i in range(no_of_rows):
                allele = self.data_matrix[i][j]
                if allele in old_NA_notation_set:
                    allele_index = NA_notation	#numpy.nan is better than -2
                elif allele not in allele2index_ls[j]:
                    allele_index = len(allele2index_ls[j])
                    allele2index_ls[j][allele] = allele_index
                    allele_index2allele[allele_index] = allele
                else:
                    allele_index = allele2index_ls[j][allele]
                
                if allele not in allele2count_ls[j]:
                    allele2count_ls[j][allele] = 1
                else:
                    allele2count_ls[j][allele] += 1
                
                newSnpData.data_matrix[i][j] = allele_index + alleleStartingIndex	# 2010-2-28
                if report and allele_index>1:
                    sys.stderr.write("%s (more than 2) alleles at SNP %s (id=%s).\n"%((allele_index+1), j, self.col_id_ls[j]))
            #2008-12-02	check if binary-allele codes are in major, minor order
            if in_major_minor_order and len(allele2index_ls[j])==2 and row_id_as_major_allele is None:	#only two-allele SNPs
                # allele index 0 would be major allele
                # allele index 1 would be minor allele
                allele1 = allele_index2allele[0]
                allele2 = allele_index2allele[1]
                if allele2count_ls[j][allele1]<allele2count_ls[j][allele2]:	#minor allele got assigned the smaller number, reverse it
                    #reverse the index. won't affect num.nan but will if NA_notation is 0 (or some other numeric value).
                    if NA_notation is not num.nan and not NA_notation_report:	#2013.1.7 replace "!=" with "is not " 
                        sys.stderr.write("\t Warning: switch the notation of major & minor alleles but NA_notation is %s, not num.nan.\n"%NA_notation)
                        NA_notation_report = True
                    newSnpData.data_matrix[:,j] = num.abs(newSnpData.data_matrix[:,j]-1-alleleStartingIndex)+alleleStartingIndex
                    allele2index_ls[j][allele1] = 1
                    allele2index_ls[j][allele2] = 0
                    allele_index2allele[0] = allele2
                    allele_index2allele[1] = allele1
        sys.stderr.write("Done.\n")
        return newSnpData, allele_index2allele_ls
    
    @classmethod
    def loadSNPDataObj(cls,row_id_key_set=None, row_id_hash_func=None, col_id_key_set=None, col_id_hash_func=None, **keywords):
        import pickle as pickle
        import pickle as pickle
        input_fname = keywords['input_fname']
        if input_fname  != "":
            if os.path.isfile(input_fname + ".pickle"):
                input = open(input_fname + '.pickle','r')
                data = pickle.load(input)
                input.close()
            else:
                data = SNPData(**keywords)
                #new_data = transposeSNPData(data)
                #new_data.strain_acc_list = None
                #new_data.category_list = None
                #new_data.tofile(input_fname+".tsv")
                try:
                    output = open(input_fname + '.pickle', 'wb')
                    pickle.dump(data, output, protocol=2)
                except Exception as exp:
                    sys.stderr.write("Error in pickleing file: "+ str(exp))
                finally:
                    if output is not None:
                        output.close() 
        else:
            data = SNPData(row_id_key_set,row_id_hash_func,col_id_key_set,col_id_hash_func,keywords)
        return data
        
class GenomeWideResults(TableClass):
    genome_wide_result_ls = None
    genome_wide_result_obj_id2index = None
    max_value = 0.0	#the current top value for all genome wide results. #must be 0.0, not None.
    #gap = 1.0	#vertical gap (y-axis) between two genome wide results
    
    def __init__(self, **keywords):
        """
        2010-11-22
            added to initialize genome_wide_result_ls and genome_wide_result_obj_id2index properly.
            argument gap is optional.
                If not specified, the gap between a newly-added gwr and the previous gwr is
                    1/3*(prev_gwr.max_value-prev_gwr.min_value).
        """
        TableClass.__init__(self, **keywords)
        self.genome_wide_result_ls = []
        self.genome_wide_result_obj_id2index = {}
        self.max_value = 0.0	#must be 0.0, not None.
    
    def get_genome_wide_result_by_obj_id(self, obj_id):
        return self.genome_wide_result_ls[self.genome_wide_result_obj_id2index[obj_id]]
    
    def add_genome_wide_result(self, genome_wide_result, gap=None):
        """
        2008-10-12
            specify gap between two genome wide results through option gap or self-guessing, 1/3 of previous (gwr.max_value-gwr.min_value)
        """
        genome_wide_result_index = len(self.genome_wide_result_ls)
        if genome_wide_result_index==0:	#the first result, no gap necessary
            genome_wide_result.base_value = self.max_value
        else:
            if gap is None:
                prev_gwr = self.genome_wide_result_ls[genome_wide_result_index-1]
                gap = (prev_gwr.max_value - prev_gwr.min_value)/3.	#self-guessed gap
            genome_wide_result.base_value = self.max_value + gap
        new_max_value = genome_wide_result.base_value + genome_wide_result.max_value - genome_wide_result.min_value
        if self.max_value is None or new_max_value > self.max_value:
            self.max_value = new_max_value
        
        self.genome_wide_result_ls.append(genome_wide_result)
        self.genome_wide_result_obj_id2index[id(genome_wide_result)] = genome_wide_result_index
    
    def clear(self):
        """
        2010-11-22
            clear the 
        """
        self.genome_wide_result_ls = []
        self.genome_wide_result_obj_id2index = {}
        self.max_value = None
    
    
class GenomeWideResult(object):
    """
    2009-4-24
        add data structure chr2min_max_pos to keep track of min,max chromosomal position all SNPs on that chromosome span
    2008-10-30
        no longer inherit from TableClass
    2008-10-21
        add option construct_data_obj_id2index
    """
    data_obj_ls = None
    data_obj_id2index = None
    
    name = ''
    results_method_id = ''
    result_id = ''
    db_entry_id = ''
    results_id = ''
    
    results_method = None
    db_entry = None
    rm = None
    
    min_value = None
    max_value = None
    
    chr_pos2index = None
    construct_data_obj_id2index = None	#True if get_data_obj_by_obj_id() is desired.
    construct_locus_db_id2index = None	#2012.11.20 True if get_data_obj_by_db_id() is desired.
    construct_chr_pos2index = None	#True if get_data_obj_by_chr_pos() is desired.
    argsort_data_obj_ls = None
    chr2no_of_snps = None
    
    def __init__(self, construct_data_obj_id2index=True, construct_chr_pos2index=False, construct_locus_db_id2index=False,\
                name=None, base_value = 0, do_log10_transformation=None):
        """
        2009-4-24
        2008-10-30
            no longer inherit from TableClass
            add this __init__()
        """
        self.construct_data_obj_id2index = construct_data_obj_id2index	#True if get_data_obj_by_obj_id() is desired.
        self.construct_chr_pos2index = construct_chr_pos2index	#True if get_data_obj_by_chr_pos() is desired.
        self.construct_locus_db_id2index = construct_locus_db_id2index	#2012.11.20 
        self.name = name
        self.base_value = base_value
        self.do_log10_transformation = do_log10_transformation
        
        self.chr2min_max_pos = {}
        # 2010-3-9 initialize these two here
        self.data_obj_ls = []	#list and dictionary are crazy references.
        self.data_obj_id2index = {}
        
        #2012.11.20
        self.locus_db_id2index = {}
        
    
    def __len__(self):
        """
        2011-3-21
            return the length of data_obj_ls if it's not None.
        """
        if self.data_obj_ls is not None:
            return len(self.data_obj_ls)
        else:
            return None
    
    def get_data_obj_index_by_locus_db_id(self, locus_db_id=None):
        """
        2012.11.20
        """
        return self.locus_db_id2index.get(locus_db_id)
    
    def get_data_obj_by_locus_db_id(self, locus_db_id=None):
        """
        2012.11.20
        """
        obj_index = self.locus_db_id2index.get(locus_db_id)
        return self.get_data_obj_by_obj_index(obj_index)
    
    def get_data_obj_by_obj_id(self, obj_id=None):
        """
        2012.11.19
            use get()
        """
        obj_index = self.data_obj_id2index.get(obj_id)
        return self.get_data_obj_by_obj_index(obj_index)
    
    def get_data_obj_by_obj_index(self, obj_index=None):
        """
        2012.11.19
            use get()
        """
        if obj_index >=0 and obj_index<len(self.data_obj_ls):
            data_obj = self.data_obj_ls[obj_index]
        else:
            data_obj = None
        return data_obj
    
    def get_data_obj_by_chr_pos(self, chromosome=None, position=None, stopPosition=None):
        """
        2012.3.7
            add argument stopPosition
        2008-09-24
        """
        if stopPosition is None:
            stopPosition = position
        if self.chr_pos2index==None:
            return None
        else:
            obj_index = self.chr_pos2index.get((chromosome, position, stopPosition))
            return self.get_data_obj_by_obj_index(obj_index)
    
    def add_one_data_obj(self, data_obj, chr_pos2index=None):
        """
        2012.11.20 assign value to data_obj.index
            deal with construct_locus_db_id2index
        2012.3.7
            add data_obj.stopPosition into the chr_pos key
        2009-4-24 update self.chr2min_max_pos
        2008-10-23
            handle chr2no_of_snps
        2008-10-21
            add option chr_pos2index to put data_obj into data_obj_ls with pre-defined order
        2008-09-24
            add snippet to deal with construct_chr_pos2index and chr_pos2index
        """
        if isinstance(chr_pos2index, dict):
            data_obj_index = chr_pos2index[(data_obj.chromosome, data_obj.position)]
            if not hasattr(self.data_obj_ls, '__len__') or len(self.data_obj_ls)==0:
                self.data_obj_ls = [None]*len(chr_pos2index)
            self.data_obj_ls[data_obj_index] = data_obj
        else:
            data_obj_index = len(self.data_obj_ls)
            self.data_obj_ls.append(data_obj)
        #2012.11.20 add an index attribute to data_obj
        data_obj.index = data_obj_index
        
        if self.construct_data_obj_id2index:	#2008-10-21
            if self.data_obj_id2index == None:
                self.data_obj_id2index = {}
            self.data_obj_id2index[id(data_obj)] = data_obj_index
        if self.construct_chr_pos2index:	#2008-09-24
            if self.chr_pos2index ==None:
                self.chr_pos2index = {}
            chr_pos = (data_obj.chromosome, data_obj.position, data_obj.stopPosition)	#2012.3.7 add data_obj.stopPosition
            if chr_pos not in self.chr_pos2index:
                self.chr_pos2index[chr_pos] = data_obj_index
            else:
                sys.stderr.write("Warning: chr_pos key %s already in self.chr_pos2index with index=%s.\n"%\
                                (repr(chr_pos), self.chr_pos2index.get(chr_pos)))
        if self.construct_locus_db_id2index:	#2012.11.20
            locus_db_id = data_obj.db_id
            if locus_db_id not in self.locus_db_id2index:
                self.locus_db_id2index[locus_db_id] = data_obj_index
            else:
                sys.stderr.write("Warning: locus_db_id key %s already in self.locus_db_id2index with index=%s.\n"%\
                                (locus_db_id, self.locus_db_id2index.get(locus_db_id)))
        if self.min_value is None or data_obj.value<self.min_value:
            self.min_value = data_obj.value
        if self.max_value is None or data_obj.value>self.max_value:
            self.max_value = data_obj.value
        
        if self.chr2no_of_snps is None:
            self.chr2no_of_snps = {}
        if data_obj.chromosome not in self.chr2no_of_snps:
            self.chr2no_of_snps[data_obj.chromosome] = 0
        self.chr2no_of_snps[data_obj.chromosome] += 1
        
        #2009-4-24 update self.chr2min_max_pos
        if data_obj.chromosome not in self.chr2min_max_pos:
            self.chr2min_max_pos[data_obj.chromosome] = [data_obj.position, data_obj.position]
        else:	# change the minimum and maximum position if condition is met
            if data_obj.position<self.chr2min_max_pos[data_obj.chromosome][0]:
                self.chr2min_max_pos[data_obj.chromosome][0]=data_obj.position
            if data_obj.position>self.chr2min_max_pos[data_obj.chromosome][1]:
                self.chr2min_max_pos[data_obj.chromosome][1]=data_obj.position
    
    def get_data_obj_at_given_rank(self, rank=None):
        """
        2009-2-18
            if rank is beyond reach, return None
        2008-10-02
            rank starts from 1.
        """
        if self.argsort_data_obj_ls is None:
            self.argsort_data_obj_ls = num.argsort(self.data_obj_ls)	#sort in ascending order
        if rank>len(self.data_obj_ls):
            return None
        else:
            return self.data_obj_ls[self.argsort_data_obj_ls[-rank]]	#value bigger, rank smaller
    
    def get_data_obj_index_given_rank(self, rank=None):
        """
        2009-2-18
            if rank is beyond reach, return None
        2008-10-15
            similar to get_data_obj_at_given_rank() but instead of returning data_obj, it returns the index of data_obj in self.data_obj_ls
        """
        if self.argsort_data_obj_ls is None:
            self.argsort_data_obj_ls = num.argsort(self.data_obj_ls)	#sort in ascending order
        if rank>len(self.data_obj_ls):
            return None
        else:
            return self.argsort_data_obj_ls[-rank]	#value bigger, rank smaller
    
    def getTopLoci(self, no_of_top_loci=1000, min_score=None):
        """
        2011-4-23
            add argument min_score. If it's not None, no_of_top_loci would be ignored.
        2011-3-21
            return data_obj directly, rather than (chr, start, stop)
        2011-3-16
            get the top loci out of gwr
        """
        if min_score is not None:
            sys.stderr.write("Get the top loci out of gwr whose value >=%s..."%(min_score))
            no_of_top_loci = len(self.data_obj_ls)	#fake the no_of_top_loci
        else:
            sys.stderr.write("Get the top %s loci out of gwr ..."%(no_of_top_loci))
            
        top_loci = []
        for i in range(no_of_top_loci):
            data_obj = self.get_data_obj_at_given_rank(i+1)
            if min_score is not None and data_obj.value<=min_score:
                break
            top_loci.append(data_obj)
        sys.stderr.write("%s loci. Done.\n"%(len(top_loci)))
        return top_loci
    
    def keepGWRObjectsWithinGivenRBDict(self, rbDict, min_reciprocal_overlap=0.6):
        """
        2010-3-18
            keep only objects (data_obj_ls, data_obj_id2index) that are within rbDict (CNV.xxx)
        """
        sys.stderr.write("Keep GWR objects that are within rbDict  ...")
        from palos.polymorphism.CNV import CNVSegmentBinarySearchTreeKey
        new_data_obj_ls = []
        new_data_obj_id2index = {}
        no_of_objs = len(self.data_obj_ls)
        for i in range(no_of_objs):
            data_obj = self.data_obj_ls[i]
            if data_obj.stop_position is not None:
                span_ls = [data_obj.position, data_obj.stop_position]
            else:
                span_ls = [data_obj.position]
            cnvSegmentKey = CNVSegmentBinarySearchTreeKey(chromosome = data_obj.chromosome, \
                                                        span_ls = span_ls,\
                                                    min_reciprocal_overlap=min_reciprocal_overlap)
            if cnvSegmentKey in rbDict:
                new_data_obj_id2index[id(data_obj)] = len(new_data_obj_ls)
                new_data_obj_ls.append(data_obj)
        self.data_obj_ls = new_data_obj_ls
        self.data_obj_id2index = new_data_obj_id2index
        no_of_new_objs = len(self.data_obj_ls)
        sys.stderr.write("%s out of %s retained.\n"%(no_of_new_objs, no_of_objs))
    
    def drawManhattanPlot(self, db_genome, outputFnamePrefix=None, min_value=2.5, need_svg=False, ylim_type=1,\
                    drawBonferroni=True, highlightBandLs=[]):
        """
        2012.3.9
            copied from variation.src.misc.GWA.drawGWANicer()
            add argument drawBonferroni
            add argument highlightBandLs, a list of [chr,start,stop], to be highlighted in red, with alpha=0.4
        2010-3-9
            if min_value is None, no filter.
            add argument ylim_type:
                1: ylim = ax.get_ylim(); ax.set_ylim([0, ylim[1]])
                2: ax.set_ylim([min_y, max_y])
        2008-1-11 draw nicer genome wide plots
        """
        chr2xy_ls = {}
        counter = 0
        for data_obj in self.data_obj_ls:
            if min_value and data_obj.value<min_value:	#2010-3-9
                continue
            chr = data_obj.chromosome
            if chr not in chr2xy_ls:
                chr2xy_ls[chr] = [[],[]]
            chr2xy_ls[chr][0].append(data_obj.position)
            chr2xy_ls[chr][1].append(data_obj.value)
            counter += 1
        
        chr_gap = 0
        oneGenomeData = db_genome.getOneGenomeData(tax_id=3702, chr_gap=0, chrOrder=1, sequence_type_id=None)
        chr_id_int2size = oneGenomeData.chr_id2size
        chr_id2cumu_start = oneGenomeData.chr_id2cumu_start
        
        sys.stderr.write("Drawing manhattan plot for %s objects ..."%(counter))
        import pylab
        pylab.clf()
        fig = pylab.figure(figsize=(10,2))
        #ax = pylab.axes()
        ax = fig.gca()
        import numpy
        chr_ls = sorted(chr2xy_ls)
        max_y = None
        min_y = None
        for chr in chr_ls:
            xy_ls = chr2xy_ls[chr]
            x_ls = numpy.array(xy_ls[0])
            x_ls += chr_id2cumu_start[chr]
            if xy_ls:
                if max_y is None:
                    max_y = max(xy_ls[1])
                else:
                    max_y = max(max_y, max(xy_ls[1]))
                if min_y is None:
                    min_y = min(xy_ls[1])
                else:
                    min_y = min(min_y, min(xy_ls[1]))
                ax.plot(x_ls, xy_ls[1], '.', markeredgewidth=0, markersize=5, alpha=0.8)
        
        #separate each chromosome
        for chr in chr_ls:
        #	print(chr)
            ax.axvline(chr_id2cumu_start[chr], linestyle='--', color='k', linewidth=0.8)
        
        if drawBonferroni:
            #draw the bonferroni line
            bonferroni_value = -math.log10(0.01/len(self.data_obj_ls))
            ax.axhline(bonferroni_value, linestyle='--', color='k', linewidth=0.8)
        
        for highlightBand in highlightBandLs:
            chr, start, stop = highlightBand[:3]
            cumu_start = start + chr_id2cumu_start[chr]
            cumu_stop = stop + chr_id2cumu_start[chr]
            ax.axvspan(cumu_start, cumu_stop, facecolor="red", alpha=0.4)
        #ax.set_ylabel("-log(P-value)")
        #ax.set_xlabel('Chromosomal Position')
        #ax.set_xlim([0, chr_id2cumu_size[chr_ls[-1]]])
        
        if ylim_type==1:
            ylim = ax.get_ylim()
            ax.set_ylim([0, ylim[1]])
        elif ylim_type==2:
            ax.set_ylim([min_y, max_y])
        
        pylab.savefig('%s.png'%outputFnamePrefix, dpi=300)
        if need_svg:
            pylab.savefig('%s.svg'%outputFnamePrefix, dpi=300)
        sys.stderr.write(".\n")
    
    def fillGenomeWideResultFromHDF5CorrelationFile(self, inputFname, datasetName='correlation', min_value_cutoff=None, \
                            do_log10_transformation=False, pdata=None,\
                            chr_pos2index=None, max_value_cutoff=None, \
                            OR_min_max=False, takeAbsValue=True):
        """
        2012.3.9
            the inputFname is a HDF5 format file. with an array of a compound data type:
                DATATYPE  H5T_COMPOUND {
                    H5T_STD_I32LE "input1LocusID";
                    H5T_STD_I32LE "input2LocusID";
                    H5T_IEEE_F32LE "correlation";
                }
        """
        sys.stderr.write("Filling genome wide result from %s ... "%inputFname)
        
        chr_pos2index = getattr(pdata, 'chr_pos2index', chr_pos2index)	#2008-10-21
        db_id2chr_pos = getattr(pdata, 'db_id2chr_pos', None)	#2011-2-24
        score_for_0_pvalue = getattr(pdata, 'score_for_0_pvalue', 50)	#2012.3.9 only used when score=0 and do_log10_transformation=True
        max_value_cutoff = getattr(pdata, 'max_value_cutoff', max_value_cutoff)	# 2009-10-27
        OR_min_max = getattr(pdata, 'OR_min_max', OR_min_max)	# 2009-10-27
        
        #2011-3-21
        chromosome_request = getattr(pdata, 'chromosome', None)
        start_request = getattr(pdata, 'start', None)
        try:
            start_request = float(start_request)	#passed from web interface functions is of str type
        except:
            pass
        stop_request = getattr(pdata, 'stop', None)
        try:
            stop_request = float(stop_request)	#passed from web interface functions is of str type. int('12384.84') results in failure.
        except:
            pass
        min_MAF_request = getattr(pdata, 'min_MAF', None)
        min_MAC_request = getattr(pdata, 'min_MAC', None)	#2009-1-29
        
        genome_wide_result_id = id(self)
        
        import h5py, numpy
        f1 = h5py.File(inputFname, 'r')
        d1 = f1[datasetName]
        d1_length = d1.shape[0]
        
        no_of_lines = 0
        header = []
        #figure out the compound data type , names
        """
        DATATYPE  H5T_COMPOUND {
         H5T_STD_I32LE "input1LocusID";
         H5T_STD_I32LE "input2LocusID";
         H5T_IEEE_F32LE "correlation";
            }
        """
        for i in range(d1_length):
            locus1_id = d1[i][0]
            score = d1[i][2]	#correlation
            if takeAbsValue:
                score = abs(score)
            db_id = locus1_id
            chr = None
            start_pos = None
            stop_pos = None
            if db_id in db_id2chr_pos:
                chr_pos = db_id2chr_pos.get(db_id)
                if len(chr_pos)>=2:
                    chr, start_pos = chr_pos[:2]
                if len(chr_pos)>=3:
                    stop_pos = chr_pos[2]
            else:	#ignore this row
                continue
            
            if chromosome_request!=None and chr!=chromosome_request:
                continue
            if start_request!=None and start_pos<start_request:
                continue
            if stop_request!=None and start_pos>stop_request:
                continue
            if do_log10_transformation:
                if score<=0:
                    sys.stderr.write("score <=0. can't do log10. row is %s. assign %s to it.\n"%(repr(d1[i]), score_for_0_pvalue))
                    #continue
                    score = score_for_0_pvalue
                else:
                    score = -math.log10(score)
            
            # 2009-10-27 procedure to decide whether to include the data point or not
            include_the_data_point = False	# default is False
            if min_value_cutoff is not None and max_value_cutoff is not None:	# both are specified. check OR_min_max.
                if OR_min_max:	# condition is OR
                    if score>=min_value_cutoff or score<=max_value_cutoff:
                        include_the_data_point = True
                else:	# condition is AND
                    if score>=min_value_cutoff and score<=max_value_cutoff:
                        include_the_data_point = True
            
            elif min_value_cutoff is not None and score>=min_value_cutoff:
                include_the_data_point = True
            elif max_value_cutoff is not None and score<=max_value_cutoff:
                include_the_data_point = True
            elif min_value_cutoff is None and max_value_cutoff is None:	# both are not specified.
                include_the_data_point = True
            
            if include_the_data_point:
                data_obj = DataObject(db_id=db_id, chromosome=chr, position=start_pos, stop_position=stop_pos, value =score)
                
                data_obj.genome_wide_result_id = genome_wide_result_id
                data_obj.genome_wide_result_name = self.name	# 2010-3-15
                self.add_one_data_obj(data_obj, chr_pos2index)
            
        del d1, f1
        sys.stderr.write(" %s data points\n"%(len(self.data_obj_ls)))
    
    def _massageDataObject(self, data_obj=None):
        """
        2013.1.9 extend the dimension of beta_list beta_pvalue_list to 5-element
        """
        data_obj.trimListTypeAttributeToGivenLength(attributeName='beta_list', noOfElementsRequired=5)
        data_obj.trimListTypeAttributeToGivenLength(attributeName='beta_pvalue_list', noOfElementsRequired=5)
        return data_obj
    
    def outputInHDF5MatrixFile(self, writer=None, filename=None, tableName='association', tableObject=None, closeFile = True, attributeDict=None,\
                            outputFileType=1):
        """
        2012.12.21 added argument tableObject, which has precedence over writer, filename, tableName
        2012.12.16 added argument outputFileType
            1: YHPyTables.YHFile
            2: HDF5MatrixFile
        2012.11.22 added attributeDict
        2012.11.19
            output it into an HDF5MatrixFile file
        """
        sys.stderr.write("Dumping association result into %s (HDF5 format) ..."%(filename))
        #each number below is counting bytes, not bits
        if outputFileType==1:
            from palos.polymorphism.Association import AssociationTable, AssociationTableFile
            rowDefinition  = AssociationTable
            OutputFileClass = AssociationTableFile
        else:
            from palos.io.HDF5MatrixFile import HDF5MatrixFile
            rowDefinition = [('locus_id','i8'),('chromosome', HDF5MatrixFile.varLenStrType), ('start','i8'), ('stop', 'i8'), \
                    ('score', 'f8'), ('MAC', 'i8'), ('MAF', 'f8'), ('genotype_var_perc', 'f8')]
            OutputFileClass = HDF5MatrixFile
        if tableObject is None:
            if writer is None and filename:
                writer = OutputFileClass(filename, mode='w', rowDefinition=rowDefinition, tableName=tableName)
                tableObject = writer.getTableObject(tableName=tableName)
            elif writer:
                tableObject = writer.createNewTable(tableName=tableName, rowDefinition=rowDefinition)
            else:
                sys.stderr.write("Error: no writer(%s) or filename(%s) to dump.\n"%(writer, filename))
                sys.exit(3)
        if attributeDict:
            from palos.io.HDF5MatrixFile import addAttributeDictToYHTableInHDF5Group
            addAttributeDictToYHTableInHDF5Group(tableObject=tableObject, attributeDict=attributeDict)
        if self.results_method_id:
            tableObject.addAttribute(name='result_id', value=self.results_method_id)
        if getattr(self, 'do_log10_transformation', None) is not None:	#2013.1.11
            tableObject.addAttribute(name='do_log10_transformation', value=self.do_log10_transformation)
        if self.name:
            tableObject.addAttribute(name='name', value=self.name)
        cellList = []
        for data_obj in self.data_obj_ls:
            data_obj = self._massageDataObject(data_obj=data_obj)
            cellList.append(data_obj)
        
        if tableObject is None:
            sys.stderr.write("Error: tableObject (name=%s) is None. could not write.\n"%(tableName))
            sys.exit(3)
        tableObject.writeCellList(cellList, cellType=2)
        if closeFile and writer is not None:
            writer.close()
        sys.stderr.write("%s objects.\n"%(len(cellList)))
        return writer
    
    
    def reIndexDataObjecs(self):
        """
        2012.11.20 need to run this after data_obj_ls is sorted and you plan to use any index
        """
        self.data_obj_id2index = {}
        self.chr_pos2index = {}
        self.locus_db_id2index = {}
        for i in range(len(self.data_obj_ls)):
            data_obj = self.data_obj_ls[i]
            data_obj_index = i
            data_obj.index = i
            if self.construct_data_obj_id2index:	#2008-10-21
                self.data_obj_id2index[id(data_obj)] = data_obj_index
            if self.construct_chr_pos2index:	#2008-09-24
                chr_pos = (data_obj.chromosome, data_obj.position, data_obj.stopPosition)	#2012.3.7 add data_obj.stopPosition
                if chr_pos not in self.chr_pos2index:
                    self.chr_pos2index[chr_pos] = data_obj_index
                else:
                    sys.stderr.write("Warning: chr_pos key %s already in self.chr_pos2index with index=%s.\n"%\
                                    (repr(chr_pos), self.chr_pos2index.get(chr_pos)))
            if self.construct_locus_db_id2index:
                locus_db_id = data_obj.db_id
                if locus_db_id not in self.locus_db_id2index:
                    self.locus_db_id2index[locus_db_id] = data_obj_index
                else:
                    sys.stderr.write("Warning: locus_db_id key %s already in self.locus_db_id2index with index=%s.\n"%\
                                    (locus_db_id, self.locus_db_id2index.get(locus_db_id)))
    
    def setResultID(self, result_id=None):
        """
        2012.11.20
            some are  for backwards compatibility
        """
        self.results_method_id = result_id
        self.result_id = result_id
        self.db_entry_id = result_id
        self.results_id = result_id
    
    def setResultMethod(self, rm=None):
        """
        2012.11.20
        """
        self.results_method = rm
        self.rm = rm
        self.db_entry = rm
        self.setResultID(rm.id)
    
class DataObject(object):
    """
    2009-1-7
        
    2008-11-20
        add mac
    2008-11-12
        add genotype_var_perc, comment
    """
    def __init__(self, **keywords):
        """
        2011-3-10
            add db_id to identify the locus by db id
        2010-4-15
            add target_seq_id, target_start, target_stop
        """
        #both db_id and locus_id is same
        self.db_id = None
        self.locus_id = None
        
        self.chromosome = None
        
        self.position = None	#both are same
        self.start = None
        
        self.stop_position = None	#both are same
        self.stop = None
        
        self.target_seq_id = None
        self.target_start = None
        self.target_stop = None
        self.name = None
        
        self.value = None
        self.score = None
        self.genome_wide_result_id = None
        self.genome_wide_result_name = None
        self.maf = None
        self.mac = None
        self.genotype_var_perc = None
        self.extra_col_ls = []
        self.beta_list = []	#2013.1.9
        self.beta_pvalue_list = []	#2013.1.9
        
        self.comment = None
        for key, value in keywords.items():
            setattr(self, key, value)
        
        #2012.11.18 convenient purpose
        self._makeTwoAttributesSameValue('db_id', 'locus_id')
        self._makeTwoAttributesSameValue('position', 'start')
        self._makeTwoAttributesSameValue('stop_position', 'stop')
        self._makeTwoAttributesSameValue('value', 'score')
        
        self.index = None
    
    def _makeTwoAttributesSameValue(self, attribute1Name=None, attribute2Name=None):
        """
        2013.1.9
        """
        attribute1Value = getattr(self, attribute1Name, None)
        attribute2Value = getattr(self, attribute2Name, None)
        if attribute1Value is not None and attribute2Value is None:
            setattr(self, attribute2Name, attribute1Value)
        elif attribute1Value is None and attribute2Value is not None:
            setattr(self, attribute1Name, attribute2Value)
    
    def __cmp__(self, other):
        """
        2008-08-20
            define how to compare DataObject
        """
        return cmp(self.value, other.value)
    
    def __str__(self):
        """
        2010-3-14
            Called by the str built-in function and by the print statement to compute
                the informal string representation of an object. This differs from __repr__
                in that it does not have to be a valid Python expression: a more convenient or
                concise representation may be used instead. The return value must be a string object.
        """
        output_str = "genome result: %s, chromosome: %s, position: %s, "%\
            (self.genome_wide_result_name, self.chromosome, self.position)
        if self.stop_position is not None:
            output_str += "stop position: %s, "%(self.stop_position)
        output_str += '\n'
        output_str += "\tscore: %s\n"%(self.value)
        if self.maf:
            output_str += "\tmaf: %s\n"%(self.maf)
        if self.genotype_var_perc:
            output_str += "\tgenotype_var_perc: %s\n"%(self.genotype_var_perc)
        if self.comment:
            output_str += "\tcomment: %s\n"%(self.comment)
        return output_str
    
    def trimListTypeAttributeToGivenLength(self, attributeName=None, noOfElementsRequired=None, defaultValue=-1):
        """
        2013.1.9
        """
        attributeValue = getattr(self, attributeName, None)
        if isinstance(attributeValue, list):
            noOfElements = len(attributeValue)
            if noOfElements<noOfElementsRequired:
                setattr(self, attributeName, attributeValue + [defaultValue]*(noOfElementsRequired-noOfElements))
            elif noOfElements>noOfElementsRequired:
                setattr(self, attributeName, attributeValue[:noOfElementsRequired])
    
    @property
    def stopPosition(self):
        """
        2011-4-20
            a wrapper to deal with the case stop_position could be None (it's a single-position locus).
        """
        if self.stop_position is None:
            return self.position
        else:
            return self.stop_position

def cmpDataObjByChrPos(x, y):
    """
    2011-3-21
        used to sort a list of DataObject via its (chromosome, position).
        i.e. data_obj_ls.sort(cmp=cmpDataObjByChrPos)
    """
    return cmp((x.chromosome, x.position), (y.chromosome, y.position))


def getGenomeWideResultFromFile(inputFname=None, min_value_cutoff=None, do_log10_transformation=False, pdata=None,\
                            construct_chr_pos2index=False, construct_data_obj_id2index=True,\
                            is_4th_col_stop_pos=False, chr_pos2index=None, max_value_cutoff=None, \
                            OR_min_max=False, report=True):
    """
    2012.11.15 argument report controls whether getResultMethodContent() will report progress.
    2011-4-19 no more integer conversion for chromosome & chromosome_request
    2011-3-21
        process chromosome, start, stop of pdata in the beginning
    2011-3-10
        db_id2chr_pos's value could be in the format of (chr,pos) OR (chr,start,stop).
    2011-2-24
        deal with inputFname with db id for locus id , rather than chr, pos
            if 2nd_column (pos) is nothing or "0", it's regarded as db_id.
        use pdata.id2chr_pos to translate db id into chr, pos
    2010-10-13
        new structure, pdata.chr_pos_map to map chr,pos to new chr, pos (like TAIR8 to TAIR9 mapping)
    2010-3-15
        add this
            data_obj.genome_wide_result_name = gwr.name
    2009-10-27
        add code to deal with pdata.max_value_cutoff and pdata.OR_min_max
    2009-6-17
        convert 2nd column (start_pos) to float, then to integer
    2009-6-10
        set additional columns (rest_of_row) as attributes of data_obj with column name as the attribute name
    2009-2-18
        handle filtering by min_MAC (column_5th)
        column 6 and 7 are allowed to be empty placeholder. (previously it causes type cast error if it's empty)
    2008-12-18
        if pdata has attribute 'gwr_name', assign it to GenomeWideResult.name.
        otherwise GenomeWideResult.name = os.path.basename(inputFname)
    2008-11-20
        fix a bug that column_5th was skipped and column_6 was tried when there are only 5 columns
    2008-11-12
        parse lines with column_5th, column_6 and more
    2008-10-28
        handle construct_data_obj_id2index
    2008-10-21
        add score_for_0_pvalue, if pdata doesn't have it, assume 50.
        get chr_pos2index from pdata, which will pre-decide the order of snps in gwr.data_obj_ls
    2008-10-14
        get "is_4th_col_stop_pos" from pdata if it exists to decide how to deal with 4th col
    2008-09-24
        add construct_chr_pos2index
    2008-08-15
        skips non-positive values if need to do_log10_transformation
    2008-08-14
        add min_MAF into pdata
    2008-08-03
        add pdata (chromosome, start, stop) to restrain data
    2008-07-17
        moved from GenomeBrowser.py
    2008-05-31
        automatically detect if header exists on the first line.
    2008-05-28
        handle both 3/4-column input file
    """
    
    #A dictionary to understand new headers:
    header_dict = {}
    
    construct_chr_pos2index = getattr(pdata, 'construct_chr_pos2index', construct_chr_pos2index)	#2008-09-24
    construct_data_obj_id2index = getattr(pdata, 'construct_data_obj_id2index', construct_data_obj_id2index)	#2008-10-28 for get_data_obj_by_obj_index()
    is_4th_col_stop_pos = getattr(pdata, 'is_4th_col_stop_pos', is_4th_col_stop_pos)	#2008-10-14
    chr_pos2index = getattr(pdata, 'chr_pos2index', chr_pos2index)	#2008-10-21
    db_id2chr_pos = getattr(pdata, 'db_id2chr_pos', None)	#2011-2-24
    score_for_0_pvalue = getattr(pdata, 'score_for_0_pvalue', 50)
    gwr_name = getattr(pdata, 'gwr_name', os.path.basename(inputFname))
    max_value_cutoff = getattr(pdata, 'max_value_cutoff', max_value_cutoff)	# 2009-10-27
    OR_min_max = getattr(pdata, 'OR_min_max', OR_min_max)	# 2009-10-27
    chr_pos_map = getattr(pdata, 'chr_pos_map', None)	#2010-10-13
    report = getattr(pdata, 'report', report)	#2012.11.15
    
    #2011-3-21
    chromosome_request = getattr(pdata, 'chromosome', None)
    start_request = getattr(pdata, 'start', None)
    try:
        start_request = float(start_request)	#passed from web interface functions is of str type
    except:
        pass
    stop_request = getattr(pdata, 'stop', None)
    try:
        stop_request = float(stop_request)	#passed from web interface functions is of str type. int('12384.84') results in failure.
    except:
        pass
    min_MAF_request = getattr(pdata, 'min_MAF', None)
    min_MAC_request = getattr(pdata, 'min_MAC', None)	#2009-1-29
    
    if report:
        sys.stderr.write("Getting genome wide result from %s ... "%inputFname)
    
    gwr = GenomeWideResult(name=gwr_name, construct_chr_pos2index=construct_chr_pos2index, \
                        construct_data_obj_id2index=construct_data_obj_id2index)
    gwr.data_obj_ls = []	#list and dictionary are crazy references.
    gwr.data_obj_id2index = {}
    gwr.do_log10_transformation = do_log10_transformation	#2013.1.11
    genome_wide_result_id = id(gwr)
    delimiter = figureOutDelimiter(inputFname)
    reader = csv.reader(open(inputFname), delimiter=delimiter)
    no_of_lines = 0
    col_name2index = {}
    header = []
    for row in reader:
        #check if 1st line is header or not
        if no_of_lines ==0 and pa_has_characters.search(row[1]):
            header = row
            col_name2index = getColName2IndexFromHeader(header) #Returns a dictionary
            continue
        
        #2011-3-10 initialize all variables
        db_id = None
        column_4th = None	#it's MAF probably
        column_5th = None	#it's MAC probably
        column_6 = None	#it's genotype_var_perc probably
        rest_of_row = []
        stop_pos = None
        if row[1] and row[1]!='0':	#2011-2-24 non-zero on 2nd column, it's position
            chr = row[0]	#2011-4-19 no more integer conversion for chromosome.
            start_pos = int(float(row[1]))
        elif db_id2chr_pos:	#2011-2-24
            db_id = int(row[0])
            if db_id in db_id2chr_pos:
                chr_pos = db_id2chr_pos.get(db_id)
                if len(chr_pos)>=2:
                    chr, start_pos = chr_pos[:2]
                if len(chr_pos)>=3:
                    stop_pos = chr_pos[2]
            else:	#ignore this row
                continue
        else:
            sys.stderr.write("db_id2chr_pos is none. but this row %s seems to be using db_id as locus id."%(repr(row)))
            continue
        
        if len(row)>=3:
            score = float(row[2])
        
        if len(row)>=4:
            if is_4th_col_stop_pos:
                stop_pos = int(row[3])
            else:
                column_4th=float(row[3])
        if len(row)>=5:
            column_5th = float(row[4])
        if len(row)>=6 and row[5]:
            column_6 = float(row[5])
        if len(row)>=7 and row[6]:
            rest_of_row = row[6:]
        """
        else:
            sys.stderr.write("only 3 or 4 columns are allowed in input file.\n")
            return gwr
        """
        if chromosome_request!=None and chr!=chromosome_request:
            continue
        if start_request!=None and start_pos<start_request:
            continue
        if stop_request!=None and start_pos>stop_request:
            continue
        if min_MAF_request!=None and column_4th!=None and column_4th<min_MAF_request:	#MAF too small
            continue
        if min_MAC_request!=None and column_5th!=None and column_5th<min_MAC_request:	#2009-1-29 MAC too small
            continue
        if do_log10_transformation:
            if score<=0:
                sys.stderr.write("score <=0. can't do log10. row is %s. assign %s to it.\n"%(repr(row), score_for_0_pvalue))
                #continue
                score = score_for_0_pvalue
            else:
                score = -math.log10(score)
        
        # 2009-10-27 procedure to decide whether to include the data point or not
        include_the_data_point = False	# default is False
        if min_value_cutoff is not None and max_value_cutoff is not None:	# both are specified. check OR_min_max.
            if OR_min_max:	# condition is OR
                if score>=min_value_cutoff or score<=max_value_cutoff:
                    include_the_data_point = True
            else:	# condition is AND
                if score>=min_value_cutoff and score<=max_value_cutoff:
                    include_the_data_point = True
            
        elif min_value_cutoff is not None and score>=min_value_cutoff:
            include_the_data_point = True
        elif max_value_cutoff is not None and score<=max_value_cutoff:
            include_the_data_point = True
        elif min_value_cutoff is None and max_value_cutoff is None:	# both are not specified.
            include_the_data_point = True
        if include_the_data_point and chr_pos_map:	#2010-10-13
            if stop_pos is not None:
                key = (chr, start_pos, stop_pos)
            else:
                key = (chr, start_pos,)
            new_chr_start_stop = chr_pos_map.get(key)
            if new_chr_start_stop is None:
                include_the_data_point = False	# skip this point
            else:
                chr, start_pos = new_chr_start_stop[:2]
                if len(new_chr_start_stop)>2:
                    stop_pos = new_chr_start_stop[2]
        if include_the_data_point:
            data_obj = DataObject(db_id=db_id, chromosome=chr, position=start_pos, stop_position=stop_pos, value =score)
            if column_4th is not None:
                data_obj.maf = column_4th
            if column_5th is not None:
                data_obj.mac = column_5th
                
            if column_6 is not None: 
                #If file has a header, then use that, otherwise guess it's genotype_var_perc
                if header and len(header)>5:
                    setattr(data_obj, header[5],column_6)
                else:
                    data_obj.genotype_var_perc = column_6
            if rest_of_row:
                for beta_pvalue in rest_of_row:
                    beta_pvalue = beta_pvalue.split(':')
                    if len(beta_pvalue)>0:
                        beta = beta_pvalue[0]
                        data_obj.beta_list.append(float(beta))
                    if len(beta_pvalue)>1:
                        pvalue = beta_pvalue[1]
                        data_obj.beta_pvalue_list.append(float(pvalue))
                
                data_obj.extra_col_ls = rest_of_row
                data_obj.comment = ','.join(rest_of_row)
                """
                if header:	#setting the betas
                    for i in range(len(rest_of_row)):
                        col_name = header[i+6]
                        setattr(data_obj, col_name, rest_of_row[i])
                """
            data_obj.genome_wide_result_id = genome_wide_result_id
            data_obj.genome_wide_result_name = gwr.name	# 2010-3-15
            gwr.add_one_data_obj(data_obj, chr_pos2index)
        
        no_of_lines += 1
        
    del reader
    if report:
        sys.stderr.write(" %s loci.\n"%(len(gwr.data_obj_ls)))
    return gwr

def cmpStringSNPID(x, y):
    """
    Examples:
        col_id_ls.sort(cmp=cmpStringSNPID)
    2010-4-4
        a cmp function to sort a list of string-format SNP IDs.
        x and y are in the form of chr_pos or chr_pos_offset like '3_4343_0'
    """
    x = x.split('_')
    x = map(int, x)
    y = y.split('_')
    y = map(int, y)
    return cmp(x,y)

class SNPInfo(object):
    """
    2012.3.8
        add locusRBDict
    2009-2-18
        a class to hold chromosome, position, allele, snps_id (db)
        DrawSNPRegion.getSNPInfo(db) does the job of filling it up
    """
    chr_pos_ls = None
    chr_pos2index = None
    snps_id2index = None
    data_ls = None	#a list of [snps_d, chromosome, position, allele1, allele2]
    #2012.3.8 key is CNVSegmentBinarySearchTreeKey(chromosome=row.chromosome, span_ls=[position, end_position], min_reciprocal_overlap=1,)
    # value is a list of queried db objects.
    locusRBDict = None	#
    
    def __init__(self, **keywords):
        """
        2009-2-18 allow any type of keywords
        """
        for argument_key, argument_value in keywords.items():
            setattr(self, argument_key, argument_value)
    
    def getSnpsIDGivenChrPos(self, chromosome, position):
        snp_info_index = self.chr_pos2index.get((chromosome, position))
        if snp_info_index is not None:
            snps_id = self.data_ls[snp_info_index][0]
        else:
            snps_id = None
        return snps_id
    
    def getSnpsAllelesGivenChrPos(self, chromosome, position):
        snp_info_index = self.chr_pos2index.get((chromosome, position))
        if snp_info_index is not None:
            alleles = self.data_ls[snp_info_index][3:5]
        else:
            alleles = None
        return alleles


def getGenomeWideResultFromHDF5MatrixFile(inputFname=None, reader=None, \
        tableName='association', tableObject=None, min_value_cutoff=None, \
        do_log10_transformation=False, pdata=None,\
        construct_chr_pos2index=False, construct_data_obj_id2index=False, construct_locus_db_id2index=False,\
        chr_pos2index=None, max_value_cutoff=None, \
        OR_min_max=False, report=True, inputFileType=1, **keywords):
    """
    2013.1.15 maf or mac =-1 means NA.
    2012.12.16 added argument inputFileType
            1: AssociationTableFile
            2: HDF5MatrixFile
    2012.11.19 similar to getGenomeWideResultFromFile, but instead the input is a HDF5MatrixFile format.
    """
    
    #A dictionary to understand new headers:
    header_dict = {}
    
    construct_chr_pos2index = getattr(pdata, 'construct_chr_pos2index', construct_chr_pos2index)	#2008-09-24
    construct_data_obj_id2index = getattr(pdata, 'construct_data_obj_id2index', construct_data_obj_id2index)	#2008-10-28 for get_data_obj_by_obj_index()
    chr_pos2index = getattr(pdata, 'chr_pos2index', chr_pos2index)	#2008-10-21
    db_id2chr_pos = getattr(pdata, 'db_id2chr_pos', None)	#2011-2-24
    score_for_0_pvalue = getattr(pdata, 'score_for_0_pvalue', 50)
    if inputFname:
        gwr_name = getattr(pdata, 'gwr_name', os.path.basename(inputFname))
    else:
        gwr_name = getattr(pdata, 'gwr_name', reader.getAttribute('name'))
    max_value_cutoff = getattr(pdata, 'max_value_cutoff', max_value_cutoff)	# 2009-10-27
    OR_min_max = getattr(pdata, 'OR_min_max', OR_min_max)	# 2009-10-27
    chr_pos_map = getattr(pdata, 'chr_pos_map', None)	#2010-10-13
    report = getattr(pdata, 'report', report)	#2012.11.15
    
    #2011-3-21
    chromosome_request = getattr(pdata, 'chromosome', None)
    start_request = getattr(pdata, 'start', None)
    try:
        start_request = float(start_request)	#passed from web interface functions is of str type
    except:
        pass
    stop_request = getattr(pdata, 'stop', None)
    try:
        stop_request = float(stop_request)	#passed from web interface functions is of str type. int('12384.84') results in failure.
    except:
        pass
    min_MAF_request = getattr(pdata, 'min_MAF', None)
    min_MAC_request = getattr(pdata, 'min_MAC', None)	#2009-1-29
    
    if report:
        sys.stderr.write("Getting genome wide result from file=%s, table=%s ... "%(inputFname, tableName))
    
    gwr = GenomeWideResult(name=gwr_name, construct_chr_pos2index=construct_chr_pos2index, \
                        construct_data_obj_id2index=construct_data_obj_id2index, \
                        construct_locus_db_id2index=construct_locus_db_id2index)
    gwr.data_obj_ls = []	#list and dictionary are crazy references.
    gwr.data_obj_id2index = {}
    genome_wide_result_id = id(gwr)
    
    if tableObject:
        associationTableObject = tableObject
    else:
        if reader is None:
            if inputFileType==1:
                from palos.polymorphism.Association import AssociationTableFile
                reader = AssociationTableFile(inputFname, mode='r', autoRead=False)
            else:
                from palos.io.HDF5MatrixFile import HDF5MatrixFile
                reader = HDF5MatrixFile(inputFname, mode='r')
        associationTableObject = reader.getTableObject(tableName=tableName)
    
    for attributeName, value in associationTableObject.getAttributes().items():
        setattr(gwr, attributeName, value)
    gwr.setResultID(associationTableObject.getAttribute('result_id'))
    gwr.do_log10_transformation = do_log10_transformation	#2013.1.11
    no_of_lines = 0
    for row in associationTableObject:
        #2011-3-10 initialize all variables
        column_6 = None	#it's genotype_var_perc probably
        rest_of_row = []
        #no type cast, all straight from HDF5
        
        db_id = row['locus_id']
        chromosome = row['chromosome']	#2011-4-19 no more integer conversion for chromosome.
        start_pos = row['start']
        stop_pos = row['stop']
        
        if db_id2chr_pos:	#2012.11.19 correct chromosome, start_pos, stop_pos based on this dictionary
            if db_id in db_id2chr_pos:
                chr_pos = db_id2chr_pos.get(db_id)
                if len(chr_pos)>=2:
                    chromosome, start_pos = chr_pos[:2]
                if len(chr_pos)>=3:
                    stop_pos = chr_pos[2]
        
        score = row['score']
        mac = row['mac']
        maf = row['maf']
        genotype_var_perc = row['genotype_var_perc']
        if chromosome=='' or chromosome is None:	#2013.1.13 invalid loci
            continue
        if chromosome_request!=None and chromosome!=chromosome_request:
            continue
        if start_pos<=0 or start_pos is None:	#2013.1.13 invalid loci
            continue
        if start_request!=None and start_pos<start_request:
            continue
        if stop_request!=None and start_pos>stop_request:
            continue
        if min_MAF_request!=None and maf!=None and maf!=-1 and maf<min_MAF_request:	#maf too small	-1 is NA.
            continue
        if min_MAC_request!=None and mac!=None and mac!=-1 and mac<min_MAC_request:	#2009-1-29 mac too small. -1 is NA
            continue
        if do_log10_transformation:
            if score<=0:
                sys.stderr.write("score <=0. can't do log10. row is %s. assign %s to it.\n"%(repr(row), score_for_0_pvalue))
                #continue
                score = score_for_0_pvalue
            else:
                score = -math.log10(score)
        
        # 2009-10-27 procedure to decide whether to include the data point or not
        include_the_data_point = False	# default is False
        if min_value_cutoff is not None and max_value_cutoff is not None:	# both are specified. check OR_min_max.
            if OR_min_max:	# condition is OR
                if score>=min_value_cutoff or score<=max_value_cutoff:
                    include_the_data_point = True
            else:	# condition is AND
                if score>=min_value_cutoff and score<=max_value_cutoff:
                    include_the_data_point = True
            
        elif min_value_cutoff is not None and score>=min_value_cutoff:
            include_the_data_point = True
        elif max_value_cutoff is not None and score<=max_value_cutoff:
            include_the_data_point = True
        elif min_value_cutoff is None and max_value_cutoff is None:	# both are not specified.
            include_the_data_point = True
        if include_the_data_point and chr_pos_map:	#2010-10-13
            if stop_pos is not None:
                key = (chromosome, start_pos, stop_pos)
            else:
                key = (chromosome, start_pos,)
            new_chr_start_stop = chr_pos_map.get(key)
            if new_chr_start_stop is None:
                include_the_data_point = False	# skip this point
            else:
                chromosome, start_pos = new_chr_start_stop[:2]
                if len(new_chr_start_stop)>2:
                    stop_pos = new_chr_start_stop[2]
        if include_the_data_point:
            data_obj = DataObject(db_id=db_id, chromosome=chromosome, position=start_pos, stop_position=stop_pos, value =score,
                                maf=maf, mac=mac, genotype_var_perc=genotype_var_perc)
            data_obj.genome_wide_result_id = genome_wide_result_id
            data_obj.genome_wide_result_name = gwr.name
            gwr.add_one_data_obj(data_obj, chr_pos2index)
        
        no_of_lines += 1
    
    if inputFname and reader is not None:
        reader.close()
    if report:
        sys.stderr.write(" %s loci.\n"%(len(gwr.data_obj_ls)))
    return gwr
