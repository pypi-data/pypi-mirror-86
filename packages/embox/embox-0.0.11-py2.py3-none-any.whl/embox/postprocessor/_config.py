import matplotlib.pyplot as plt
from matplotlib import cycler
from matplotlib import ticker

formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-1, 1))

rcParams = plt.rcParams

rcParams["axes.prop_cycle"] = cycler("color",
                                     ["#3742fa", "#2ed573", "#ff4757", "#2f3542", "#eccc68", "#ffa502", "#8e44ad",
                                      "#4834d4", "#70a1ff", "#CAD3C8"])
rcParams["figure.figsize"] = (3.5, 2.625)
rcParams["figure.dpi"] = 600
rcParams["font.size"] = 8
rcParams["xtick.direction"] = "in"
rcParams["xtick.major.size"] = 3
rcParams["xtick.major.width"] = 0.5
rcParams["xtick.minor.size"] = 1.5
rcParams["xtick.minor.width"] = 0.5
rcParams["xtick.minor.visible"] = True
rcParams["xtick.top"] = True

rcParams["axes.grid"] = True
rcParams["grid.linestyle"] = ":"
rcParams["grid.color"] = "k"
rcParams["grid.alpha"] = 0.5
rcParams["grid.linewidth"] = 0.5

rcParams["legend.frameon"] = True
rcParams["legend.framealpha"] = 1.0
rcParams["legend.fancybox"] = True
rcParams["legend.numpoints"] = 1

rcParams["axes.linewidth"] = 0.5
rcParams["grid.linewidth"] = 0.5
rcParams["lines.linewidth"] = 1.0
rcParams["savefig.bbox"] = "tight"
rcParams["savefig.pad_inches"] = 0.05

rcParams["font.serif"] = "Times New Roman"
rcParams["font.family"] = "serif"
rcParams["mathtext.fontset"] = "dejavuserif"

rcParams["text.usetex"] = True
rcParams["text.latex.preamble"] = r"\usepackage{amsmath}"
