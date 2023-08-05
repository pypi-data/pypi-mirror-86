# BBCHeadlines
[![](https://img.shields.io/pypi/v/bbc-feeds)](https://pypi.org/project/bbc-feeds) \
A python package to get sports, weather, and news from BBC.

### Installation

    pip3 install bbc-feeds

### Usage
Import the library:

    import bbc_feeds

### Functions
**News**:
- `news().all()`
- `news().world()`
- `news().uk()`
- `news().us()`
- `news().entertainment()`
- `news().buisness()`
- `news().tech()`
- `news().science()`
- `news().tech()`

**Sports**
- `sports().all()`
- `sports().cricket()`
- `sports().soccer()`
- `sports().tennis()`
- `sports().athletics()`
- `sports().golf()`
- `sports().boxing()`
- `sports().swimming()`
- `sports().cycling()`
- `sports().formula1()`

**Weather**
- `weather().forecast(city_id)` (To get your city ID, search for it at [BBC Weather's Website](https://www.bbc.com/weather)).

All functions have an optional parameter `limit`, where you can limit the number of entries.