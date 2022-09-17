import pandas as pd

df = pd.read_excel('logs/excel/log.xlsx')
LGamePricePLUS = df ["Game price"]
Refined_Prices = []
Amt = 1
for price in LGamePricePLUS:
    Amt += 1
    print(Amt)
    word = []
    for i in price:
        if i == "," or i == ".":
            word.append(".")
        elif i.isdigit():
            word.append(i)
        else:
            continue
    Refined_Prices.append("".join(word))
print(Refined_Prices)