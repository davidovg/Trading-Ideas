import numpy as np
import pandas as pd



def _get_smooth(ts, smooth_lag):
    smooth = ts

    if smooth_lag > 1:
        smooth = np.cumsum(ts, dtype=float)
        smooth[smooth_lag:] = smooth[smooth_lag:] - smooth[:-smooth_lag]
        smooth[:] = smooth[:] / smooth_lag
        smooth[:smooth_lag - 1] = np.nan

    return smooth


# Length in Business Days
def get_momentum(ts, lag=260, smooth_lag=3):
    smooth = _get_smooth(ts, smooth_lag)
    res = np.empty(ts.shape)*np.nan
    res[smooth_lag+lag-1:] = smooth[smooth_lag+lag-1:] / smooth[smooth_lag:-lag+1]-1
    return res


def fut_mom_distribution(ts, lag=260, smooth_lag=3, target_date=44181, n_scens=10000, hist_len=750):
    if target_date <= ts.index.max():
        print("momentum for already present {}".format(target_date))
        mom_df = ts.apply(get_momentum, axis=0, raw=True, args=(lag, smooth_lag))
        mom = mom_df.loc[ts.index[ts.index <= target_date].max()]
        return pd.DataFrame(data= np.ones((n_scens,1)) * mom.values.reshape((1, len(mom))),
                            columns=mom.index)
    else:
        jump_date = ts.index[ts.index <= target_date].max()
        if len(ts.loc[:jump_date]) < hist_len:
            n_l = len(ts.loc[:jump_date])
            print("Noth enough history, using {} instead of {}".format(n_l, hist_len))
            hist_len = n_l

        smooth = ts.apply(_get_smooth, axis=0, raw=True, args=[smooth_lag])
        start_vals = smooth.iloc[ts.index.get_loc(jump_date) - lag]

        end_val_start = smooth.loc[jump_date]
        jump_length = int((target_date - jump_date)/7*5)

        assert hist_len > jump_length, "Not enough data"

        #assess if using smooth instead is better, remember to trim smooth nans off
        log_vals = ts.apply(np.log).values[-hist_len:]
        log_returns = log_vals[jump_length:, :] - log_vals[:-jump_length,:]

        data_dim = hist_len - jump_length
        rand = np.random.normal(0, 1, (int(n_scens/2), data_dim))
        rand = np.concatenate((rand, rand * -1), axis=0)

        drift = np.mean(log_returns, axis=0)
        centered_log_returns = log_returns- drift
        sigma_adj = data_dim ** 0.5
        log_ret_scens = np.matmul(rand, centered_log_returns) / sigma_adj + drift

        log_scens = log_ret_scens + np.ones((n_scens, 1)) * end_val_start.map(np.log).values.reshape((1, len(end_val_start)))
        price_scens = pd.DataFrame(log_scens, columns=end_val_start.index).apply(np.exp)
        mom_scens = price_scens / start_vals - 1

        return mom_scens


