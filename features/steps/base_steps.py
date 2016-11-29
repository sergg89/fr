from behave import *
import requests
import json
import nose
from features.steps.sql_unit import DB
import re
import jpath
from features import BASE_DIR
import yaml


class ScenarioIsFailed(Exception):
    pass

use_step_matcher("parse")

def get_part_of_json(data, json_p):
    path_list = json_p.split('.')
    result = data
    for elem in path_list:
        if elem == '':
            pass
        elif elem.startswith('[') and elem.endswith(']'):
            result = result[int(elem[1:-1])]

        else:
            try:
                result = jpath.get('.' + elem, result)
            except Exception as e:
                print('Key Error %s' % e)
                if type(result) == list:
                    print('object is a list!')
                raise KeyError
    return result


def log_error(str):
    print("")
    print("")
    print('-----------ERROR-----------')
    print(str)
    print("")
    print("")


def log_full(r):
    req = r.request
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """

    print("")
    print("")

    print('{}\n{}\n{}\n\n{}'.format(
        '-----------REQUEST-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

    print("")

    print('{}\n{}\n{}\n\n{}'.format(
        '-----------RESPONSE-----------',
        str(r.status_code) + ' ' + r.reason,
        '\n'.join('{}: {}'.format(k, v) for k, v in r.headers.items()),
        r.text,
    ))
    print("")

    print('Operation took ' + str(round(r.elapsed.total_seconds(), 3)) + 's')

    print("")
    print("")
    print("")
    print("")


@step('I make a {http_verb} request to "{url_path_segment}"')
def make_a_request(context, http_verb, url_path_segment):
    print(context.headers)
    print(context.body)
    if context.table:
        params = {}
        for row in context.table:
            param = row['PARAMETER_NAME']
            value = row['VALUE']
            if param.startswith("context"):
                param = eval(param)
            if value.startswith("context"):
                value = eval(value)
            params.update({param: value})
        param_part = '?'
        for key in params.keys():
            param_part = param_part + key + '=' + params.get(key) + '&'
        param_part = param_part[:-1]
    else:
        param_part = ''

    url = context.base_url + url_path_segment + param_part
    print(url)
    print(context.body)
    if http_verb == "GET":
        context.r = getattr(requests, http_verb.lower())(url, headers=context.headers)
    else:
        context.r = getattr(requests, http_verb.lower())(url, headers=context.headers, data=json.dumps(context.body))
    log_full(context.r)
    return context.r


@step("I add request body")
def add_body_to_request(context):
    try:
        context.body = json.loads(context.text)
        context.body = replace_if_need(context, context.body)
        print(context.body)
    except Exception as e:
        raise ScenarioIsFailed(log_error(' Exception! Cannot convert body to json %s \n' % e))


@step("the response status code should equal {expected_code}")
def validate_status_code(context, expected_code):
    nose.tools.assert_equal(context.r.status_code, int(expected_code))


@step("I run sql script")
def step_impl(context):
    if context.text == "" or None:
        raise ScenarioIsFailed(log_error(' Exception! Cannot read sql script! \n'))
    elif context.text.startswith("context"):
        variable = context.text[8:context.text.find('=') - 1]
        context.sql = context.text[context.text.find('=')+1:]
        db = DB()
        dict = db.select(context.sql)[0]
        for key in dict.keys():
            value = dict.get(key)
        context.__setattr__(variable, value)
    else:
        context.sql = context.text
        db = DB()
        db.update(context.sql)




@step('the response header "{header_name}" should equal "{expected_header_value}"')
def headers_parameter_validation(context, header_name, expected_header_value):
    nose.tools.assert_equal(context.r.headers[header_name], str(expected_header_value))


@step('I set "{header_name}" header to "{header_value}"')
def set_header(context, header_name, header_value):
    if header_value.startswith("context"):
        context.headers[header_name] = getattr(context, header_value[8:])
    else:
        context.headers[header_name] = header_value


@step('the response structure should equal "{expected_response_structure}"')
def response_structure_validation(context, expected_response_structure):
    data = context.r.json()
    try:
        response_valid = getattr(context.json_responses, expected_response_structure)

        assert response_valid.check(data)
    except NameError:
        print("")
        print("File with responses not found")
        print("")


@step('JSON at path "{json_path}" should equal {expected_json_value}')
def json_object_validation(context, json_path, expected_json_value):
    data = context.r.json()
    actual_json_value = get_part_of_json(data, json_path)
    if expected_json_value.startswith("context"):
        expected_json_value = getattr(context, expected_json_value[8:])
        nose.tools.assert_equal(actual_json_value, expected_json_value)
    else:
        try:
            converted_value = json.loads(expected_json_value)
            nose.tools.assert_equal(actual_json_value, converted_value)
        except AssertionError:
            nose.tools.assert_equal(str(actual_json_value), converted_value)



@step('JSON value at path "{json_path}" I save as "context.{var}"')
def step_impl(context, json_path, var):
    data = context.r.json()
    value = get_part_of_json(data, json_path)
    print(value)
    if var == 'token':
        value = value
    settings = yaml.load(open(BASE_DIR + '/features/config.yaml').read())
    settings.update({var: value})
    with open(BASE_DIR + '/features/config.yaml', 'w') as yaml_file:
        yaml.dump(settings, yaml_file, default_flow_style=False)
    context.__setattr__(var, value)
    print('context-token = %s '%context.token)


@step("I compare {val1} and {val2} it should be {is_equal}")
def step_impl(context, val1, val2, is_equal):
    if val1.startswith("context"):
        val1 = getattr(context, val1[8:])
    if val2.startswith("context"):
        val2 = getattr(context, val2[8:])
    if is_equal == 'equal':
        assert val1 == val2
    elif is_equal == 'not equal':
        assert val1 != val2


def replace_if_need(context, json):
    for key in json:
        if type(json[key]) == list:
            for element in json[key]:
                replace_if_need(context, element)
        elif type(json[key]) == dict:
            replace_if_need(context, json[key])
        elif type(json[key]) == str:
            if (json[key]).startswith("context"):
                json[key] = getattr(context, json[key][8:])
    return json



