import pandas as pd
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt


class Model():
	def __init__(self, *args, **kwargs):
		super().__init(*args, **kwargs)
		self.optimizer = None

	def tsne(X_data, y_data, perplexities, n_iter=1000, img_name_prefix='t-sne'):
        """
		X_data = dataframe with only X data and column names(pandas.core.frame.DataFrame)
		y_data = only y values with no column names(pandas.core.series.Series)
		perplexities = as a list
		n_iter = int value (default=1000)
		Image is also saved with name starting as t-sne
        """
	    for index,perplexity in enumerate(perplexities):
	        # perform t-sne
	        print('\nperforming tsne with perplexity {} and with {} iterations at max'.format(perplexity, n_iter))
	        X_reduced = TSNE(verbose=2, perplexity=perplexity).fit_transform(X_data)
	        print('Done..')
	        
	        # prepare the data for seaborn         
	        print('Creating plot for this t-sne visualization..')
	        df = pd.DataFrame({'x':X_reduced[:,0], 'y':X_reduced[:,1] ,'label':y_data})
	        
	        # draw the plot in appropriate place in the grid
	        sns.lmplot(data=df, x='x', y='y', hue='label', fit_reg=False, size=8,\
	                   palette="Set1",markers=True)
	        plt.title("perplexity : {} and max_iter : {}".format(perplexity, n_iter))
	        img_name = img_name_prefix + '_perp_{}_iter_{}.png'.format(perplexity, n_iter)
	        print('saving this plot as image in present working directory...')
	        plt.savefig(img_name)
	        plt.show()
	        print('Done')