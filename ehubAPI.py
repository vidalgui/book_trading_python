import requests
import json
import pandas as pd


apiKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb21wYW55SWQiOiJMVnYxWmFuRGt6TXc2Ym03YjZvUE5kcjRnT0JLUjg5cSIsInRpbWVzdGFtcCI6MTY1OTU2MTQ4MDg3MCwiaWF0IjoxNjU5NTYxNDgwfQ.AKZE4UIvUZkp70EDI8CWRDBaOeftiZL3_wrJnuPWSUc'
companyCode = 1338


def idTokenPOST(email, password):
    url = "https://api-ehub.bbce.com.br/bus/v2/login"

    payload = json.dumps({
        "companyExternalCode": 1338,
        "email": email,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'apiKey': apiKey
    }

    json_data = json.loads(requests.request(
        "POST", url, headers=headers, data=payload).text)

    idToken = json_data["idToken"]

    return idToken


def forwardCurve(date, email, password):
    
    url = "https://api-ehub.bbce.com.br/bus/v1/curve/bbce-fwd?referenceDate="+date
    
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + idTokenPOST(email, password),
        'apiKey': apiKey
    }

    json_data = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)
    
    return json_data

def activeCompanies(email, password):
    url = "https://api-ehub.bbce.com.br/bus/v2/companies?tradeName=&status=Ativa"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + idTokenPOST(email, password),
        'apiKey': apiKey
    }

    json_data = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)

    return json_data


def todosNegocios(inicial, final, email, password):
    url = "https://api-ehub.bbce.com.br/bus/v1/all-deals/report?initialPeriod=" + \
        str(inicial) + "&finalPeriod=" + str(final)

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + idTokenPOST(email, password),
        'apiKey': apiKey
    }

    negocios = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)

    return negocios


def prodID(id, email, password):
    url = "https://api-ehub.bbce.com.br/bus/v2/tickers/" + str(id)

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + idTokenPOST(email, password),
        'apiKey': apiKey
    }

    produtos = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)

    return produtos["description"]


def produtos(email, password):
    url = "https://api-ehub.bbce.com.br/bus/v2/tickers?status="

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + idTokenPOST(email, password),
        'apiKey': apiKey
    }

    produtos = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)

    return produtos


def myOrders(inicial, final, email, password):
    url = "https://api-ehub.bbce.com.br/bus/v1/orders?initialPeriod=" + \
        str(inicial)+"&finalPeriod=" + str(final) + "&status=Aberta"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + idTokenPOST(email, password),
        'apiKey': apiKey
    }

    orders = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)

    return orders


def matches(inicial, final, email, password):
    url = "https://api-ehub.bbce.com.br/bus/v1/matches?initialPeriod=" + \
        str(inicial)+"&finalPeriod=" + str(final)

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + idTokenPOST(email, password),
        'apiKey': apiKey
    }

    matches = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)

    return matches


def registries(inicial, final, email, password):
    url = "https://api-ehub.bbce.com.br/bus/v1/registries?walletId=1020&endDate=" + \
        str(final)+"&startDate=" + str(inicial)

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + idTokenPOST(email, password),
        'apiKey': apiKey
    }

    matches = json.loads(requests.request(
        "GET", url, headers=headers, data=payload).text)

    return matches
