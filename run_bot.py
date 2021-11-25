import requests
import json
import sys
import os
import pandas_queries
import xlsx_reader
import update_xlsx
import answers
from time import sleep
try:
    from flask import Flask
    from flask import request
except ImportError as e:
    print(e)
    print("Looks like 'flask' library is missing.\n"
          "Type 'pip3 install flask' command to install the missing library.")
    sys.exit()
bearer = str(os.getenv("ACCESS_TOKEN"))  # BOT'S ACCESS TOKEN
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer
}

# SETUP
dists = ['Ingram', 'Comstor', 'Scansource']
dists_FT = ['Ingram Fast Track', 'Comstor Fast Track', 'Scansource Fast Track']

col_list = ['Cisco Standard Part Number', 'Distributor Part Number', 'Product Item Description', 'Quantity on Hand', 'Quantity On Order',
            'Distributor Reported In-transit Quantity', 'Committed Quantity', 'Available']
col_list_FT = ["FT Part Number", "Avaiable"]
data = xlsx_reader.df_dict(
    sheet_names=dists, col_list=col_list, file_path="./data/input_file.xlsx")

data_FT = xlsx_reader.df_dict(
    dists_FT, col_list_FT, file_path="./data/input_file.xlsx", fast_track=True)
last_update = update_xlsx.get_json("./data/last_update.json")
contacts = update_xlsx.get_json("./data/contacts.json")
admins = update_xlsx.get_json("./data/admins.json")

def send_get(url, payload=None, js=True):

    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request = request.json()
    return request

def send_post(url, data):

    request = requests.post(url, json.dumps(data), headers=headers).json()
    return request
def update_db(backoff,webhook):
        sleep(backoff)
        result = requests.request("GET", webhook['data']['files'][0], headers={
                                  "Authorization": "Bearer " + bearer})
        while (str(result.status_code) != '200') and backoff < 660:
            sleep(backoff)
            result = requests.request("GET", webhook['data']['files'][0], headers={
                                      "Authorization": "Bearer " + bearer})
            backoff = backoff*4
        if (backoff < 660) and (result.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
            xlsx = result.content
            start_title = result.headers['Content-Disposition'].find(
                    '_') - 2
            title = result.headers['Content-Disposition'][start_title:(
                    start_title+12)]
            status = update_xlsx.get_input_file(xlsx,title)
            if status =="Success, Input File Updated":
                global data,data_FT,last_update 
                data = xlsx_reader.df_dict(
                                    sheet_names=dists, col_list=col_list, file_path="./data/input_file.xlsx")

                data_FT = xlsx_reader.df_dict(
                                    dists_FT, col_list_FT, file_path="./data/input_file.xlsx", fast_track=True)
                last_update = update_xlsx.get_json("./data/last_update.json")
                return "O seu upload foi bem sucedido!<br/>"
            else:
                return "Não consegui finalizar seu upload... Peço que por favor contate um `Admin`<br/>"
        elif backoff >= 660 and (result.status_code != 200):
                return "Desculpe, o seu upload está demorando muito... tivemos que tira-lo da fila.<br/>"
        else:
                return "Puxa, algo deu errado... Verifique se o tipo de arquivo é '.xlsx' ou '.json', ou contate um admin.<br/>"          
def buscar(message):
    if len(message) > 0:
        main_dict = dict()
        for dist in data.keys():
            result = pandas_queries.product_query(
                    data[dist], message, 'Cisco Standard Part Number')
            main_dict[dist] = result[message]
            product_exists = not (all(value == "Not Listed" for value in main_dict.values(
                    )))
            product_available = not (all(value == "Not Available" for value in main_dict.values(
                    )))
        if product_exists:
            if product_available:
                    return answers.msg_busca(message,dists,main_dict,contacts,last_update)
            else:
                    return "Me desculpe... O produto que você procura não esta disponível no momento."
        else:
            return "Me desculpe, o produto que você procura não esta disponível no momento... Lembre-se de confirir se seu Part Number é válido."
    else:
            return "Preciso de um Part Number para efetuar a busca, tente novamente por favor. Digite `help me` para receber ajuda"
def negotiator(webhook):
            if webhook['resource'] == "memberships" and webhook['data']['personEmail'] == bot_email:
                send_post("https://api.ciscospark.com/v1/messages",
                        {
                            "roomId": webhook['data']['roomId'],
                            "markdown": (answers.greetings(bot_name=bot_name) + answers.help_me(dists))
                        }
                        )
            msg = None
            if ('files' in webhook['data']) and (webhook['data']['personEmail'] in admins["admins"]):
                send_post("https://api.ciscospark.com/v1/messages",
                        {"roomId": webhook['data']['roomId'], "markdown": update_db(10,webhook)})
            if ('files' in webhook['data']) and (webhook['data']['personEmail'] not in admins["admins"]):
                send_post("https://api.ciscospark.com/v1/messages",
                        {"roomId": webhook['data']['roomId'], "markdown": "Desculpe... Acho você não tem permição para fazer Update do meu banco de dados :(<br/>"})
            if ("@webex.bot" not in webhook['data']['personEmail']) and ('files' not in webhook['data']):
                result = send_get(
                    'https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
                in_message = result.get('text', '').lower()
                in_message = in_message.replace(bot_name.lower() + " ", '')
                if in_message.startswith('help me'):
                    msg = answers.help_me(dists)
                elif in_message.startswith('admins'):
                    msg =  answers.msg_admins(admins)
                elif in_message.startswith('contatos'):
                    msg =  answers.msg_contatos(contacts,dists)
                elif in_message.startswith("buscar "):
                    message = in_message.split('buscar ')[1]
                    message = message.upper()
                    msg = buscar(message)
                elif in_message.startswith("top 20 "):
                    message = in_message.split('top 20 ')[1]
                    message = str(message).capitalize()
                    if str(message + ' Fast Track') in dists_FT:
                        result = pandas_queries.FT_TOP20(
                            data_FT[str(message + ' Fast Track')], col_list_FT)
                        result = json.loads(result)
                        msg = answers.top_20(message,result,col_list_FT,contacts,last_update)
                    elif str(message) == 'Stack':
                        result = pandas_queries.FT_TOP20_STACK(data_FT, col_list_FT)
                        result = json.loads(result)
                        msg = answers.top_20_stack(result,col_list_FT,last_update,dists,contacts)
                    else:
                        msg = "Desculpe, não conheço esse distribuidor... Tente digitar `Help me` para receber ajuda."
                elif in_message.endswith("top 20"):
                    msg = "Preciso de um Nome De Destribuidor para efetuar a busca, tente novamente por favor. Digite `help me` para receber ajuda"
                    pass
                if msg != None:
                    send_post("https://api.ciscospark.com/v1/messages",
                            {"roomId": webhook['data']['roomId'], "markdown": msg})
                return "Success"

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def teams_webhook():
    #switchcase
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        negotiator(webhook)
        return "true"


        
    elif request.method == 'GET':
        message = "<center><img src=\"https://cdn-images-1.medium.com/max/800/1*wrYQF1qZ3GePyrVn-Sp0UQ.png\"style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Don't forget to create/update your Webhooks to start receiving events from Webex Teams!</i></b></center>" % bot_name
        return message


def main():
    global bot_email, bot_name
    if len(bearer) != 0:
        test_auth = send_get(
            "https://api.ciscospark.com/v1/people/me", js=False)
        if test_auth.status_code == 401:
            print("Looks like the provided access token is not correct.\n"
                  "Please review it and make sure it belongs to your bot account.\n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.webex.com/my-apps "
                  "and generate a new access token.")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName", "")
            bot_email = test_auth.get("emails", "")[0]
    else:
        print("'bearer' variable is empty! \n"
              "Please populate it with bot's access token and run the script again.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.webex.com/my-apps "
              "and generate a new access token.")
        sys.exit()

    if "@webex.bot" not in bot_email:
        print("You have provided an access token which does not relate to a Bot Account.\n"
              "Please change for a Bot Account access token, view it and make sure it belongs to your bot account.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.webex.com/my-apps "
              "and generate a new access token for your Bot.")
        sys.exit()
    else:
        app.run(host='localhost', debug=True, port=8080)


if __name__ == "__main__":
    main()
