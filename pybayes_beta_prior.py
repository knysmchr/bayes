from matplotlib.font_manager import FontProperties
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

jpfont = FontProperties(fname='/Users/knysmchr/Downloads/IPAexfont00301/ipaexg.ttf')

fig1 = plt.figure(num=1, facecolor='w')
q = np.linspace(0, 1, 250)
plt.plot(q, st.uniform.pdf(q), 'k-')
plt.plot(q, st.beta.pdf(q, 4, 6), 'k--')
plt.xlim(0, 1)
plt.ylim(0, 2.8)
plt.legend(['(A)一様分布($\\alpha$ = 1, $\\beta$ = 1)',
            '(B)ベータ分布($\\alpha$ = 4, $\\beta$ = 6)'],
            loc='best', frameon=False, prop=jpfont)
plt.xlabel('成功確率q', fontproperties=jpfont)
plt.ylabel('確率密度', fontproperties=jpfont)
plt.savefig('pybayes_fig_beta_prior.png', dpi=300)
plt.show()