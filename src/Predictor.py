'''
Created on 2019 M01 21

@author: kgap1
'''

from stocker import Stocker
 
aurora = Stocker('ACB.TO')
aurora.plot_stock()
# predict days into the future
model, model_data = aurora.create_prophet_model(days=90)
# import pystan
# model_code = 'parameters {real y;} model {y ~ normal(0,1);}'
# model = pystan.StanModel(model_code=model_code)  # this will take a minute
# y = model.sampling(n_jobs=1).extract()['y']
# y.mean()  # should be close to 0