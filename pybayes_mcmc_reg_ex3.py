import numpy as np
import scipy.stats as st
import scipy.linalg as la
import pymc3 as pm
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

FontPath = '/Users/knysmchr/Downloads/IPAexfont00301/ipaexg.ttf'
jpfont = FontProperties(fname=FontPath)


def main():
    # 回帰モデルからのデータ生成
    n = 50
    np.random.seed(99)
    u = st.norm.rvs(scale=0.7, size=n)
    x1 = st.uniform.rvs(loc=-np.sqrt(3.0), scale=2.0*np.sqrt(3.0), size=n)
    x2 = st.uniform.rvs(loc=-np.sqrt(3.0), scale=2.0*np.sqrt(3.0), size=n)
    y = 1.0 + 2.0 * x1 - x2 + u
    X = np.stack((np.ones(n), x1, x2), axis=1)
    # 回帰モデルの係数と誤差項の分散の事後分布の設定
    k = X.shape[1]
    b0 = np.zeros(k)
    A0 = 0.2 * np.eye(k)
    nu0 = 5.0
    lam0 = 7.0
    sd0 = np.sqrt(np.diag(la.inv(A0)))
    multiple_regression = pm.Model()
    with multiple_regression:
        sigma2 = pm.InverseGamma('sigma2', alpha=0.5*nu0, beta=0.5*lam0)
        b = pm.MvNormal('b', mu=b0, tau=A0, shape=k)
        y_hat = pm.math.dot(X, b)
        likelihood = pm.Normal('y', mu=y_hat, sd=pm.math.sqrt(sigma2), observed=y)
    # 事後分布からのサンプリング
    n_draws = 5000
    n_chains = 4
    n_tunes = 1000
    with multiple_regression:
        trace = pm.sample(draws=n_draws, chains=n_chains, tune=n_tunes, random_seed=123)
    print(pm.summary(trace))
    # 事後分布のグラフの作成
    fig, ax = plt.subplots(k+1, 2, num=1, figsize=(8, 1.5*(k+1)), facecolor='w')
    for index in range(k+1):
        if index < k:
            mc_trace = trace['b'][:, index]
            x_min = mc_trace.min() - 0.2 * np.abs(mc_trace.min())
            x_max = mc_trace.max() + 0.2 * np.abs(mc_trace.max())
            x = np.linspace(x_min, x_max, 250)
            prior = st.norm.pdf(x, loc=b0[index], scale=sd0[index])
            y_label = '$\\beta_{:<d}$'.format(index+1)
        else:
            mc_trace = trace['sigma2']
            x_min = 0.0
            x_max = mc_trace.max() + 0.2 * np.abs(mc_trace.max())
            x = np.linspace(x_min, x_max, 250)
            prior = st.invgamma.pdf(x, 0.5*nu0, scale=0.5*lam0)
            y_label = '$\\sigma^2$'
            ax[index, 0].set_xlabel('乱数係数', fontproperties=jpfont)
            ax[index, 1].set_xlabel('パラメータの分布', fontproperties=jpfont)
        ax[index, 0].plot(mc_trace, 'k-', linewidth=0.1)
        ax[index, 0].set_xlim(1, n_draws*n_chains)
        ax[index, 0].set_ylabel(y_label, fontproperties=jpfont)
        posterior = st.gaussian_kde(mc_trace).evaluate(x)
        ax[index, 1].plot(x, posterior, 'k-', label='事後分布')
        ax[index, 1].plot(x, prior, 'k:', label='事前分布')
        ax[index, 1].set_xlim(x_min, x_max)
        ax[index, 1].set_ylim(0, 1.1*posterior.max())
        ax[index, 1].set_ylabel('確率密度', fontproperties=jpfont)
        ax[index, 1].legend(loc='best', frameon=False, prop=jpfont)
    plt.tight_layout()
    plt.savefig('pybayes_fig_mcmc_reg_ex3.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    main()