## Setup

```
$ pip install navercafe
```

## Usage

```
from navercafe import NaverCafe

# 1. setup
cafe_name = 'wikibookstudy'
club_id = '30853297'
cafe = NaverCafe(cafe_name, club_id)

# 2. (optional) enter user id and pw
# This is semi-automatic (needs manual authentication)
cafe.enter_id_pw('your_id', 'your_pw')

# 3. get article board
board_id = 28
df1 = cafe.articleboard(board_id)
print(len(df1))
print(df1.head())

# 4. get comments
article_id = 139
df2 = cafe.comments(article_id)
print(len(df2))
print(df2.head())
```

