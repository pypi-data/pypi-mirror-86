from ProgressText import ProgressText

for i in ProgressText(range(7)):
    pass

for i in ProgressText(range(50)):
    pass

for i in ProgressText(range(1000), every_percent=20):
    pass

for i in ProgressText([1,3,5,7,9,11]):
    pass
