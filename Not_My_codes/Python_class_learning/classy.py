#!/home/oceanw/anaconda3/bin/python3
class empolyee:
	def __init__(self, first, last, pay):
		self.first = first
		self.last = last
		self.pay = pay
		self.email = first+ '.' + last + "@company.com"
		if self.pay<55000: self.underpay = self.first+" is underpaid!"

emp1 = empolyee("Corey",'Schafer', 50000)
emp2 = empolyee("Test", 'User', 60000)
emp1.new = "random string"

print(emp1.email)
print(emp2.email)
print(emp1.underpay)
#print(emp2.underpay) # this is not allowed as the "underpay" attribute does not exist for emp2

#print(emp2.self) self is not an attribute
print(emp1.new)

