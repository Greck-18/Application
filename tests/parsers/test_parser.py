import os
import pprint as pp
from pytest import mark, fixture,raises
from prs.parser.news import ParserLinks,ParserNews

from .data import num_page,num_page_neg


# @fixture(autouse=True, scope="function")
# def clean_files():
#     os.mkdir(".files")
#     yield
#     os.system("rm -rf .files")


# @mark.parser
# @mark.links
# def test_load_lings(num_page):
#     parser = ParserLinks(num_page)
#     parser.get_data()
#     parser.process_data()
#     assert len(parser.links)


# @mark.parser
# @mark.links
# #@mark.single
# def test_check_links(num_page):
#     parser = ParserLinks(num_page)
#     parser.get_data()
#     parser.process_data()
#     assert isinstance(parser.links[0], str)


# # @mark.single
# # def test_create_file(num_page):
# #     with open(".files/"+str(num_page)+".txt", "w") as file:
# #         file.write(str(num_page))


# @mark.parser
# @mark.links
# #@mark.single
# def test_num_page_neg(num_page_neg):
#     parser = ParserLinks(num_page_neg)
#     parser.get_data()
#     with raises(ValueError):
#         parser.process_data()


# @mark.parser
# @mark.links
# @mark.single
# def test_num_page_message_neg(num_page_neg):
#     parser = ParserLinks(num_page_neg)
#     parser.get_data()
#     try:
#         parser.process_data()
#     except ValueError as error:
#         assert str(num_page_neg) in error.args[0]



@mark.parser
@mark.links
@mark.single
def test_load_news(num_page):
    parser = ParserLinks(num_page)
    parser.get_data()
    parser.process_data()
    news_parser=ParserNews(parser.links[0])
    news_parser.get_data()
    news_parser.process_data()
    pp.pprint(news_parser.news)
