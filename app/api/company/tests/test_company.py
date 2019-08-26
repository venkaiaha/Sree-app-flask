# def test_list_companies(client):
#     rv = client.get('/api/v1/company')

#     if b'[]' not in rv.data:
#         raise AssertionError(rv.data)
#     if rv.status_code != 200:
#         raise AssertionError(rv.status_code)


# def test_create_company(client):
#     rv = client.post('/api/v1/company', json={'id': 1, 'name': '<give any company name/acn>'})

#     if b'Felix' not in rv.data:
#         raise AssertionError(rv.data)
#     if rv.status_code != 201:
#         raise AssertionError(rv.status_code)


# def test_get_company(client):
#     rv = client.get('/api/v1/company/<give any company _id>')

#     if b'Felix' not in rv.data:
#         raise AssertionError(rv.data)
#     if rv.status_code != 200:
#         raise AssertionError(rv.status_code)


# def test_update_company(client):
#     rv = client.put('/api/v1/company/<any _id>', json={'name': 'any name'})

#     if rv.status_code != 204:
#         raise AssertionError(rv.status_code)


# def test_delete_company(client):
#     rv = client.delete('/api/v1/company/<give _id>')

#     if rv.status_code != 204:
#         raise AssertionError(rv.status_code)


# def test_get_company_404(client):
#     rv = client.get('/api/v1/company/<give _id>')

#     if rv.status_code != 404:
#         raise AssertionError(rv.status_code)


# def test_update_cat_404(client):
#     rv = client.put('/api/cats/1', json={'name': 'Sylvester'})

#     if rv.status_code != 404:
#         raise AssertionError(rv.status_code)


# def test_delete_cat_404(client):
#     rv = client.delete('/api/cats/1')

#     if rv.status_code != 404:
#         raise AssertionError(rv.status_code)