import numpy as np
import pandas as pd
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import numbers
from scipy import stats
from scipy.ndimage.interpolation import shift

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
months_long = ["January", "February", "March", "April", "May", "June", "July",
               "August", "September", "October", "November", "December"]

# Number format change
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return np.trunc(stepper * number) / stepper


def to_perc(number) -> float:
    return np.trunc(number*10000) / 100


def to_bp(number) -> float:
    return np.trunc(number*100000) / 10


def isNaN(input):
    return input != input

# ---- Dates ----
def prevwday(d):
    return d - timedelta(days=(d.weekday()+1) % 7+2 if d.weekday() % 6 == 0 else 1)

def previous_eom(_date, k=1):
    if k > 1:
        _date = previous_eom(_date, k-1)
    return date(_date.year, _date.month, 1) - timedelta(days=1)

def fromDate2YYYYMMDD(dt):
    return str(dt.year) + dt.strftime('%m') + dt.strftime('%d')


def fromPy2Excel(Py_date):
    return Py_date.toordinal() + 2 - date(1900, 1, 1).toordinal()


def fromPy2Isonum(dt):
    return int(dt.year*10000+dt.month*100+dt.day)


def fromExcel2Py(SQL_date):
    return date.fromordinal(date(1900, 1, 1).toordinal() + SQL_date - 2)


def fromDate2ExcelNumber(x):  # transform a list of date into an np array with the numeric representation of excel
    d0 = date(1899, 12, 31)
    y = (x - d0).days
    return y + 1

def fromExcelNumber2Date(x):
    y = date(1899, 12, 30) + timedelta(days=x)
    return y


def fromExcelNumber2DateList(x):
    y = [date(1899, 12, 30) + timedelta(days=xx) for xx in x]
    return y


def fromDate2ExcelNumberArray(x):  # transform a list of date into an np array with the numeric representation of excel
    d0 = date(1899, 12, 31)
    x_ = [(date.date() - d0).days for date in x]
    y = np.array(x_)
    return y + 1

def yearShift(x, numberOfYears):
    return x + relativedelta(years=numberOfYears)


def monthShift(x, numberOfMonths):
    return x + relativedelta(months=numberOfMonths)


def dayShift(x, numberOfDays):
    return x + timedelta(days=numberOfDays)


def nearest_less_equal(items, pivot):
    return min([i for i in items if i <= pivot], key=lambda x: abs(x - pivot))


# ---- Time Series Modification ----
def get_ar(a, k=1):
    return np.corrcoef(a[k:],a[:-k])[0][1]


def fromRet2PriceSeries(x):
    y =[]
    y.append(100)
    x = x.fillna(0)  # replace nan with 0
    for i in range(len(x)-1):
        y.append(y[i] * (1 + x.iloc[i+1] / 100))
    z = pd.DataFrame(y, columns=x.columns)
    tmp = shift(np.array(x.index), 1, cval=np.NaN)
    tmp[0] = tmp[1]-1
    z.index = tmp
    return z


def fromRet2PriceMatrix(x):
    y = [100 * np.ones(x.shape[1])]
    x_1 = x.fillna(0).values  # replace nan with 0
    for i in range(x.shape[0]):
        y.append(np.multiply(y[i], (1 + x_1[i])))
    z = pd.DataFrame(y, columns=x.columns)
    if isinstance(x.index[0], date):
        z.index = x.index.insert(0, dayShift(x.index[0], -1))
    else:
        z.index = x.index.insert(0, x.index[0]-1)
    return z

# Function to compute a composite z-score
# INPUT: a DataFrame with the items as the index of the DF and the indicators as the columns

def z_score(x, weights):
    col = list(x)
    y = x.copy()
    for i in col:
        imax = max(x[i])
        imin = min(x[i])
        idif = imax-imin
        y[i] = (x[i]-imin)/idif if idif != 0 else x[i]*0

    score = -np.array(y.apply(lambda t: np.dot(t, np.array(weights)), axis=1))
    ranks = score.argsort()
    output = y.index.array[ranks]
    return output


# ---- Match Functions ----

def match_position(a, b):  # find position of elements of a in b
    a = [a] if isinstance(a, (str, numbers.Number)) else np.array(a).tolist()
    b = [b] if isinstance(a, (str, numbers.Number)) else np.array(b).tolist()
    output = [b.index(x) if x in b else None for x in a]
    return output


def match_common_elements(a,b):  # find the elements of a that are also in b taken only once
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return np.array(list(a_set & b_set))
    else:
        return None

# ---- Time Series ----

# Time Series Cleaning and Alignment

def timeseries_aligment(df1, df2):  # Allign two timeseries expressed as dataframes and fill NA with previous values
    tmp = pd.concat([df1, df2], axis=1, sort=False)
    tmp = tmp.dropna(axis=0, how='all')  # drop all common NA
    tmp = tmp.fillna(method='ffill')
    tmp = tmp.fillna(method='bfill')  # this line is to fill initial NA
    df1_alig = tmp[df1.columns]
    df2_alig = tmp[df2.columns]
    output = [df1_alig, df2_alig]
    return output


def returns_aligment(df1, df2):
    tmp = pd.concat([df1, df2], axis=1, sort=False)
    tmp = tmp.dropna(axis=0, how='all')  # drop all common NA
    tmp = tmp.sort_index().fillna(0)
    df1_alig = tmp[df1.columns]
    df2_alig = tmp[df2.columns]
    output = [df1_alig, df2_alig]
    return output


def rebase_timeseries(df1):
    df1 = df1.sort_index()
    tmp = df1.dropna(axis=0, how='all')  # drop all common NA
    tmp = tmp.fillna(method='ffill')
    tmp = tmp.fillna(method='bfill')
    output = tmp.divide(tmp.iloc[0]/100)
    return output


# Max DD

def get_max_dd(data):
    maxdd = 1
    data = np.array(data)
    old = data[0]
    for i in range(1, len(data)):
        new = data[i]
        ret = new/old-1
        if ret <=0:
            for k in range(i, len(data)):
                lret = data[k]/old-1
                if lret >= 0:
                    break
                else:
                    maxdd = min(lret, maxdd)
        old = new
    return maxdd


def max_dd_len(data):
    len_maxdd = 0
    data = np.array(data)
    old = data[0]
    for i in range(1, len(data)):
        new = data[i]
        ret = new/old-1
        if ret <=0:
            for k in range(i, len(data)):
                lret = data[k]/old-1
                len_dd = k - i + 1
                if lret >= 0:
                    break
                else:
                    len_maxdd = max(len_dd, len_maxdd)
        old = new
    return -len_maxdd


def max_dd_len_wrapper(ret, rf):
    prices = fromRet2PriceMatrix(ret)
    return prices.apply(max_dd_len, axis=0)


def max_dd_from_ret(ret):
    prices = fromRet2PriceMatrix(ret)
    return prices.apply(get_max_dd, axis=0)

# Downside Deviation

def downside_deviation(ret):
    dwn_dev = np.std(ret[ret < 0])
    return dwn_dev * np.sqrt(len(ret))


# Lower Partial Moment, works on matrices

def lpm(returns, threshold, order):
    # This method returns a lower partial moment of the returns
    # Create an array he same length as returns containing the minimum return threshold
    threshold_array = np.empty((returns.shape[0], returns.shape[1]))
    threshold_array.fill(threshold)
    # Calculate the difference between the threshold and the returns
    diff = threshold_array - returns
    # Set the minimum of each to 0
    diff = np.clip(diff, a_min=0, a_max=500)
    # Return the sum of the different to the power of order
    return np.sum(diff ** order, axis=0) / returns.shape[0]


# Sortino Ratio, works on matrices

def sortino_ratio(ret, rf, target=0):
    s = ret.shape[0]
    gmean_ret = (1 + ret).prod(axis=0) ** (260 / s)
    gmean_rf = (1 + rf).prod(axis=0) ** (260 / s)
    return (gmean_ret-gmean_rf.values[0]) / (np.sqrt(lpm(ret, target, 2)) * np.sqrt(260))


# Sharpe Ratio, works on dataframes
def sharpe_ratio(ret, rf):
    s = ret.shape[0]
    gmean_ret = (1+ret).prod(axis=0)**(260/s)
    gmean_rf = (1+rf).prod(axis=0)**(260/s)
    return (gmean_ret-gmean_rf.values[0]) / (np.std(ret.subtract(rf.iloc[:,0], axis=0)) * np.sqrt(260))


# Calmar Ratio, works on matrices

def calmar_ratio(ret, rf):
    prices = fromRet2PriceMatrix(ret)
    dd = prices.apply(get_max_dd, axis=0, raw=True)
    tot_ret = np.prod((ret + 1), axis=0)-1
    tot_rf = (np.prod((rf + 1))-1).value
    return (tot_ret - tot_rf) / abs(dd)


def ann_ret_from_prices(prices):
    x = (prices.iloc[-1, :]/prices.iloc[0, :])**(252/prices.shape[0])-1
    return x


def ann_ret(ret):
    x = np.prod((ret + 1), axis=0)**(252/ret.shape[0])-1
    return x


def tot_ret(ret):
    t_ret = np.prod((ret + 1), axis=0)-1
    return t_ret


def tot_ret_wrapper(ret, rf):
    return tot_ret(ret)


def tot_ret_from_price(price):
    t_ret = price.iloc[-1, :]/price.iloc[0, :]-1
    return t_ret


def ann_vol(ret):
    return np.std(ret) * np.sqrt(252)


def ret_vol(ret):
    x = ann_ret(ret)/ann_vol(ret)
    return x
# ---- Presentation ----


def clean_name_for_excel(name, leng):
    data = str(name).replace("/", "-").strip()
    return str((data[:leng]) if len(data) > leng else data)


def string_truncate(stri, num_car):
    if isNaN(stri) or (stri is None):
        output = ""
    else:
        output = stri[:num_car] if len(stri) > num_car else stri
    return output


def performance_ranking(df, type_ranking):
    for col in df.columns:
        i = df.columns.get_loc(col)
        df[col + "_r"] = (-type_ranking[i] * df[col]).argsort().argsort() + 1
    return df

def performance_ranking_from_dic(df, type_ranking):
    df_2 = pd.DataFrame()
    for col in df.columns:
        df_2[col] = df[col]
        df_2[col + "_r"] = (-type_ranking[col] * df[col]).argsort().argsort() + 1
    return df_2


def table_number_formatting(df, dict):
    for col in dict:
        if col in df.columns:
            df[col] = round((df[col] * dict[col][0]), dict[col][1])
    return df




# ts = (np.array([np.random.normal(1/10000,13/10000) for i in range(500)])+1).cumprod()


# ---- Data Cleaning ----

def detect_outliers_series(x):
    z_score = stats.zscore(x)
    output = x[z_score > 2]  # more than 2 standard deviation away
    return output

def detect_outliers(x):
    y = x.unstack().reset_index()
    z_score = stats.zscore(y.iloc[:, 2])
    output = y.loc[z_score > 2, :]  # more than 2 standard deviation away
    return output

def detect_outliers_daily_ret(x, threshold):
    y = x.unstack().reset_index()
    y = y.rename(columns={0: 'value'})
    output = y.loc[abs(y.iloc[:, 2]) > threshold, :]  # more than 2 standard deviation away
    return output



# ---- Miscellaneous ----

def unique(in_list):
    return list(dict.fromkeys(in_list))

def key_2_string(l):
    return "--" + "--".join([str(ll) for ll in l])+"--"


def sumprod(a,b):
    return np.ravel(np.dot(a,b))[0]


def commalist(in_list):
    res = ""
    for a in range(len(in_list)):
        res = res + "\'"+str(in_list[a])+"\'"
        if a != len(in_list)-1:
            res = res + ","

    return res


#works on numpy array
def vols_2_srri(vols):
    bins = np.array([0.5, 2, 5, 10, 15, 25, 1000])/100
    return np.digitize(vols, bins, right=True) + 1


