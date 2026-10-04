import rodiumai
print(getattr(rodiumai, "__file__", "n/a"))
print([a for a in dir(rodiumai) if not a.startswith("_")][:80])