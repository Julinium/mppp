import re, requests
from bs4 import BeautifulSoup, Comment

import helper
import constants as C



def getJson(link_item):

    """
    # Synapsis:
        From a link, gets a structured object (JSON) representing data of the Consultation and all its related objects
    # Params:
        link_item: a line of the generated links file, containing pudlication date, portal id and organization acronym.
    # Return:
        JSON object representing data.
    """

    if link_item == None or len(link_item) < 3:
        helper.printMessage('ERROR', 'getter.getJson', 'Got an invalid link item.')
        return None
    helper.printMessage('DEBUG', 'getter.getJson', f'Getting objects for item id = {link_item[0]}')

    cons_uri = f"{link_item[0]}{C.LINK_STITCH}{link_item[1]}"
    cons_link = f'{C.LINK_PREFIX}{cons_uri}'
    dce_link = f'{C.SITE_INDEX}?page=entreprise.EntrepriseDownloadCompleteDce&reference={link_item[0]}&orgAcronym={link_item[1]}'

    rua = helper.getUa()
    rua_label = "Random"
    try:
        start_delimiter = "Mozilla/5.0 ("
        end_delimiter = "; "
        start_index = rua.index(start_delimiter) + len(start_delimiter)
        end_index = rua.index(end_delimiter, start_index)
        rua_label = rua[start_index:end_index]
    except ValueError as ve:
        helper.printMessage('ERROR', 'getter.getJson', f'Error trimming UA: {str(ve)}')
    
    helper.printMessage('DEBUG', 'getter.getJson', f'Using UA: {rua_label}.')
    headino = {"User-Agent": rua }
    sessiono = requests.Session()

    cons_bytes = 0
    try:
        dce_head = sessiono.head(dce_link, headers=headino, timeout=C.REQ_TIMEOUT, allow_redirects=True)
        if dce_head.status_code == 200 :
            if 'Content-Length' in dce_head.headers:
                cons_bytes = int(dce_head.headers['Content-Length'])
            # return None
        else:
            helper.printMessage('WARN', 'getter.getJson', f'Request to DCE Header page returned a {dce_head.status_code} status code.')
            if dce_head.status_code == 429:
                helper.printMessage('WARN', 'getter.getJson', f'Too many Requests, said the server: {dce_head.status_code} !')
                helper.sleepRandom(300, 600)
    except Exception as x:
        helper.printMessage('WARN', 'getter.getJson', f'Exception raised while getting file size at {str(dce_link)}: {str(x)}')
        # return None

    try: request_cons = sessiono.get(cons_link, headers=headino, timeout=C.REQ_TIMEOUT)  # driver.get(lots_link)
    except Exception as x:
        helper.printMessage('ERROR', 'getter.getJson', f'Exception raised while getting Cons at {str(cons_link)}: {str(x)}')
        return None
    helper.printMessage('DEBUG', 'getter.getJson', f'Getting Cons page : {request_cons}')
    if request_cons.status_code != 200 :
        helper.printMessage('ERROR', 'getter.getJson', f'Request to Cons page returned a {request_cons.status_code} status code.')
        if request_cons.status_code == 429:
            helper.printMessage('ERROR', 'getter.getJson', f'Too many Requests, said the server: {request_cons.status_code} !')
            helper.sleepRandom(300, 600)
        return None

    bowl = BeautifulSoup(request_cons.text, 'html.parser')


    soup = bowl.find(class_='recap-bloc')

    cons_idddd = link_item[0].strip()
    cons_pub_d = link_item[2].strip()

    deadl_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_dateHeureLimiteRemisePlis')
    cons_deadl = deadl_span.get_text().strip() if deadl_span else ""

    picto_img  = soup.find('img', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_pictCertificat')
    picto_src  = picto_img['src'].strip() if picto_img else ""
    cons_repec = picto_src.strip().replace('themes/images/', '').replace('.gif', '')

    cance_span = soup.find('img', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_pictConsultationAnnulee')
    cons_cance = True if cance_span else False

    category = None
    categ_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_categoriePrincipale')
    cons_categ = categ_span.get_text().strip() if categ_span else ""
    if cons_categ != "":
        category = {"label": cons_categ}

    refce_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_reference')
    cons_refce = refce_span.get_text().strip() if refce_span else ""

    objet_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_objet')
    cons_objet = objet_span.get_text().strip() if objet_span else ""

    helper.printMessage('DEBUG', 'getter.getJson', f'Found item: = {cons_objet[:C.TRUNCA]} ...')

    client = None
    achet_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_entiteAchat')
    cons_achet = achet_span.get_text().strip() if achet_span else ""
    if cons_achet != "":
        client = {"name": cons_achet}

    type = None
    type_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_annonce')
    cons_type = type_span.get_text().strip() if type_span else ""
    if cons_type != "":
        type = {"name": cons_type}
    
    procedure = None
    proce_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_typeProcedure')
    cons_proce = proce_span.get_text().strip() if proce_span else ""
    if cons_proce != "":
        procedure = {"name": cons_proce}

    mode = None
    passa_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_modePassation')
    cons_passa = passa_span.get_text().replace('|', '').strip() if passa_span else ""
    if cons_passa != "":
        mode = {"name": cons_passa}

    lexec_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_lieuxExecutions')
    cons_lexec = lexec_span.get_text().strip() if lexec_span else ""

    domai_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_domainesActivite')
    domains = []
    domai_lis  = domai_span.find_all('li')
    for domai_li in domai_lis:
        domai = domai_li.get_text().strip() if domai_li else ""
        if len(domai) > 1 : domains.append({"name": domai})

    add_r_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseRetraitDossiers')
    cons_add_r = add_r_span.get_text().strip() if add_r_span else ""

    add_d_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseDepotOffres')
    cons_add_d = add_d_span.get_text().strip() if add_d_span else ""

    add_o_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_lieuOuverturePlis')
    cons_add_o = add_o_span.get_text().strip() if add_o_span else ""

    plans_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_prixAcquisitionPlan')
    cons_plans = plans_span.get_text().strip() if plans_span else ""

    adm_n_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_contactAdministratif')
    cons_adm_n = adm_n_span.get_text().strip() if adm_n_span else ""

    adm_m_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_email')
    cons_adm_m = adm_m_span.get_text().strip() if adm_m_span else ""

    adm_t_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_telephone')
    cons_adm_t = adm_t_span.get_text().strip() if adm_t_span else ""

    adm_f_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_telecopieur')
    cons_adm_f = adm_f_span.get_text().strip() if adm_f_span else ""

    reser_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_idRefRadio_RepeaterReferentielRadio_ctl0_labelReferentielRadio')
    cons_reser = reser_span.get_text().strip() if reser_span else ""

    qualifs = []
    quali_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_qualification')
    # cons_quali = []
    quali_lis  = quali_span.find_all('li')
    for quali_li in quali_lis:
        qualif = quali_li.get_text().strip() if quali_li else ""
        if len(qualif) > 1 : qualifs.append({"name": qualif,})

    agrements = []
    agrem_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_agrements')
    # cons_agrem = []
    agrem_lis  = agrem_span.find_all('li')
    for agrem_li in agrem_lis:
        agrement = agrem_li.get_text().strip() if agrem_li else ""
        if len(agrement) > 1 : agrements.append({"name": agrement,})

    # Samples
    samples = []
    ech_d_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_dateEchantillons')
    cons_ech_d = ech_d_span.get_text().strip() if ech_d_span else ""
    ech_a_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseEchantillons')
    cons_ech_a = ech_a_span.get_text().strip() if ech_a_span else ""
    if len(cons_ech_d) > 3 or len(cons_ech_a) > 3 : samples.append({"when": cons_ech_d, "description": cons_ech_a})

    # Meetings
    meetings = []
    reu_d_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_dateReunion')
    cons_reu_d = reu_d_span.get_text().strip() if reu_d_span else ""
    reu_a_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_adresseReunion')
    cons_reu_a = reu_a_span.get_text().strip() if reu_a_span else ""
    if len(cons_reu_d) > 3 or len(cons_reu_a) > 3 : meetings.append({"when": cons_reu_d, "description": cons_reu_a})

    # Visits #
    visits = []
    vis_d_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_repeaterVisitesLieux_ctl1_dateVisites')
    cons_vis_d = vis_d_span.get_text().strip() if vis_d_span else ""
    vis_a_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_repeaterVisitesLieux_ctl1_adresseVisites')
    cons_vis_a = vis_a_span.get_text().strip() if vis_a_span else ""
    if len(cons_vis_d) > 3 or len(cons_vis_a) > 3 : visits.append({"when": cons_vis_d, "description": cons_vis_a})

    varia_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_varianteValeur')
    cons_varia = varia_span.get_text().strip() if varia_span else ""

    estim_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_idReferentielZoneText_RepeaterReferentielZoneText_ctl0_labelReferentielZoneText')
    cons_estim = estim_span.get_text().strip() if estim_span else ""

    cauti_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_cautionProvisoire')
    cons_cauti = cauti_span.get_text().strip() if cauti_span else ""

    sized_anch = bowl.find('a', id='ctl0_CONTENU_PAGE_linkDownloadDce')
    cons_sized = sized_anch.get_text().strip() if sized_anch else ""
    cons_sized = sized_anch.get_text().strip('Dossier de consultation -').strip() if sized_anch else ""

    nbrlo_span = soup.find('span', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_nbrLots')
    cons_nbrlo = nbrlo_span.get_text().replace('Lots', '').strip() if nbrlo_span else "1"
    if cons_nbrlo == '': cons_nbrlo = '1'

    lots_span = soup.find('a', id='ctl0_CONTENU_PAGE_idEntrepriseConsultationSummary_linkDetailLots')
    lots_href = ''
    if lots_span and lots_span.has_attr('href'): lots_href = lots_span['href']


    if len(lots_href) > 2:
        cons_lots = getLots(lots_href)
    else:
        cons_lots = [
            {
                "number": 1,
                "title": cons_objet,
                "category": category,
                "description": '',
                "estimate": cons_estim,
                "bond": cons_cauti,
                "reserved": cons_reser,
                "qualifs": qualifs,
                "agrements": agrements,
                "samples": samples,
                "meetings": meetings,
                "visits": visits,
                "variant": cons_varia,
                }
            ]

    cons_dict = {
        "published": cons_pub_d,
        "deadline": cons_deadl,
        "cancelled": cons_cance,
        "reference": cons_refce,
        "category": category,
        "lots_count": cons_nbrlo,
        "title": cons_objet,
        "location": cons_lexec,
        "client": cons_achet,
        "type": type,
        "procedure": procedure,
        "mode": mode,
        "ebid_esign": cons_repec,
        "lots": cons_lots,
        "plans_price": cons_plans,
        "domains": domains,
        "address_withdrawal": cons_add_r,
        "address_bidding": cons_add_d,
        "address_opening": cons_add_o,
        "contact_name": cons_adm_n,
        "contact_email": cons_adm_m,
        "contact_phone": cons_adm_t,
        "contact_fax": cons_adm_f,
        "chrono": cons_idddd,
        "link": cons_uri,
        "size_read": cons_sized,
        }

    return cons_dict


def getLots(lots_href):
    helper.printMessage('DEBUG', 'getter.getLots', 'Item is multi-lot. Reading lots ... ')
    lots_link = C.SITE_INDEX + lots_href.replace("javascript:popUp('index.php", "").replace("%27,%27yes%27)", "")

    rua = helper.getUa()
    rua_label = "Random"
    try:
        start_delimiter = "Mozilla/5.0 ("
        end_delimiter = "; "
        start_index = rua.index(start_delimiter) + len(start_delimiter)
        end_index = rua.index(end_delimiter, start_index)
        rua_label = rua[start_index:end_index]
    except ValueError as ve:
        helper.printMessage('WARN', 'getter.getLots', f'Error trimming UA: {str(ve)}')
    
    helper.printMessage('DEBUG', 'getter.getLots', f'Using UA: {rua_label}.')
    headino = {"User-Agent": rua }

    sessiono = requests.Session()

    try: request_lots = sessiono.get(lots_link, headers=headino, timeout=C.REQ_TIMEOUT)  # driver.get(lots_link)
    except Exception as x:
        helper.printMessage('ERROR', 'getter.getLots', f'Exception raised while getting lots at {str(lots_link)}: {str(x)}')
        return None
    helper.printMessage('DEBUG', 'getter.getLots', f'Getting Lots page : {request_lots}')
    if request_lots.status_code != 200 :
        helper.printMessage('ERROR', 'getter.getLots', f'Request to Lots page returned a {request_lots.status_code} status code.')
        if request_lots.status_code == 429:
            helper.printMessage('ERROR', 'getter.getLots', f'Too many Requests, said the server: {request_lots.status_code} !')
            helper.sleepRandom(300, 600)
        return None

    bowl = BeautifulSoup(request_lots.text, 'html.parser')

    soup = bowl.find(class_='content')

    lots = []

    def iscomment(elem):
        return isinstance(elem, Comment)

    separator = soup.find('div', class_='separator')
    comments = soup.find_all(string=iscomment)
    i = 0
    for comment in comments:
        if "Debut Lot 1" in comment :
            current_lot = {}

            # Number
            number_elem = comment.find_next_sibling("div", class_="intitule-bloc intitule-150")
            number_span = number_elem.find(class_='blue bold')
            number = number_span.get_text().strip('Lot').strip(':').strip() if number_span else ""

            # Title
            title_elem = number_elem.find_next_sibling("div", class_="content-bloc bloc-600")
            title = title_elem.get_text().strip() if title_elem else ""

            # Category
            category = None
            category_elem = title_elem.find_next_sibling("div", class_="content-bloc bloc-600")
            categ = category_elem.get_text().strip() if category_elem else ""
            if categ != "":
                category = {"label": categ}
            

            # Extract Description
            description_elem = category_elem.find_next_sibling("div", class_="content-bloc bloc-600")
            description = description_elem.get_text().strip() if description_elem else ""

            # Estimation
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_idReferentielZoneTextLot_RepeaterReferentielZoneText_ctl0_panelReferentielZoneText'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_idReferentielZoneTextLot_RepeaterReferentielZoneText_ctl0_labelReferentielZoneText'
            estimation_div  = description_elem.find_next_sibling("div", id=div_id)
            estimation_span = estimation_div.find('span', id=span_id)
            estimation = estimation_span.get_text().strip() if estimation_span else ""

            # Caution Provisoire
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelCautionProvisoire'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_cautionProvisoire'
            caution_div  = estimation_div.find_next_sibling("div", id=div_id)
            caution_span = caution_div.find('span', id=span_id)
            caution = caution_span.get_text().strip() if caution_span else ""


            # Qualifications
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelQualification'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_qualification'
            qualifs_div  = caution_div.find_next_sibling("div", id=div_id)
            qualifs_span = qualifs_div.find('span', id=span_id)
            qualifs_lis = qualifs_span.find_all('li')
            qualifs = []
            for qualifs_li in qualifs_lis :
                qualif = qualifs_li.get_text().strip() if qualifs_li else ""
                if qualif != '' : qualifs.append({"name": qualif,})

            # Agrements
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelAgrements'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_agrements'
            agrements_div  = qualifs_div.find_next_sibling("div", id=div_id)
            agrements_span = agrements_div.find('span', id=span_id)
            agrements_lis = agrements_span.find_all('li')
            agrements = []
            for agrements_li in agrements_lis :
                agrement = agrements_li.get_text().strip() if agrements_li else ""
                if agrement != '' : agrements.append({"name": agrement,})

            # Samples
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelEchantillons'
            samples_div  = agrements_div.find_next_sibling("div", id=div_id)
            samples_lis = samples_div.find_all('li')
            samples = []
            for samples_li in samples_lis :
                span_d_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_repeaterVisitesLieux_ctl1_Echantillons'
                span_l_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_repeaterVisitesLieux_ctl1_Echantillons'
                sample_spans = samples_li.find_all('span')
                if len(sample_spans) > 1 :
                    sample_date = sample_spans[0].get_text().strip() if sample_spans[0] else ""
                    sample_lieu = sample_spans[1].get_text().strip() if sample_spans[1] else ""
                    sample = {
                        "when": re.sub(r'\s+', ' ', sample_date).strip(),
                        "description": re.sub(r'\s+', ' ', sample_lieu).strip(),
                        }
                samples.append(sample)

            # Meetings
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelReunion'
            span_id_d = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_dateReunion'
            span_id_a = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_adresseReunion'
            meeting_div  = samples_div.find_next_sibling("div", id=div_id)
            meeting_span_d = meeting_div.find('span', id=span_id)
            meeting_span_a = meeting_div.find('span', id=span_id)
            meeting_d = meeting_span_d.get_text().strip() if meeting_span_d else ""
            meeting_a = meeting_span_a.get_text().strip() if meeting_span_a else ""
            meetings = []
            if len(meeting_d) > 3 or len(meeting_a) > 3 : meetings.append({"when": meeting_d, "description": meeting_a})

            # In-site Visits
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelVisitesLieux'
            # span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelRepeaterVisitesLieux'
            visits_div  = meeting_div.find_next_sibling("div", id=div_id)
            visits_lis = visits_div.find_all('li')
            visits = []
            for visits_li in visits_lis :
                span_d_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_repeaterVisitesLieux_ctl1_dateVisites'
                span_l_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_repeaterVisitesLieux_ctl1_dateVisites'
                visit_spans = visits_li.find_all('span')
                if len(visit_spans) > 1 :
                    visit_date = visit_spans[0].get_text().strip() if visit_spans[0] else ""
                    visit_lieu = visit_spans[1].get_text().strip() if visit_spans[1] else ""
                    visit = {
                        "when": re.sub(r'\s+', ' ', visit_date).strip(),
                        "description": re.sub(r'\s+', ' ', visit_lieu).strip(),
                        }
                visits.append(visit)


            # Variante
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_panelVariante'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_varianteValeur'
            variante_div  = visits_div.find_next_sibling("div", id=div_id)
            variante_span = variante_div.find("div", class_="content-bloc bloc-600")
            variante = variante_span.get_text().strip() if variante_span else ""


            # ReservePME
            div_id  = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_idRefRadio_RepeaterReferentielRadio_ctl0_panelReferentielRadio'
            span_id = f'ctl0_CONTENU_PAGE_repeaterLots_ctl{i}_idRefRadio_RepeaterReferentielRadio_ctl0_labelReferentielRadio'
            pme_div  = variante_div.find_next_sibling("div", id=div_id)
            pme_span = pme_div.find('span', id=span_id)
            pme = pme_span.get_text().strip() if pme_span else ""


            # Store extracted data for current lot

            current_lot = {
                "number": number,
                "title": title,
                "category": category,
                "description": description,
                "estimate": estimation,
                "bond": caution,
                "qualifs": qualifs,
                "agrements": agrements,
                "samples": samples,
                "meetings": meetings,
                "visits": visits,
                "variant": variante,
                "reserved": pme,
                }

            lots.append(current_lot)
            i += 1
    return lots
