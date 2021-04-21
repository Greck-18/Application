from pytest import fixture


@fixture(params=[1, 4, 16, 30000])
def num_page(request):
    return request.param


@fixture(params=[0, -100, None, 1000000000])
def num_page_neg(request):
    return request.param
