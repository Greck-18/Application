from pytest import fixture


@fixture(params=[1, 4, 16, 32, 64, 86, 100, 256, 344])
def num_page(request):
    return request.param


@fixture(params=[0, -100, None, 1000000000,-567865,'5475',False,-547547])
def num_page_neg(request):
    return request.param


@fixture(params=(i for i in range(20)))
def count_url(request):
    return request.param