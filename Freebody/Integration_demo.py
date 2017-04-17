# coding: utf-8
#we need to anonymize the function by using lambda as below:
cosfunc = lambda x : np.cos(x**2)
int.quad(cosfunc, 0, 3)
get_ipython().magic('save Integration_demo')
get_ipython().magic('save Integration_demo 70-74')
