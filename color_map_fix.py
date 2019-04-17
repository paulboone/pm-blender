import numpy as np

# subtle blues
colors = np.array([(255,255,217),(237,248,177),(199,233,180),(127,205,187),(65,182,196),
            (29,145,192),(34,94,168),(37,52,148),(8,29,88)])

# heat map
colors = np.array([(255,247,236),
(254,232,200),
(253,212,158),
(253,187,132),
(252,141,89),
(239,101,72),
(215,48,31),
(179,0,0),
(127,0,0)])


updated_colors = np.ones((len(colors), 3))
# updated_colors = np.ones((len(colors), 4))
updated_colors[:,0:3] = colors / 255

print(updated_colors)
