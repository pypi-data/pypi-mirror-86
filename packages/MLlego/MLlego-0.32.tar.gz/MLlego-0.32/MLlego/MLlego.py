import itertools
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.manifold import TSNE
from sklearn import metrics


class Model():
	def __init__(self, *args, **kwargs):
		pass

	def tsne(self, X_data, y_data, perplexities, n_iter=1000, img_name_prefix='t-sne'):
		"""
		X_data = dataframe with only X data and column names(pandas.core.frame.DataFrame)
		y_data = only y values with no column names(pandas.core.series.Series)
		perplexities = as a list
		n_iter = int value (default=1000)
		Image is also saved with name starting as t-sne
        """
		for index,perplexity in enumerate(perplexities):
			print('\nperforming tsne with perplexity {} and with {} iterations at max'.format(perplexity, n_iter))
			X_reduced = TSNE(verbose=2, perplexity=perplexity).fit_transform(X_data)
			print('Done..')
			# prepare the data for seaborn
			print('Creating plot for this t-sne visualization..')
			df = pd.DataFrame({'x':X_reduced[:,0], 'y':X_reduced[:,1] ,'label':y_data})

			# draw the plot in appropriate place in the grid
			sns.lmplot(data=df, x='x', y='y', hue='label', fit_reg=False, size=8,palette="Set1",markers=True)
			plt.title("perplexity : {} and max_iter : {}".format(perplexity, n_iter))
			img_name = img_name_prefix + '_perp_{}_iter_{}.png'.format(perplexity, n_iter)
			print('saving this plot as image in present working directory...')
			plt.savefig(img_name)
			plt.show()
			print('Done')

	def plot_confusion_matrix(self, y_test, y_pred, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
	    """ Input - (y_test, y_pred, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues)
	    Output - Confusion Matrix"""
	    cm = metrics.confusion_matrix(y_test, y_pred)
	    print('\n| Confusion Matrix |')
	    print('{}'.format(cm))
	    plt.figure(figsize=(8,8))
	    plt.grid(b=False)
	    if normalize:
	        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

	    plt.imshow(cm, interpolation='nearest', cmap=cmap)
	    plt.title(title)
	    plt.colorbar()
	    tick_marks = np.arange(len(classes))
	    plt.xticks(tick_marks, classes, rotation=90)
	    plt.yticks(tick_marks, classes)

	    fmt = '.2f' if normalize else 'd'
	    thresh = cm.max() / 2.
	    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
	        plt.text(j, i, format(cm[i, j], fmt),
	                 horizontalalignment="center",
	                 color="white" if cm[i, j] > thresh else "black")

	    plt.tight_layout()
	    plt.ylabel('True label')
	    plt.xlabel('Predicted label')
	    plt.show()
	    return cm
	
	def perform_model(self, model, X_train, y_train, X_test, y_test, class_labels, cm_normalize=True, print_cm=True, cm_cmap=plt.cm.Greens):
	    """This method is to run classical model like Logistic Regression, Linear SVC, Kernel SVM, Decision Trees, Random Forest Classifier, Gradient Boosted Decision Trees
	    Input - (model, X_train, y_train, X_test, y_test, class_labels, cm_normalize=True, print_cm=True, cm_cmap=plt.cm.Greens)
	    Output - A dict that has Train_time, Train_pred, Train_accuracy, Test_time, Test_accuracy, Confusion_matrix, Classification_report
	    Example of input - 
	            Logistic Regression:
	                parameters = {'C':[0.01, 0.1, 1, 10, 20, 30], 'penalty':['l2','l1']}
	                log_reg = linear_model.LogisticRegression()
	                log_reg_grid = GridSearchCV(log_reg, param_grid=parameters, cv=3, verbose=1, n_jobs=-1)
	                log_reg_grid_results =  perform_model(log_reg_grid, X_train, y_train, X_test, y_test, class_labels=labels)
	            Linear SVC:
	                parameters = {'C':[0.125, 0.5, 1, 2, 8, 16]}
	                lr_svc = LinearSVC(tol=0.00005)
	            Kernel SVM:
	                parameters = {'C':[2,8,16],'gamma': [ 0.0078125, 0.125, 2]}
	                rbf_svm = SVC(kernel='rbf')
	                rbf_svm_grid = GridSearchCV(rbf_svm,param_grid=parameters, n_jobs=-1)
	            Decision Trees:
	                parameters = {'max_depth':np.arange(3,10,2)}
	                dt = DecisionTreeClassifier()
	                dt_grid = GridSearchCV(dt,param_grid=parameters, n_jobs=-1)
	            Random Forest Classifier:
	                params = {'n_estimators': np.arange(10,201,20), 'max_depth':np.arange(3,15,2)}
	                rfc = RandomForestClassifier()
	                rfc_grid = GridSearchCV(rfc, param_grid=params, n_jobs=-1)
	            Gradient Boosted Decision Trees:
	                param_grid = {'max_depth': np.arange(5,8,1), 'n_estimators':np.arange(130,170,10)}
	                gbdt = GradientBoostingClassifier()
	                gbdt_grid = GridSearchCV(gbdt, param_grid=param_grid, n_jobs=-1)
	                """
	    # to store results at various phases
	    results = dict()
	    
	    # time at which model starts training 
	    train_start_time = datetime.now()
	    model.fit(X_train, y_train)
	    train_end_time = datetime.now()
	    results['Train_time'] =  train_end_time - train_start_time
	    
	    # predict train data
	    test_start_time = datetime.now()
	    y_pred = model.predict(X_train)
	    test_end_time = datetime.now()
	    results['Train_pred'] = y_pred
	   
	    # calculate overall accuracty of the model
	    accuracy = metrics.accuracy_score(y_true=y_train, y_pred=y_pred)
	    # store accuracy in results
	    results['Train_accuracy'] = accuracy
	    print('Train Accuracy : {}'.format(accuracy))
	    
	    
	    # predict test data
	    test_start_time = datetime.now()
	    y_pred = model.predict(X_test)
	    test_end_time = datetime.now()
	    results['Test_time'] = test_end_time - test_start_time
	    results['predicted'] = y_pred
	   
	    # calculate overall accuracty of the model
	    accuracy = metrics.accuracy_score(y_true=y_test, y_pred=y_pred)
	    # store accuracy in results
	    results['Test_accuracy'] = accuracy
	    print('Test Accuracy : {}'.format(accuracy))

	    # plot confusin matrix
	    results['Confusion_matrix'] = metrics.confusion_matrix(y_test, y_pred)
	    self.plot_confusion_matrix(y_test, y_pred, classes=class_labels, normalize=True, title='Normalized confusion matrix', cmap = plt.cm.Greens)
	        
	    # get classification report
	    print('\t\t\t\t\t\t| Classifiction Report |')
	    classification_report = metrics.classification_report(y_test, y_pred)
	    # store report in results
	    results['Classification_report'] = classification_report
	    print('',classification_report)
	    
	    # add the trained  model to the results
	    results['model'] = model
	    
	    return results