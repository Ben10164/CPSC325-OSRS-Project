import DateTimeHelper


DateTimeHelper.NameIDHelper.UpdateJson()

name = "Twisted bow"

test = DateTimeHelper.getDT(name , "6h")
print(test)

import matplotlib.pyplot as plt

# Creating a plot
res = test.plot(title=name).get_figure()

# Save figure
path = "Graphs/" + name + ".png"
res.savefig(path)