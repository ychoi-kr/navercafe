## Setup

```
$ pip install navercafe
```

## Usage

```
from navercafe import NaverCafe

cafe = NaverCafe('wikibookstudy', '30853297')
cafe.enter_id_pw('your_id', 'your_pw')  # Need manual authentication

df = cafe.articleboard(34)
print(len(df))
print(df.head())
```
