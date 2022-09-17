import pandas as pd

# LOfferType = ['reloco','panadera']
# LNewHighestDiscount = ['asdaskdasldndl', 'kl14jldsa']
# LDaysSinceTheOfferStarted = ['asdasd','61151']
# LDaysForTheOfferToEnd = ['asd1151','123414']

LOfferType = ['asdads','14141f1']
LNewHighestDiscount = ['asdasda1d1d12d','1411232341f1']
LDaysSinceTheOfferStarted = ['asda1d12 2112 s1ds','141412424231f1']
LDaysForTheOfferToEnd = ['asd1d 1sd 1ads','41241244']


# df1 = pd.DataFrame({
# 	"Offer type": [],
# 	"New highest discount?": [],
# 	"Days since the offer started": [],
# 	"Days for the offer to end": [],
# })

df1 = pd.read_excel('log.xlsx')

LOfferType = list(df1["Offer type"].dropna()) + LOfferType
print(LOfferType)
LNewHighestDiscount = list(df1["New highest discount?"].dropna()) + LNewHighestDiscount
print(LNewHighestDiscount)
LDaysSinceTheOfferStarted = list(df1["Days since the offer started"].dropna()) + LDaysSinceTheOfferStarted
print(LDaysSinceTheOfferStarted)
LDaysForTheOfferToEnd = list(df1["Days for the offer to end"].dropna()) + LDaysForTheOfferToEnd
print(LDaysForTheOfferToEnd)


df1["Offer type"] = pd.Series(LOfferType)
df1["New highest discount?"] = pd.Series(LNewHighestDiscount)
df1["Days since the offer started"] = pd.Series(LDaysSinceTheOfferStarted)
df1["Days for the offer to end"] = pd.Series(LDaysForTheOfferToEnd)


# df = pd.read_excel('log.xlsx')

# df = pd.concat([df, df1])
# df = df.append(df1)
# df = pd.DataFrame.merge(df1)


df1.to_excel('log.xlsx', index=False)
# df.to_excel('log.xlsx', index=False)