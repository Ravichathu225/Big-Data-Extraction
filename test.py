from pydantic import BaseModel
from typing import List, Optional

class ExtractData(BaseModel):
    

data = open("","r").read()

prompt = """
prase following excale file and output give me json format
```
html{data}
```
""".format(data=data).strip('/n')
