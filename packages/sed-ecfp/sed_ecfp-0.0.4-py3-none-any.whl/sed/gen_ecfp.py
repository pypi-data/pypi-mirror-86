import os
import sys
import rdkit.Chem as Chem
from rdkit.Chem import AllChem
import numpy as np
import xlrd
import scipy.io as scio

def gen_ecfps(gpcr_name,gpcr_length,gpcr_radius):
    # local_path = os.path.dirname(os.getcwd())
    local_path = os.getcwd()
    gpcr_path = local_path+'/data/' + gpcr_name
    print("GPCR_Path:",gpcr_path)

    gpcr_diameter = int(gpcr_radius) * 2
    excel = xlrd.open_workbook(gpcr_path + '/Input_Smiles.xlsx')
    # 获取第一个sheet
    sheet = excel.sheets()[0]

    # 打印第j列数据
    x1 = sheet.col_values(0)

    a1 = smiles_to_fps(x1, int(gpcr_length), int(gpcr_radius))

    #print(a1)
    saved_file = gpcr_name + '_ECFP' + str(gpcr_diameter) + '_' + str(gpcr_length)
    np.save(saved_file, a1)
    print("生成的ECFP：", saved_file)
    #mat_file = saved_file + '.mat'
    #print(mat_file)
    #print(type(a1))
    #scio.savemat(mat_file, {"X":a1})
    #return a1
    return saved_file

def smiles_to_fps(data, fp_length, fp_radius):
    return stringlist2intarray(np.array([smile_to_fp(s, fp_length, fp_radius) for s in data]))


def smile_to_fp(s, fp_length, fp_radius):
    m = Chem.MolFromSmiles(s)
    return (AllChem.GetMorganFingerprintAsBitVect(
        m, fp_radius, nBits=fp_length, invariants=[1] * m.GetNumAtoms(), useFeatures=False)).ToBitString()


def stringlist2intarray(A):
    '''This function will convert from a list of strings "10010101" into in integer numpy array.'''
    return np.array([list(s) for s in A], dtype=int)


if __name__ == "__main__":
    gen_ecfps('P08908', 1024, 6)

