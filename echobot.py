import json
import requests
import time
import urllib
import numpy as np

TOKEN = "496952154:AAEU1FLmT3wBsd83YNDezv5K04EG9CCDWx8"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    gate = True
    q_no = 1

    last_textchat = (None, None)
    text, chat = get_last_chat_id_and_text(get_updates())
    send_message("Hi and welcome to Pre-Anaesthesia Health Assessment! I am SleepBot your assistant for today!", chat)
    send_message("We have a few questions for you before we go into the Operating Theatre", chat)
    send_message("If you do not understand or are not sure about questions and/or answers, "
                 "please ask me or the healthcare professional you will speak to after. "
                 "Shall we begin? ", chat)


    while True:
        if gate is True:
            text, chat = get_last_chat_id_and_text(get_updates())
            if text == "yes":
                q_no += 0.1
                gate = False

            if text == "no":
                q_no += 1
                gate = False

            time.sleep(0.5)

        if q_no == 1:
            send_message("Do you need an interpreter?", chat)
        if q_no == 1.1:
            send_message("Which is your preferred language?", chat)
            q_no = np.around(q_no)

        if q_no == 2:
            send_message("Do you have any religious/cultural needs?", chat)
        if q_no == 2.1:
            send_message("Can you provide your religion details?", chat)
            q_no = np.around(q_no)

        if q_no == 3:
            send_message("Do you have any allergies(medicines, sticking plaster, iodine, latex, food, etc.)?", chat)
        if q_no == 3.1:
            send_message("Can you provide details on your allergies?", chat)
            q_no = np.around(q_no)

        if q_no == 4:
            send_message("Are you in good physical condition?", chat)
        if q_no == 4.1:
            send_message("Can you provide your illness/surgical history?", chat)
            q_no = np.around(q_no)

        if q_no == 5:
            send_message("Have you seen a (specialist) doctor for any medical condition?", chat)
        if q_no == 5.1:
            send_message("Can you provide details of your last visits?", chat)
            q_no = np.around(q_no)

        if q_no == 6:
            send_message("Have you ever had surgery performed?", chat)
        if q_no == 6.1:
            send_message("Can you provide details of your last surgeries?", chat)
            q_no = np.around(q_no)




                # if (text, chat) != last_textchat:
    #     send_message("Do you need an interpreter?", chat)
    #     text, chat = get_last_chat_id_and_text(get_updates())
    #     time.sleep(2)
    #
    #     if text == "yes":
    #         send_message("Which Language will you prefer?", chat)
    #         text, chat = get_last_chat_id_and_text(get_updates())
    #     if text == "no":
    #         send_message("Do you have any religious/cultural needs?", chat)
    #         text, chat = get_last_chat_id_and_text(get_updates())
    #         time.sleep(2)
    #
    #         if text == "yes":
    #             send_message("Can you provide some details?", chat)
    #             text, chat = get_last_chat_id_and_text(get_updates())
    #         if text == "no":
    #             send_message("Do you have any allergies?", chat)
    #             text, chat = get_last_chat_id_and_text(get_updates())
    #             time.sleep(2)


if __name__ == '__main__':
    main()

