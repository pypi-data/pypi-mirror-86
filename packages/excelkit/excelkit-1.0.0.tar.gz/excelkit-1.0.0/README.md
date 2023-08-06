# A ToolKit to Operate Excel File
---

## Installation
```
pip install excelkit
```

## Tools
### **`parse`** - parse excel file
```bash
excelkit parse --help
# or
excel-parse --help


excel-parse demo.xlsx

excel-parse demo.xlsx -o out.tsv

excel-parse demo.xlsx -O table

excel-parse demo.xlsx -O table --color red

excel-parse demo.xlsx -O json --indent 2

excel-parse demo.xlsx -O json --indent 2 --header

excel-parse demo.xlsx --pager 
```


### **`build`** - build excel file
```bash
excelkit build --help
# or
excel-build --help


excel-build demo/genelist demo/hsa00010.conf

excel-build demo/genelist demo/hsa00010.conf -o kegg.xlsx

excel-build demo/genelist demo/hsa00010.conf -o kegg.xlsx -s GENE,KEGG

excel-build demo/genelist demo/hsa00010.conf -h

excel-build demo/genelist demo/hsa00010.conf -hs

excel-build demo/genelist demo/hsa00010.conf -hs -bs

cat demo/genelist | excel-build
```

### **`concat`** - concat excel files
```bash
excelkit concat --help
# or
excel-concat --help

examples:

excel-concat input1.xlsx input2.xlsx -o out.xlsx

excel-concat input1.xlsx input2.xlsx -o out.xlsx --keep-fmt
```
