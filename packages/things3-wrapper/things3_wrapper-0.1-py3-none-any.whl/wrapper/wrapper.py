import webbrowser
from urllib import parse

# Reference : https://culturedcode.com/things/support/articles/2803573/

BASE_URL = 'things://'
AUTH_TOKEN = 'ueruO9naTWSK1vG4ndLb-A'
PROJECT_ID = 'BFrGXFTACMYe9FuSxLMc9G'

def add(title=None, titles=None, completed=None, canceled=None, show_quick_entry=None, reveal=None, notes=None, checklist_items=None, when=None, deadline=None, tags=None, _list=None, _list_id=None, heading=None, creation_date=None, completion_date=None):
    query = dict()

    if title != None:
        quary['title'] = title
    if titles != None:
        quary['titles'] = titles
    if completed == True:
        quary['completed'] = 'true'
    if canceled == True:
        quary['canceled'] = 'true'
    if show_quick_entry != None:
        quary['show-quick-entry'] = show_quick_entry
    if reveal != None:
        quary['reveal'] = reveal
    if notes != None:
        quary['notes'] = notes
    if checklist_items != None:
        quary['checklist-items'] = checklist_items
    if when != None:
        quary['when'] = when
    if deadline != None:
        quary['deadline'] = deadline
    if tags != None:
        quary['tags'] = tags
    if _list != None:
        quary['list'] = _list
    if _list_id != None:
        quary['list-id'] = _list_id
    if heading != None:
        quary['heading'] = heading
    if creation_date != None:
        quary['creation_date'] = creation_date
    if completion_date != None:
        quary['completion_date'] = completion_date

    query_encoded = parse.urlencode(query, encoding='UTF-8', doseq=True, quote_via=parse.quote)
    url = BASE_URL + '/add?' + query_encoded
    return url

def add_project(title=None, completed=None, canceled=None, reveal=None, notes=None, when=None, deadline=None, tags=None, area=None, area_id=None, to_dos=None, creation_date=None, completion_date=None):
    query = dict()

    if title != None:
        query['title'] = title
    if completed == True:
        query['completed'] = 'true'
    if canceled == True:
        query['canceled'] = 'true'
    if reveal == True:
        query['reveal'] = 'true'
    if notes != None:
        query['notes'] = notes
    if when != None:
        query['when'] = when
    if deadline != None:
        query['deadline'] = deadline
    if tags != None:
        query['tags'] = tags
    if area != None:
        query['area'] = area
    if area_id != None:
        query['area-id'] = area_id
    if to_dos != None:
        query['to-dos'] = to_dos
    if creation_date != None:
        query['creation-date'] = creation_date
    if completion_date != None:
        query['completion-date'] = completion_date

    query_encoded = parse.urlencode(query, encoding='UTF-8', doseq=True, quote_via=parse.quote)
    url = BASE_URL + '/add-project?' + query_encoded
    return url

def update(auth_token=None, _id=None, title=None, completed=None, canceled=None, reveal=None, duplicate=None, notes=None, prepend_notes=None, append_notes=None, when=None, deadline=None, tags=None, add_tags=None, checklist_items=None, prepend_checklist_items=None, append_checklist_items=None, _list=None, _list_id=None, heading=None, creation_date=None, completion_date=None):
    query = dict()

    query_encoded = parse.urlencode(query, encoding='UTF-8', doseq=True, quote_via=parse.quote)
    url = BASE_URL + '/update?' + query_encoded
    return url

def update_project(auth_token=None, _id=None, title=None, completed=None, canceled=None, reveal=None, duplicate=None, notes=None, prepend_notes=None, append_notes=None, when=None, deadline=None, tags=None, add_tags=None, area=None, area_id=None, creation_date=None, completion_date=None):
    query = dict()

    if auth_token != None:
        query['auth_token'] = auth_token
    if _id != None:
        query['_id'] = _id
    if title != None:
        query['title'] = title
    if completed != None:
        query['completed'] = completed
    if canceled != None:
        query['canceled'] = canceled
    if reveal != None:
        query['reveal'] = reveal
    if duplicate != None:
        query['duplicate'] = duplicate
    if notes != None:
        query['notes'] = notes
    if prepend_notes != None:
        query['prepend_notes'] = prepend_notes
    if append_notes != None:
        query['append_notes'] = append_notes
    if when != None:
        query['when'] = when
    if deadline != None:
        query['deadline'] = deadline
    if tags != None:
        query['tags'] = tags
    if add_tags != None:
        query['add_tags'] = add_tags
    if area != None:
        query['area'] = area
    if area_id != None:
        query['area_id'] = area_id
    if creation_date != None:
        query['creation_date'] = creation_date
    if completion_date != None:
        query['completion_date'] = completion_date

    query_encoded = parse.urlencode(query=None, encoding='UTF-8', doseq=True, quote_via=parse.quote)
    url = BASE_URL + '/update-project?' + query_encoded
    return url
#
def show(_id=None, _query=None, filter=None):
    query = dict()

    if _id != None:
        query['_id'] = _id
    if _query != None:
        query['_query'] = _query
    if filter != None:
        query['filter'] = filter

    query_encoded = parse.urlencode(query, encoding='UTF-8', doseq=True, quote_via=parse.quote)
    url = BASE_URL + '/show?' + query_encoded
    return url
#
def search(_query=None):
    query = dict()

    if _query != None:
        query['_query'] = _query

    query_encoded = parse.urlencode(query, encoding='UTF-8', doseq=True, quote_via=parse.quote)
    url = BASE_URL + '/search?' + query_encoded
    return url

def json(data=None, auth_token=None, reveal=None):
    query = dict()

    if data != None:
        query['data'] = title
    if auth_token != None:
        query['auth-token'] = auth_token
    if reveal == True:
        query['reveal'] = 'true'

    query_encoded = parse.urlencode(query, encoding='UTF-8', doseq=True, quote_via=parse.quote)
    url = BASE_URL + '/json?' + query_encoded
    return url

if __name__ == '__main__':
    # auth_token = AUTH_TOKEN
    # project_id = PROJECT_ID
    # url = json(data=None, auth_token=AUTH_TOKEN, reveal=None)
    # webbrowser.open(url)
