def msg_admins(admins):
               return   '<br/>'\
                        '<h4> Os meus administradores são:</h4>' \
                        '<ul>'\
                        '<li>' + admins["admins"][0] +'</li>' \
                        '<li>' + admins["admins"][1] +'</li>' \
                        '<li>' + admins["admins"][2] +'</li>' \
                        '<li>' + admins["admins"][3] +'</li>' \
                        '</ul>'
def msg_contatos(contacts,dists):
        return  '<br/>'\
                '<h4>Informações para contato com os distriubuidores:</h4>'\
                '<ul>'\
                '<li>' + str(dists[0]) + ' - ' + str(contacts["Ingram"][0]) + ' - ' + str(contacts["Ingram"][1]) + ' - ' + str(contacts["Ingram"][2])+'</li>' \
                '<li>' + str(dists[1]) + ' - ' + str(contacts["Comstor"][0]) + ' - ' + str(contacts["Comstor"][1]) + ' - ' + str(contacts["Comstor"][2])+'</li>' \
                '<li>' + str(dists[2])+' - ' + str(contacts["Scansource"][0]) + ' - ' + str(contacts["Scansource"][1]) + ' - ' + str(contacts["Scansource"][2])+'</li>' \
                '</ul>'
def msg_busca(message,dists,main_dict,contacts,last_update):
    return  '<br/>'\
            '<h4>Part Number a ser procurado: **' + str(message) + '**</h4>' \
            '<ul>'\
            '<li>*' + str(dists[0]) + ':* ' + str(main_dict["Ingram"]) + '</li>' \
            '<li>*' + str(dists[1]) + ':* ' + str(main_dict["Comstor"]) + '</li>'\
            '<li>*' + str(dists[2]) + ':* ' + str(main_dict["Scansource"]) + '</li>'\
            '</ul>'\
            '<h4>Data da última atualização: ' + str(last_update["Day"])+'/'+str(last_update["Month"])+'/'+str(last_update["Year"])+'</h4>'\
            '</br>'\
            '<h4>Informações para contato:</h4>'\
            '<ul>'\
            '<li>' + str(dists[0]) + ' - ' + str(contacts["Ingram"][0]) + ' - ' + str(contacts["Ingram"][1]) + ' - ' + str(contacts["Ingram"][2])+'</li>' \
            '<li>' + str(dists[1]) + ' - ' + str(contacts["Comstor"][0]) + ' - ' + str(contacts["Comstor"][1]) + ' - ' + str(contacts["Comstor"][2])+'</li>' \
            '<li>' + str(dists[2])+' - ' + str(contacts["Scansource"][0]) + ' - ' + str(contacts["Scansource"][1]) + ' - ' + str(contacts["Scansource"][2])+'</li>' \
            '</ul>'

def help_me(dists):

    return "<br/>" \
        "<h3>Claro! Seguem abaixo alguns comandos que consigo entender...</h3>" \
        '<ul>'\
        "<li>**Help me** - Mostra o que posso fazer</li>" \
        "<li>**Admins** - Mostra meus administradores</li>" \
        "<li>**Contatos** - Mostra informações para contato com os distribuidores disponíveis</li>" \
        '<li>**Buscar** ***PART NUMBER*** - Busca pelo part number fornecido. Tente o comando: `Buscar WS-C2960X-24PS-BR`</li>'\
        "<li>**Top 20** ***DISTRIBUIDOR*** - Busca pelos top 20 produtos Fast Track com maior quantidade disponível por distribuidor. Tente o comando: `Top 20 Ingram`</li>" \
        "<li>**Top 20** **Stack** - Busca pelos top 20 produtos Fast Track com maior quantidade disponível dentre todos os distribuidores. Tente o comando: `Top 20 Stack`</li>" \
        '</ul>'\
        "<h4>Distribuidores disponíveis:</h4>" \
        '<ul>'\
        '<li>' + str(dists[0])+'</li>' \
        '<li>' + str(dists[1])+'</li>'\
        '<li>' + str(dists[2]) + '</li>'\
        '</ul>'
def top_20(message,result,col_list_FT,contacts,last_update):

    return  '<br/>'\
            '<h4>TOP 20 FT: ' + str(message) + '</h4>' \
                        '<br/>'\
                        '<ol>'\
                        + "<li>*"+str(result['0'][col_list_FT[0]]) + '*   ' + str(int(result['0'][col_list_FT[-1]])) + "</li>" \
                        + "<li>*"+str(result['1'][col_list_FT[0]]) + '*   ' + str(int(result['1'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['2'][col_list_FT[0]]) + '*   ' + str(int(result['2'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['3'][col_list_FT[0]]) + '*   ' + str(int(result['3'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['4'][col_list_FT[0]]) + '*   ' + str(int(result['4'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['5'][col_list_FT[0]]) + '*   ' + str(int(result['5'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['6'][col_list_FT[0]]) + '*   ' + str(int(result['6'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['7'][col_list_FT[0]]) + '*   ' + str(int(result['7'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['8'][col_list_FT[0]]) + '*   ' + str(int(result['8'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['9'][col_list_FT[0]]) + '*   ' + str(int(result['9'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['10'][col_list_FT[0]]) + '*   ' + str(int(result['10'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['11'][col_list_FT[0]]) + '*   ' + str(int(result['11'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['12'][col_list_FT[0]]) + '*   ' + str(int(result['12'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['13'][col_list_FT[0]]) + '*   ' + str(int(result['13'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['14'][col_list_FT[0]]) + '*   ' + str(int(result['14'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['15'][col_list_FT[0]]) + '*   ' + str(int(result['15'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['16'][col_list_FT[0]]) + '*   ' + str(int(result['16'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['17'][col_list_FT[0]]) + '*   ' + str(int(result['17'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['18'][col_list_FT[0]]) + '*   ' + str(int(result['18'][col_list_FT[-1]])) + "</li>"  \
                        + "<li>*"+str(result['19'][col_list_FT[0]]) + '*   ' + str(int(result['19'][col_list_FT[-1]])) + "</li>"  \
                        '<ol/>'\
                        '</br>'\
                        '**Data da última atualização: ' + str(last_update["Day"])+'/'+str(last_update["Month"])+'/'+str(last_update["Year"])+'**'\
                        '</br>'\
                        '</br>'\
                        '<h4>Informações para contato:</h4>'\
                        '</br>'\
                        + str(message) + ' - ' + str(contacts[str(message)][0]) + ' - ' + str(
                            contacts[str(message)][1]) + ' - ' + str(contacts[str(message)][2])+'<br/>'
def top_20_stack(result,col_list_FT,last_update,dists,contacts):
    return  '<br/>'\
            '<h4>***TOP 20 Produtos Fast Track***</h4>' \
            '<br/>'\
            '<ol>'\
            + "<li>*"+str(result['0'][col_list_FT[0]]) + '*   ' + str(int(result['0'][col_list_FT[-1]])) + "</li>" \
            + "<li>*"+str(result['1'][col_list_FT[0]]) + '*   ' + str(int(result['1'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['2'][col_list_FT[0]]) + '*   ' + str(int(result['2'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['3'][col_list_FT[0]]) + '*   ' + str(int(result['3'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['4'][col_list_FT[0]]) + '*   ' + str(int(result['4'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['5'][col_list_FT[0]]) + '*   ' + str(int(result['5'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['6'][col_list_FT[0]]) + '*   ' + str(int(result['6'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['7'][col_list_FT[0]]) + '*   ' + str(int(result['7'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['8'][col_list_FT[0]]) + '*   ' + str(int(result['8'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['9'][col_list_FT[0]]) + '*   ' + str(int(result['9'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['10'][col_list_FT[0]]) + '*   ' + str(int(result['10'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['11'][col_list_FT[0]]) + '*   ' + str(int(result['11'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['12'][col_list_FT[0]]) + '*   ' + str(int(result['12'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['13'][col_list_FT[0]]) + '*   ' + str(int(result['13'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['14'][col_list_FT[0]]) + '*   ' + str(int(result['14'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['15'][col_list_FT[0]]) + '*   ' + str(int(result['15'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['16'][col_list_FT[0]]) + '*   ' + str(int(result['16'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['17'][col_list_FT[0]]) + '*   ' + str(int(result['17'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['18'][col_list_FT[0]]) + '*   ' + str(int(result['18'][col_list_FT[-1]])) + "</li>"  \
            + "<li>*"+str(result['19'][col_list_FT[0]]) + '*   ' + str(int(result['19'][col_list_FT[-1]])) + "</li>"  \
            '<ol/>'\
            '</br>'\
            '**Data da última atualização: ' + str(last_update["Day"])+'/'+str(last_update["Month"])+'/'+str(last_update["Year"])+'**'\
            '</br>'\
            '<h4>Informações para contato:</h4>'\
            '<ul>'\
            '<li>' + str(dists[0]) + ' - ' + str(contacts["Ingram"][0]) + ' - ' + str(contacts["Ingram"][1]) + ' - ' + str(contacts["Ingram"][2])+'</li>' \
            '<li>' + str(dists[1]) + ' - ' + str(contacts["Comstor"][0]) + ' - ' + str(contacts["Comstor"][1]) + ' - ' + str(contacts["Comstor"][2])+'</li>' \
            '<li>' + str(dists[2])+' - ' + str(contacts["Scansource"][0]) + ' - ' + str(contacts["Scansource"][1]) + ' - ' + str(contacts["Scansource"][2])+'</li>' \
            '</ul>'\
            '</br>'

def greetings(bot_name):

    return "Olá Me chamo %s.<br/>" \
           "Digite `Help me` para ver no que eu posso te ajudar.<br/>" % bot_name