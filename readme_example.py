from hdroller import Die

# A standard d10.
die = Die.d10

# A d10, exploding on highest face at most twice, similar to Legend of the Five Rings.
die = Die.d10.explode(2)

# Roll ten L5R dice and keep the five highest.
die = Die.d10.explode(2).keep_highest(10, 5)

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(die.outcomes(), die.pmf())
plt.show()