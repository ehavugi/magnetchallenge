import os
import numpy as np
import pandas as pd
path="."

from scipy.stats import gmean
import matplotlib.pyplot as plt
material="Volumetric_Loss_Material D.csv"
materials=["Volumetric_Loss_Material A.csv",
        "Volumetric_Loss_Material B.csv",
        "Volumetric_Loss_Material C.csv",
        "Volumetric_Loss_Material D.csv",
        "Volumetric_Loss_Material E.csv"]
for material in materials:
    data={}
    for school in os.listdir(path):  # list of subdirectories and files
        pathTrue=os.path.isdir(school)
        # print(school,os.path.isdir(school))
        if pathTrue:
            # print(school)
            matpath= f"{path}/{school}/Result/{material}"
            if os.path.isfile(matpath):
                datai=  pd.read_csv(f"{path}/{school}/Result/{material}",header=None)
                
                # print("Datai", datai.describe())
                data[school]=np.abs(datai.values.reshape(-1))
                # print("data", data.describe())
    data=pd.DataFrame.from_dict(data)
    print(data.columns)
    # data=data[[ 'Paderborn', 'Sydney','Tsinghua', 'TUDelft', 'XJTU']]
    # data=data[[ 'ASU', 'Tribhuvan']]

    # data['av'] = data.geomean(axis=1)
    # print(data.describe())
    dataMean = data.mean(axis=1)
    datastd = data.std(axis=1)

    data["gmean"] = data.apply(gmean, axis=1)
    data['std']=datastd/dataMean
    # data['gmean'] =dataMean

    data.to_csv("ave.csv")

    correct="../finaltest/EvaluationKit/EvaluationKit/Measured_"+material
    # print(correct)
    datac = pd.read_csv(correct,header=None)
    # data[]
    # print(datac.values.shape,data['ASU'].values.shape)

    print("school, median error, 95 th percentile,99 percentile,99.9 percentile")

    for each in ['ASU', 'KU Leuven', 'Mondragon', 'NTUT', 'Paderborn', 'PoliTO', 'Sydney', 'Tribhuvan', 'Tsinghua', 'TUDelft', 'UTK', 'XJTU']:
        if each in data.columns:
            data['error']=np.abs(data[each].values.reshape(-1)-datac.values.reshape(-1))/datac.values.reshape(-1)
            print(each, np.percentile(data['error'],50),np.percentile(data['error'],95),np.percentile(data['error'],99),np.percentile(data['error'],99.9))

    data['error']=np.abs(data["gmean"].values.reshape(-1)-datac.values.reshape(-1))/datac.values.reshape(-1)
    print("gmean", np.percentile(data['error'],50),np.percentile(data['error'],95),np.percentile(data['error'],99),np.percentile(data['error'],99.9))


    plt.plot(data['std'],data['error'],"*")
    plt.ylabel("Error(%)")
    plt.xlabel("standard deviation")
    print(np.corrcoef(data['std'],data['error']))
    n = len(data)
    datacopy=data.copy(True)
    dataccopy=datac.copy(True)
    percentileErrors = []
    percentileRejectionRatio = []
    for RejectionRatio in range(1,99):
        reject=np.percentile(datacopy['std'].values,RejectionRatio)
        datac= dataccopy[datacopy['std'].values>reject]

        data=datacopy[datacopy['std'].values>reject]
        # print("Bayesian Error(given a condition detectable)")
        data['error']=np.abs(data["gmean"].values.reshape(-1)-datac.values.reshape(-1))/datac.values.reshape(-1)
        # print("gmean after filtering: ", np.percentile(data['error'],50),np.percentile(data['error'],95),np.percentile(data['error'],99),np.percentile(data['error'],99.9))
        # for each in ['ASU', 'KU Leuven', 'Mondragon', 'NTUT', 'Paderborn', 'PoliTO', 'Sydney', 'Tribhuvan', 'Tsinghua', 'TUDelft', 'UTK', 'XJTU']:
        #     if each in data.columns:
        #         data['error']=np.abs(data[each].values.reshape(-1)-datac.values.reshape(-1))/datac.values.reshape(-1)
        #         # print(each,np.percentile(data['error'],50), np.percentile(data['error'],95),np.percentile(data['error'],99),np.percentile(data['error'],99.9))
        percentileErrors.append(np.percentile(data['error'],95))
        percentileRejectionRatio.append(RejectionRatio)
        # print(len(data)/n*100, "%","remaining")
    # print(data.index)

    plt.figure()
    plt.plot(percentileRejectionRatio,percentileErrors)
    # plt.plot(percentileRejectionRatio, percentileErrors)

    plt.ylabel("Error")
    plt.xlabel("Percentile rejected by std metric")
    plt.savefig(material+".png")
    # plt.show()

