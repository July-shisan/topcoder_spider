# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MatchItem(Item):
    # define the fields for your item here like:
    # name = Field()
    match_id = Field()
    name = Field()
    href = Field()
    date = Field()

class MatchDetailItem(Item):
    match_id = Field()
    division = Field()
    place = Field()
    score = Field()
    username = Field()

class ProblemItem(Item):
    problem_id = Field()
    href = Field()
    name = Field()
    match_id = Field()
    date = Field()
    writer = Field()
    categary = Field()
    level_div1 = Field()
    rate_div1 = Field()
    level_div2 = Field()
    rate_div2 = Field()
    content = Field()
    
class SolutionItem(Item):
    solution_id = Field()
    problem_id = Field()
    match_id = Field()
    language = Field()
    status = Field()
    
