import camelot
import numpy as np

fileLocClaim = "C:/workspace/pdf_extraction/claim.pdf"
tables = camelot.read_pdf(fileLocClaim, flavor='stream', pages='all')
result = []
data_set = []
for table in tables:
    data_list = table.df.to_numpy()
    for data in data_list:
        data_set.append(data)
print(data_set)
#return data_set