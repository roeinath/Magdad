import json
from io import BytesIO

from django.http import FileResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import web_framework.server_side.infastructure.ids_manager as ids_manager
from APIs.ExternalAPIs.FilesAPIs import files_api
from APIs.ExternalAPIs.FilesAPIs.talpix_file import TalpiXFile
from APIs.TalpiotAPIs import User
from web_features.features import categories as feature_categories
from web_features.quick_access_pages import quick_access_page_list
from web_framework.server_side.infastructure.auth.talpiot_jwt_authentication import TalpiotJWTAuthentication

YNET_RSS_SOURCE = 'https://www.ynet.co.il/Integration/StoryRss1854.xml'

actions_lsts = {}


############# Utilities #############
@csrf_exempt
def good_json_response(data):
    response = JsonResponse(data)
    response['Access-Control-Allow-Origin'] = '*'

    return response


def init_session_actions(request):
    if request.session.session_key not in actions_lsts:
        actions_lsts[request.session.session_key] = []


############# Handlers ###############

# All ids ever rendered.
all_ids = []


def recursive_add_ids_of_children(component):
    if component['id'] not in all_ids:
        all_ids.append(component['id'])

    if 'component' in component:
        recursive_add_ids_of_children(component['component'])


def get_actions(request):
    init_session_actions(request)

    actions = []

    while len(actions_lsts[request.session.session_key]) > 0:
        action = actions_lsts[request.session.session_key].pop(0)
        if action.get('error') is not None:
            print(action)
            return HttpResponseBadRequest(action['error'] + '<br>recommendation:' + str(action.get('suggestion')))
        else:
            if action['action'] == 'add':
                actions.append(action)
                all_ids.append(action['value']['id'])
            else:
                if action['value']['id'] not in all_ids:
                    actions_lsts[request.session.session_key].append(action)
                else:
                    actions.append(action)
                    if action['action'] == 'add_component':
                        recursive_add_ids_of_children(action['value']['child']['component'])

    actions_lsts[request.session.session_key].clear()

    return good_json_response({'actions': actions})


@api_view(['GET'])
@authentication_classes([TalpiotJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_page(request):
    user = request.user

    if not isinstance(user, User):
        return Response({'error': 'יש להתחבר עם חשבון תלפיות (אם אתה מחובר, נסה להתנתק ולהתחבר מחדש)'}, status=403)

    init_session_actions(request)

    class_name = request.GET.get("name")
    page = None
    for category in feature_categories:

        if class_name not in category.pages:
            continue

        if not category.is_authorized(user):
            return Response({'error': 'אין לך הרשאות לעמוד הזה'}, status=403)

        print("Currently connected user: ", user)

        if user is None:
            return Response({'error': 'יש להתחבר עם חשבון תלפיות (אם אתה מחובר, נסה להתחבר מחדש)'}, status=403)

        if not category.pages[class_name].is_authorized(user):
            return Response({'error': 'אין לך הרשאות לעמוד הזה'}, status=403)

        print(request.GET['params'])
        params = request.GET['params'].split(',')
        page = category.pages[class_name](params)

    if page is None:
        return Response({'error': f'Page {class_name} not found'}, status=404)

    print("User", user.name[::-1], "opened", page.get_title()[::-1])

    page.session_id = request.session.session_key
    root = page.get_initial_ui(request.user)

    actions_lsts[request.session.session_key].append({
        'action': 'add',
        'value': root.render(),
    })

    return get_actions(request)


@api_view(['POST'])
@authentication_classes([TalpiotJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request):
    init_session_actions(request)

    if request.body:
        payload = json.loads(request.body)
        if payload.get('data'):
            action_id = payload.get('method_id')
            if action_id in ids_manager.action_ids:
                ids_manager.action_ids[action_id](payload['data'])
            else:
                actions_lsts[request.session.session_key].append(
                    {'error': "bad method id", "suggestion": 'try reloading the page (get_data)'})
        else:
            actions_lsts[request.session.session_key].append({'error': 'no "data" key in POST request'})
    else:
        actions_lsts[request.session.session_key].append({'error': 'empty POST request'})
    return get_actions(request)


@api_view(['POST'])
@authentication_classes([TalpiotJWTAuthentication])
@permission_classes([IsAuthenticated])
def run_func(request):
    init_session_actions(request)

    payload = json.loads(request.body)
    action_id = payload.get('method_id')
    print('PARAM PARAM', payload)
    if action_id:
        del payload['method_id']
    if action_id in ids_manager.action_ids:
        ids_manager.action_ids[action_id](payload)  # run user func
    else:
        print("Request for bad method id: ", action_id)
        actions_lsts[request.session.session_key].append(
            {'error': "bad method id", "suggestion": 'try reloading the page (run_func)'})
    return get_actions(request)


@api_view(['GET'])
@authentication_classes([TalpiotJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_pages(request):
    init_session_actions(request)

    user = request.user

    categories = []

    for cat in feature_categories:
        pages = []

        for page_url, page in cat.pages.items():
            if not page.is_authorized(user):
                continue

            pages.append({
                'name': page.get_title(),
                'url': '/react/page/' + page_url
            })

        if len(pages) == 0:
            continue

        categories.append({
            'name': cat.get_title(),
            'pages': pages
        })

    return good_json_response({
        'categories': categories
    })


@api_view(['GET'])
@authentication_classes([TalpiotJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_ynet_news(request):
    # req = requests.get(YNET_RSS_SOURCE)
    #
    # soup = BeautifulSoup(req.text)
    # articles = soup.findAll('item')
    #
    # headlines = []
    #
    # for article in articles:
    #     title = article.find('title')
    #     pubdate = article.find('pubdate')
    #     headlines.append({
    #         'title': title.contents[0],
    #         'pubDate': dt.datetime.strptime(pubdate.contents[0], "%a, %d %b %Y %H:%M:%S %z").strftime('%H:%M')
    #     })
    return (good_json_response({'news': []}))


@api_view(['GET'])
@authentication_classes([TalpiotJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_file(request):
    path = request.GET['filepath']
    file = TalpiXFile.objects(path_on_server=path)[0]
    stream = BytesIO(files_api.download_file_as_stream(file).content_as_bytes())
    response = FileResponse(stream)
    response.filename = file.filename
    response['Content-Disposition'] = 'attachment'
    response['Access-Control-Allow-Origin'] = '*'
    return response


@api_view(['GET'])
@authentication_classes([TalpiotJWTAuthentication])
@permission_classes([IsAuthenticated])
def quick_access_pages(request):
    init_session_actions(request)
    user = request.user

    pages = []
    pages_for_quick_access = quick_access_page_list()

    for category in feature_categories:
        for page_url, page in category.pages.items():
            if page in pages_for_quick_access and page.is_authorized(user):
                pages.append({
                    'name': page.get_title(),
                    'url': '/react/page/' + page_url
                })

    return good_json_response({
        'pages': pages
    })
