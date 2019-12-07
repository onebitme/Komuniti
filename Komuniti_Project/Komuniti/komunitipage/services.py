from .models import *
from qwikidata.sparql import (get_subclasses_of_item, return_sparql_query_results)
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api


class WikidataService:

    def query(query):
        # send any sparql query to the wikidata query service and get full result back
        # here we use an example that counts the number of humans
        sparql_query = """
        SELECT distinct ?itemDescription WHERE{  
          ?item rdfs:label "%s"@en.  
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }  
        }
        """ % query
        return return_sparql_query_results(sparql_query)

# class UserService:
#
#     def login(id):
#         return User.objects.filter(id=id).values()
#
#     def signup(data):
#         return User.objects.filter(id=data.id).values()
#


class CommunityService:

     def getCommunity(url):
         return Community.objects.filter(url=url).values(
             'id',
             'title',
             'description'
         )
#
#     def getCommunityMembers(url):
#         return Community.objects.filter(url=url).values(
#             'members__id',
#             'members__username',
#             'members__date_registered'
#         )
#
#     def getCommunityDataTypes(url):
#         return Community.objects.filter(url=url).values(
#             'datatype__id',
#             'datatype__title',
#             'datatype__body'
#         )
#
#     def getCommunityDataFields(url):
#         # todo is it possible to use Community here or should i use DataField model instead
#         return Community.objects.filter(url=url).values(
#             'datafield__id',
#             'datafield__type__name',
#             'datafield__is_required',
#             'datafield__wikidata_item'
#         )
#         # data = Community.objects.filter(url=url).values(
#         #    'id'
#         # )
#         # return DataField.objects.filter(id=data[0]).values()