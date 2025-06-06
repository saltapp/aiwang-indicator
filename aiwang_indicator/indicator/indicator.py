#以下所有函数如无特别说明，输入参数S均为numpy序列或者列表list，N为整型int 
#应用层1级函数完美兼容通达信或同花顺，具体使用方法请参考通达信 

import numpy as np
import pandas as pd

#------------------ 0级：核心工具函数 --------------------------------------------      
def RD(N,D=3):   return np.round(N,D)        #四舍五入取3位小数 
def RET(S,N=1):  return np.array(S)[-N]      #返回序列倒数第N个值,默认返回最后一个
def ABS(S):      return np.abs(S)            #返回N的绝对值
def LN(S):       return np.log(S)            #求底是e的自然对数,
def POW(S,N):    return np.power(S,N)        #求S的N次方
def SQRT(S):     return np.sqrt(S)           #求S的平方根
def SIN(S):      return np.sin(S)            #求S的正弦值（弧度)
def COS(S):      return np.cos(S)            #求S的余弦值（弧度)
def TAN(S):      return np.tan(S)            #求S的正切值（弧度)  
def MAX(S1,S2):  return np.maximum(S1,S2)    #序列max
def MIN(S1,S2):  return np.minimum(S1,S2)    #序列min
def IF(S,A,B):   return np.where(S,A,B)      #序列布尔判断 return=A  if S==True  else  B


def REF(S, N=1):          #对序列整体下移动N,返回序列(shift后会产生NAN)    
    return pd.Series(S).shift(N).values  

def DIFF(S, N=1):         #前一个值减后一个值,前面会产生nan 
    return pd.Series(S).diff(N).values     #np.diff(S)直接删除nan，会少一行

def STD(S,N):             #求序列的N日标准差，返回序列    
    return  pd.Series(S).rolling(N).std(ddof=0).values     

def SUM(S, N):            #对序列求N天累计和，返回序列    N=0对序列所有依次求和         
    return pd.Series(S).rolling(N).sum().values if N>0 else pd.Series(S).cumsum().values  

def CONST(S):             #返回序列S最后的值组成常量序列
    return np.full(len(S),S[-1])
  
def HHV(S,N):             #HHV(C, 5) 最近5天收盘最高价        
    return pd.Series(S).rolling(N).max().values     

def LLV(S,N):             #LLV(C, 5) 最近5天收盘最低价     
    return pd.Series(S).rolling(N).min().values    
    
def HHVBARS(S,N):         #求N周期内S最高值到当前周期数, 返回序列
    return pd.Series(S).rolling(N).apply(lambda x: np.argmax(x[::-1]),raw=True).values 

def LLVBARS(S,N):         #求N周期内S最低值到当前周期数, 返回序列
    return pd.Series(S).rolling(N).apply(lambda x: np.argmin(x[::-1]),raw=True).values    
  
def MA(S,N):              #求序列的N日简单移动平均值，返回序列                    
    return pd.Series(S).rolling(N).mean().values  
  
def EMA(S,N):             #指数移动平均,为了精度 S>4*N  EMA至少需要120周期     alpha=2/(span+1)    
    return pd.Series(S).ewm(span=N, adjust=False).mean().values     

def SMA(S, N, M=1):       #中国式的SMA,至少需要120周期才精确 (雪球180周期)    alpha=1/(1+com)    
    return pd.Series(S).ewm(alpha=M/N,adjust=False).mean().values           #com=N-M/M

def WMA(S, N):            #通达信S序列的N日加权移动平均 Yn = (1*X1+2*X2+3*X3+...+n*Xn)/(1+2+3+...+Xn)
    return pd.Series(S).rolling(N).apply(lambda x:x[::-1].cumsum().sum()*2/N/(N+1),raw=True).values 

def DMA(S, A):            #求S的动态移动平均，A作平滑因子,必须 0<A<1  (此为核心函数，非指标）
    if isinstance(A,(int,float)):  return pd.Series(S).ewm(alpha=A,adjust=False).mean().values    
    A=np.array(A);   A[np.isnan(A)]=1.0;   Y= np.zeros(len(S));   Y[0]=S[0]     
    for i in range(1,len(S)): Y[i]=A[i]*S[i]+(1-A[i])*Y[i-1]      #A支持序列 by jqz1226         
    return Y             
  
def AVEDEV(S, N):         #平均绝对偏差  (序列与其平均值的绝对差的平均值)   
    return pd.Series(S).rolling(N).apply(lambda x: (np.abs(x - x.mean())).mean()).values 

def SLOPE(S, N):          #返S序列N周期回线性回归斜率            
    return pd.Series(S).rolling(N).apply(lambda x: np.polyfit(range(N),x,deg=1)[0],raw=True).values

def FORCAST(S, N):        #返回S序列N周期回线性回归后的预测值， jqz1226改进成序列出    
    return pd.Series(S).rolling(N).apply(lambda x:np.polyval(np.polyfit(range(N),x,deg=1),N-1),raw=True).values  

def LAST(S, A, B):        #从前A日到前B日一直满足S_BOOL条件, 要求A>B & A>0 & B>=0 
    return np.array(pd.Series(S).rolling(A+1).apply(lambda x:np.all(x[::-1][B:]),raw=True),dtype=bool)

def INDEX(S):             #将序列S转化为指数化序列，首日为1000，后续按涨跌幅递推
    S = np.array(S, dtype=float)
    idx = np.zeros(len(S))
    if len(S) == 0:
        return idx
    idx[0] = 1000
    for i in range(1, len(S)):
        if S[i-1] == 0:
            idx[i] = idx[i-1]
        else:
            idx[i] = idx[i-1] * (S[i] / S[i-1])
    return idx

def CUMPROD(S):              #对输入序列S进行累计乘积，返回同长度的序列。例如：S=[1,2,3,4]，返回[1,2,6,24]
    S = np.array(S, dtype=float)
    # 将nan替换为1（累计乘积的中性元素）
    S[np.isnan(S)] = 1
    return np.cumprod(S)
  
#------------------   1级：应用层函数(通过0级核心函数实现）使用方法请参考通达信--------------------------------
def COUNT(S, N):                       # COUNT(CLOSE>O, N):  最近N天满足S_BOO的天数  True的天数
    return SUM(S,N)    

def EVERY(S, N):                       # EVERY(CLOSE>O, 5)   最近N天是否都是True
    return  IF(SUM(S,N)==N,True,False)                    
  
def EXIST(S, N):                       # EXIST(CLOSE>3010, N=5)  n日内是否存在一天大于3000点  
    return IF(SUM(S,N)>0,True,False)

def FILTER(S, N):                      # FILTER函数，S满足条件后，将其后N周期内的数据置为0, FILTER(C==H,5)
    for i in range(len(S)): S[i+1:i+1+N]=0  if S[i] else S[i+1:i+1+N]        
    return S                           # 例：FILTER(C==H,5) 涨停后，后5天不再发出信号 
  
def BARSLAST(S):                       #上一次条件成立到当前的周期, BARSLAST(C/REF(C,1)>=1.1) 上一次涨停到今天的天数 
    M=np.concatenate(([0],np.where(S,1,0)))  
    for i in range(1, len(M)):  M[i]=0 if M[i] else M[i-1]+1    
    return M[1:]                       

def BARSLASTCOUNT(S):                  # 统计连续满足S条件的周期数        by jqz1226
    rt = np.zeros(len(S)+1)            # BARSLASTCOUNT(CLOSE>OPEN)表示统计连续收阳的周期数
    for i in range(len(S)): rt[i+1]=rt[i]+1  if S[i] else rt[i+1]
    return rt[1:]  
  
def BARSSINCEN(S, N):                  # N周期内第一次S条件成立到现在的周期数,N为常量  by jqz1226
    return pd.Series(S).rolling(N).apply(lambda x:N-1-np.argmax(x) if np.argmax(x) or x[0] else 0,raw=True).fillna(0).values.astype(int)
  
def CROSS(S1, S2):                     # 判断向上金叉穿越 CROSS(MA(C,5),MA(C,10))  判断向下死叉穿越 CROSS(MA(C,10),MA(C,5))   
    return np.concatenate(([False], np.logical_not((S1>S2)[:-1]) & (S1>S2)[1:]))    # 不使用0级函数,移植方便  by jqz1226
    
def LONGCROSS(S1,S2,N):                # 两条线维持一定周期后交叉,S1在N周期内都小于S2,本周期从S1下方向上穿过S2时返回1,否则返回0         
    return  np.array(np.logical_and(LAST(S1<S2,N,1),(S1>S2)),dtype=bool)            # N=1时等同于CROSS(S1, S2)
    
def VALUEWHEN(S, X):                   # 当S条件成立时,取X的当前值,否则取VALUEWHEN的上个成立时的X值   by jqz1226
    return pd.Series(np.where(S,X,np.nan)).ffill().values  

def BETWEEN(S, A, B):                  # S处于A和B之间时为真。 包括 A<S<B 或 A>S>B
    return ((A<S) & (S<B)) | ((A>S) & (S>B))  

def TOPRANGE(S):                       # TOPRANGE(HIGH)表示当前最高价是近多少周期内最高价的最大值 by jqz1226
    rt = np.zeros(len(S))
    for i in range(1,len(S)):  rt[i] = np.argmin(np.flipud(S[:i]<S[i]))
    return rt.astype('int')

def LOWRANGE(S):                       # LOWRANGE(LOW)表示当前最低价是近多少周期内最低价的最小值 by jqz1226
    rt = np.zeros(len(S))
    for i in range(1,len(S)):  rt[i] = np.argmin(np.flipud(S[:i]>S[i]))
    return rt.astype('int')
