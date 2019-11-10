from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api
import sqlparse

Q_DOUGLAS_ADAMS = "Q42"
q42_dict = get_entity_dict_from_api(Q_DOUGLAS_ADAMS)
q42 = WikidataItem(q42_dict)

print(q42)


sqlparse.split('select * from foo; select * from bar;')
[u'select * from foo; ', u'select * from bar;']