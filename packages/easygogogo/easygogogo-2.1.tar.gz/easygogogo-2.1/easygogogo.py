import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from scipy.stats import kstest
import scipy.stats as stats
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm
from scipy.stats import pearsonr
from scipy.stats import chi2_contingency
from scipy.stats import shapiro
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa import stattools
from scipy.stats import f_oneway
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
import math
import statsmodels.api as sma

from sklearn.linear_model import LogisticRegression
from scipy.optimize import curve_fit
import sklearn

from sklearn.cluster import AgglomerativeClustering
import random


from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

import math
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import silhouette_score
def last(a,e):
    RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    def get_w(array):
        row = array.shape[0]  # 计算出阶数
        a_axis_0_sum = array.sum(axis=0)
        # print(a_axis_0_sum)
        b = array / a_axis_0_sum  # 新的矩阵b
        # print(b)
        b_axis_0_sum = b.sum(axis=0)
        b_axis_1_sum = b.sum(axis=1)  # 每一行的特征向量
        # print(b_axis_1_sum)
        w = b_axis_1_sum / row  # 归一化处理(特征向量)
        nw = w * row
        AW = (w * array).sum(axis=1)
        # print(AW)
        max_max = sum(AW / (row * w))
        # print(max_max)
        CI = (max_max - row) / (row - 1)
        CR = CI / RI_dict[row]
        print("一致性检验指标为",CR)
        if CR < 0.1:

            print(round(CR, 3))
            print('满足一致性')
            print("寻找最大的特征根")
            print(np.max(w))
            print(sorted(w,reverse=True))
            print(max_max)
            print("计算出特征向量")
            print('特征向量:%s' % w)
            return w
        else:
            print("警告！！！")
            print(array)
            print(round(CR, 3))
            print('不满足一致性，请进行修改')

    def main(array):
        if type(array) is np.ndarray:
            return get_w(array)
        else:
            print('请输入numpy对象')

    e = main(e)
    res = []
    print(a)
    for i in list(a):
        res.append(main(i))
    print(res)
    res = np.array(res)
    print(res)
    try:

        ret = (np.transpose(res) * e).sum(axis=1)
        print(ret)
    except TypeError:
        print('数据有误，可能不满足一致性，请调整参数矩阵后重试')
    # if __name__ == '__main__':
        # e = np.array(
        #     [[1, 3, 5, 3, 5],
        #      [1 / 3, 1, 3, 1, 3],
        #      [1 / 5, 1 / 3, 1, 1 / 3, 3],
        #      [1 / 3, 1, 3, 1, 3],
        #      [1 / 5, 1 / 3, 1 / 3, 1 / 3, 1]])
        #
        # a = np.array([
        #     [1, 1, 5],
        #     [1, 1, 5],
        #     [1 / 5, 1 / 5, 1]])
        # b = np.array([
        #     [1, 3, 5],
        #     [1 / 3, 1, 2],
        #     [1 / 5, 1 / 2, 1]])
        #
        # c = np.array([
        #     [1, 4, 7],
        #     [1 / 4, 1, 4],
        #     [1 / 7, 1 / 4, 1]])
        #
        # d = np.array([
        #     [1, 1 / 2, 1 / 3],
        #     [2, 1, 1],
        #     [3, 1, 1]])
        #
        # f = np.array([
        #     [1, 1 / 2, 1 / 3],
        #     [2, 1, 1],
        #     [3, 1, 1]]
def panding(data):
    SSE = []  # 存放每次结果的误差平方和
    for k in range(1, 9):
        estimator = KMeans(n_clusters=k)  # 构造聚类器
        estimator.fit(data)
        SSE.append(estimator.inertia_)  # estimator.inertia_获取聚类准则的总和
    X = range(1, 9)
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(X, SSE, 'o-')
    plt.savefig("手肘法图")
    plt.clf()
    Scores = []  # 存放轮廓系数
    for k in range(2, 9):
        estimator = KMeans(n_clusters=k)  # 构造聚类器
        estimator.fit(data)
        Scores.append(silhouette_score(data, estimator.labels_, metric='euclidean'))
    X = range(2, 9)
    plt.xlabel('k')
    plt.ylabel('轮廓系数')
    plt.plot(X, Scores, 'o-')
    plt.savefig("轮廓系数法")
def r_julei(data):
    print("相关系数矩阵")
    print(data.corr())
    print("请使用r")
    print("dev.new()\nX<-read.table('clipboda',header=T)\n=cor(X) \nhc<-hclust(d)\nplot(hc)")
def cengci_julei(data1,group_size):
    z_scaler = preprocessing.StandardScaler()
    print("如果列的坐标混乱，要先使用排列方法使得，数据以一定的顺序进行查找，方便查找和使用。")
    data1.sort_index()
    print("同时也要进行数据的")
    data1 = np.array(data1)
    data1 = z_scaler.fit_transform(data1)

    print("聚类分析的步骤")
    print(". 读入数据、观察数据。\
2. 确定数据是否需要标准化，进行标准化\
3. 根据数据的稀疏程度等各种指标，确认聚类的方法。\
4. 首先通过python的手肘法初步确认聚类分类的次数。\
5. 如果手肘法无法使用，使用轮廓系数法进行进一步确认。\
6. 根据确认的聚类方法和聚类类别次数，进行模型的拟合。\
7. 根据模型的弥合结果进行进一步预测，和评估结果的判断。\
8. 模型的进一步改进，参数的改变。")
    print("Single link\
单链接聚类（single link clustering）也叫最近邻聚类（nearest neighbor clustering）。两个簇之间\
的距离定义为两簇中离得最近的两个元素之间的距离：\
Complete link\
complete link clustering也叫最远邻聚类（ furthest neighbor clustering）。两个簇之间的距离定义\
为两簇中离得最远的两个元素之间的距离：\
Average link\
在实际应用中，首选的方法是平均链接聚类（average link clustering），测量所有对之间的平均距离")
    print("#进行散点图的颜色标注")
    group_size = group_size
    cls = AgglomerativeClustering(n_clusters=group_size, linkage='ward')
    cluster_group = cls.fit(data1)
    plt.clf()
    cnames = ['black', 'blue', 'yellow', 'green']
    print("# 放到 plt 中展示")
    for point, gp_id in zip(data1, cluster_group.labels_):
        plt.scatter(point[0], point[1], s=5, c=cnames[gp_id], alpha=1)
    plt.savefig("按照颜色不同标注的图.png")
    plt.clf()
    print("# 进行层次聚类分析的结果分析")
    data = data1
    plt.scatter(x=data[:, 0:1], y=data[:, 1:2], marker='.', color='red')
    n = np.arange(data.shape[0])
    for i, txt in enumerate(n):
        plt.annotate(txt, (data[i:i + 1, 0:1], data[i:i + 1, 1:2]))
    plt.savefig("聚类结果的图")
    plt.clf()
    ac = AgglomerativeClustering(n_clusters=group_size)
    clustering = ac.fit(data)
    print("每个数据所属的簇编号", clustering.labels_)
    print("每个簇的成员", clustering.children_)
    Z = linkage(data1)

    print(dendrogram(Z))
    plt.savefig("聚类分线图2.png")
### 指数曲线法（三段和值）
def e_fit(input_list):
    tmp = input_list
    if(len(input_list)%3!=0):
        tmp = np.delete(tmp,[range(0,len(input_list)%3)])
    tmp = np.split(tmp,3)
    n = len(tmp[0])
    suma = sum(tmp[0])
    sumb = sum(tmp[1])
    sumc = sum(tmp[2])
    dd = (sumc-sumb)/(sumb-suma)
    b = math.pow(abs(dd),1/n)*(-1 if (sumb-suma)<0 else 1)*(-1 if (sumc-sumb)<0 else 1)
    a = (sumb-suma)*(b-1)/((b**n-1)**2)
    k = (1/n)*(suma-a*(b**n-1)/(b-1))
    print(a,b,k)
    def log_re(t):
        return  1 / (k + a * (b ** t))
    return log_re
### 逻辑曲线进行求a，b，k （三段和值）
def log_fit(input_list):
    tmp = input_list
    if(len(input_list)%3!=0):
        tmp = np.delete(tmp,[range(0,len(input_list)%3)])
    tmp = 1/tmp
    tmp = np.split(tmp,3)
    n = len(tmp[0])
    suma = sum(tmp[0])
    sumb = sum(tmp[1])
    sumc = sum(tmp[2])
    dd = (sumc-sumb)/(sumb-suma)
    b = math.pow(abs(dd),1/n)*(-1 if (sumb-suma)<0 else 1)*(-1 if (sumc-sumb)<0 else 1)
    a = (sumb-suma)*(b-1)/(b*((b**n-1)**2))
    k = (1/n)*(suma-a*b*((b**n-1)/(b-1)))
    print(a,b,k)
    def e_fit_pre(t):
        return k + a * (b ** t)
    return e_fit_pre
### 逻辑曲线进行预测
def log_pre(a,b,k,t):
    return 1/(k+a*(b**t))
def e_smooth_next(list_input,tmp,alpha):
    a = list_input[-1]
    b = tmp[-1]
    print(alpha*a + (1-alpha)*b)
def e_smooth_n(listin,tmp,alpha):
    a = 2*listin[-1]-tmp[-1]
    b = (listin[-1]-tmp[-1])*alpha*(1-alpha)
    print("方程(预测值）为=",a,"+",b,"*n")
    c = []
    for i in range(1,16):
        tot = a+b*i
        c.append(tot)
    print(c)
def e_smooth(list_input,alpha):
    a1 = 0
    for j in range(3):
        a1 += list_input[j]
    a1 = a1/3
    tmp = []
    tmp.append(a1)
    for i in range(1,len(list_input)+1,1):
        tmp.append(alpha*list_input[i-1] + (1-alpha)*tmp[i-1])
    tmp.pop(0)
    return tmp
def move_smooth(list_input,alpha):
    tmp = []
#     print(len(list_input))
    for i in range(alpha-1):
        tmp.append(math.nan)
    for i in range(alpha,len(list_input)+1):
#         print(1)
        mean = sum(list_input[(i-alpha):i])/alpha
        tmp.append(mean)
    return tmp
def smooth_next(list_real,list_move,alpha,n):
    real = list_real[-1]
    move = list_move[-1]
    a = 2*real -move
    b = (2/(alpha-1))*(real-move)
    print("模型为",a,"+",b,"* n")
    return a + b*n
def yieryidong(aa,day,alpha,late = 1):
    import matplotlib.pyplot as plt
    print("转化时间序列的坐标值（转化为【-12,12】或者【0,12】或者【1,12】）\
时间序列作为x轴，以观察值作为y轴，绘制散点图观察是否有趋势\
（有趋势）（季节性），有季节性应该通过季节性的时间序列分析\
（有趋势）（无季节性），使用简单移动平均，加权移动平均，指数平滑法进行预测\
（有趋势）（无季节性）（有饱和值）三类生长曲线\
（有趋势）（有季节性）（无饱和值）（有波动）使用arima进行预测\
进行时间序列模型的验证（交叉验证，选择评估指标）")
    a = pd.DataFrame(aa, columns=["x", "mean_1", "mean_2", "smooth"])
    a["x"] = aa.iloc[:,0]
    a['mean_1'] = move_smooth(np.array(a['x']), day)
    a['mean_2'] = move_smooth(np.array(a['mean_1']), day)
    a['smooth'] = e_smooth(np.array(a['x']), alpha)
    a['smooth2'] = e_smooth(np.array(a['smooth']),alpha)
    a['smooth3'] = e_smooth(np.array(a['smooth2'],alpha))
    plt.figure(figsize=(15, 7))
    plt.grid(True)
    plt.plot(a["x"])
    plt.savefig("时间序列趋势图.png")
    plt.clf()
    print("首先要进行时间坐标的转换，即转化为时间坐标均值为0")
    print("二次平均法后以及加总上一次二次指数平滑法之后的数据")
    print(a)
    print("指数平滑法进行预测")
    print("一次指数平滑只能预测以后一个周期")
    e_smooth_next(np.array(a['x']), np.array(a['smooth']), alpha)
    print("二次指数平滑，可以推算出曲线,以下为方程")
    e_smooth_n(np.array(a['smooth']),np.array(a['smooth2']),alpha)
    print("三次次指数平滑，可以推算出曲线,以下为方程")
    e_smooth_n(np.array(a['smooth2']), np.array(a['smooth3']), alpha)
    print("二次平均法进行预测往后1期")
    smooth_next(np.array(a['mean_1']), np.array(a['mean_2']), day, late)
    print("一次平均法进行预测往后1期")
    smooth_next(np.array(a['x']), np.array(a['mean_1']), day, late)
def judge(x):
    import pandas as pd
    import numpy as np
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from scipy.stats import kstest
    import scipy.stats as stats
    from sklearn.preprocessing import PolynomialFeatures
    import statsmodels.api as sm
    from scipy.stats import pearsonr
    from scipy.stats import chi2_contingency
    from scipy.stats import shapiro
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tsa import stattools
    from scipy.stats import f_oneway
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn import preprocessing
    print("检验正态性")
    for i in range(x.shape[1]):
        stat, p = shapiro(x[:, i])
        if (p < 0.05):
            print("变量", i, "正态性良好", "p-value", p)
        else:
            print("变量", i, "正态性不好", "p-value", p)
    print("检验多重共线性（VIF）")
    vif = pd.DataFrame()
    for i in range(x.shape[1]):
        a = variance_inflation_factor(x, 0)
        print("变量", i, "vif", a)
    print("检验自相关")
    for i in range(x.shape[1]):
        a = stattools.acf(x[:, i],nlags=x.shape[0]-1)
        print("变量", i, "自相关系数为", a)

    print("检验同方差性")
    for i in range(x.shape[1]):
        if (i < x.shape[1]):
            for j in range(i, x.shape[1]):
                stat, p = f_oneway(x[:, i], x[:, j])
                print(p)
                if (p < 0.05):

                    print("变量", i, "与", j, "方差具有齐性")
                else:
                    print("变量", i, "与", j, "方差不具有齐性")
def Regression(pddata):
    # 要保证传入的pddata的列名字已经修改为指定的值
    import pandas as pd
    import numpy as np
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from scipy.stats import kstest
    import scipy.stats as stats
    from sklearn.preprocessing import PolynomialFeatures
    import statsmodels.api as sm
    from scipy.stats import pearsonr
    from scipy.stats import chi2_contingency
    from scipy.stats import shapiro
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tsa import stattools
    from scipy.stats import f_oneway
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn import preprocessing
    pddata = pddata

    print("*初步观察数据(前10行数据）")
    print(pddata.head(10))
    print("*描述性统计")
    print(pddata.describe())
    print("***描述指标概览")

    print("***散点图矩阵")
    pd.plotting.scatter_matrix(pddata, alpha=0.5,  figsize=None, ax=None, diagonal='hist', marker='.',
                               density_kwds=None, hist_kwds=None, range_padding=0.05)
    plt.title('180411105')
    # plt.legend()
    plt.savefig("散点图矩阵.png")
    plt.clf()
    print("#这里是一些对变量的描述")
    print("***进一步的相关系数矩阵")
    print(np.corrcoef(np.array(pddata)))
    print("***更直观的表达方式——相关系数热力图")
    b = sns.heatmap(np.corrcoef(np.array(pddata)))
    fig = b.get_figure()
    fig.savefig('相关系数矩阵热力图散点图.png')
    plt.clf()
    print("*数据的预处理")
    print("***重复值判断")
    result1 = pddata.duplicated()
    if result1.any() == True:
        print("有重复值，执行删除操作")
    else:
        print("无重复值")
    print("***异常值离散值离群值判断（通过其必须在均值的三个标准差判断的区间进行估计）P(|x−μ|>3σ)≤0.003同时(使用箱线图）")
    for i in pddata.columns:
        a = sns.boxplot(x = pddata[i])
        fig = a.get_figure()
        fig.savefig('异常值判断'+i+".png")
    print("***由于数据量较小，如果离散值进行全部的删除操作，会影响效果的展示，影响不好，所以，在这步操作中，只进行展示")
    print("*数据的标准化")
    print("***观察到数据的粒度相差较大，所以相对应的进行样本的标准化")
    z_scaler = preprocessing.StandardScaler()
    y = np.array(pddata["y"])
    pddata = pddata.drop(labels="y",axis=1)
    npdata = np.array(pddata)
    npdata = z_scaler.fit_transform(npdata)
    print("标准化之后的数据显示")
    print(npdata)
    print("*对模型的先验概率")

    judge(npdata)
    print("*下一步进行对模型进行拟合操作，请通过返回的np数组进行传入下一步中，oneway或者twoway")

    print("*进行二次模型的拟合")
    return npdata,y
def makemodel(X1,y):
    import pandas as pd
    import numpy as np
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from scipy.stats import kstest
    import scipy.stats as stats
    from sklearn.preprocessing import PolynomialFeatures
    import statsmodels.api as sm
    from scipy.stats import pearsonr
    from scipy.stats import chi2_contingency
    from scipy.stats import shapiro
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tsa import stattools
    from scipy.stats import f_oneway
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn import preprocessing
    model = sm.OLS(y, X1).fit()
    print("*模型参数总览")
    print(model.summary())
    print("以下，进行模型相关检验")
    print("首先进行模型的主观假设检验")
    print("基本假定:"
          "β！=0")
    print("R检验")
    print("R值为",model.rsquared)
    print("t检验")
    print("t值为",model.tvalues)
    print("如果p>|t|这一列<=0.05,说明通过t检验，拒绝原假设")
    print("F检验")
    print("p值为", model.f_pvalue)
    if model.f_pvalue < 0.05:
        print("通过f检验，拒绝原假设")
    else:
        print("接受原假设")
    print("*模型参数细分，以及相应的参数判断，另外还有模型参数的区间分布。")
    print("# 提取回归系数")
    print(model.params)

    print("# 提取回归系数标准差")
    print(model.bse)

    print("# 提取回归系数p值")
    print(model.pvalues)

    print("# 提取回归系数t值")
    print(model.tvalues)

    print("# 提取回归系数置信区间model.conf_int() 默认5%，括号中可填具体数字 比如0.05, 0.1")
    print(model.conf_int())

    print("# 提取模型预测值")
    print(model.fittedvalues)

    print("# 提取残差")
    print(model.resid)

    print("# 模型自由度（系数自由度）")
    print(model.df_model)

    print("# 残差自由度（样本自由度）")
    print(model.df_resid)

    print("# 模型样本数量")
    print(model.nobs)

    print("##模型评价类")
    print("# 提取R方")
    print(model.rsquared)

    print("# 提取调整R方")
    print(model.rsquared_adj)

    print(" # 提取AIC")
    print(model.aic)

    print(" # 提取BIC")
    print(model.bic)

    print("# 提取F-statistic")
    print(model.fvalue)

    print("# 提取F-statistic 的pvalue")
    print(model.f_pvalue)

    print("# 模型mse")
    print(model.mse_model)

    print("# 残差mse")
    print(model.mse_resid)

    print("# 总体mse")
    print(model.mse_total)

    print(" # 协方差矩阵比例因子")
    print(model.scale)

    print(" #  White异方差稳健标准误")
    print(model.HC0_se)

    print(" # MacKinnon和White（1985）的异方差稳健标准误")
    print(model.HC1_se)

    print("#  White异方差矩阵")
    print(model.cov_HC0)

    print("# MacKinnon和White（1985）的异方差矩阵")
    print(model.cov_HC1)
    return model
def oneway(npdata,y):
    import pandas as pd
    import numpy as np
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from scipy.stats import kstest
    import scipy.stats as stats
    from sklearn.preprocessing import PolynomialFeatures
    import statsmodels.api as sm
    from scipy.stats import pearsonr
    from scipy.stats import chi2_contingency
    from scipy.stats import shapiro
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tsa import stattools
    from scipy.stats import f_oneway
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn import preprocessing
    print("*一次方程的拟合")
    print("***这一步代表以上的变量已经选择完毕")
    print("***进行一次方程的最小二乘法的拟合")
    X1 = sm.add_constant(npdata)
    def tran(x):
        return sm.add_constant(x)
    model = makemodel(X1,y)
    nihepic(model)
    return model,tran
def twoway(npdata,y):
    import pandas as pd
    import numpy as np
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from scipy.stats import kstest
    import scipy.stats as stats
    from sklearn.preprocessing import PolynomialFeatures
    import statsmodels.api as sm
    from scipy.stats import pearsonr
    from scipy.stats import chi2_contingency
    from scipy.stats import shapiro
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tsa import stattools
    from scipy.stats import f_oneway
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn import preprocessing
    print("*一次方程的拟合")
    print("***这一步代表以上的变量已经选择完毕")
    print("***进行一次方程的最小二乘法的拟合")
    poly_reg = PolynomialFeatures(degree=2)
    X1 = poly_reg.fit_transform(npdata)
    X1 = sm.add_constant(X1)


    model = makemodel(X1, y)
    def tran(x):
        poly_reg = PolynomialFeatures(degree=2)
        x = poly_reg.fit_transform(x)
        x = sm.add_constant(x)

        return x
    nihepic(model)
    return model,tran
def nihepic(model):
    import pandas as pd
    import numpy as np
    import sklearn
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from scipy.stats import kstest
    import scipy.stats as stats
    from sklearn.preprocessing import PolynomialFeatures
    import statsmodels.api as sm
    from scipy.stats import pearsonr
    from scipy.stats import chi2_contingency
    from scipy.stats import shapiro
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    from statsmodels.tsa import stattools
    from scipy.stats import f_oneway
    import seaborn as sns
    import matplotlib.pyplot as plt
    from sklearn import preprocessing
    fig = plt.figure(figsize=(25, 18))
    fig = sm.graphics.plot_partregress_grid(model, fig=fig)

    fig.savefig('偏回归图', dpi=300)
    plt.clf()
    print("partial regression plot 偏回归图，是呈现了模型中已有一个或多个自变量的情况下，新增一个自变量对模型产生的影响。")


















