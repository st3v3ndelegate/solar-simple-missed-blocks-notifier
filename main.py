import requests as requests
import json

telegram_bot_key = "<BOT_KEY>"
telegram_chat_id = "<CHAT_ID>"

delegates_to_check = [
    "st3v3n"
]


def load_previous_missed_blocks():
    with open('missed_blocks.json', 'r') as f:
        return json.load(f)


def get_missed_blocks():
    response = requests.get('https://api.solar.org/api/blocks/missed')

    if response.status_code == 200:
        data = json.loads(response.text)["data"]
        return data
    else:
        print("Request failed with status code:", response.status_code)
        return []


def send_a_message(message):
    url = 'https://api.telegram.org/bot' + telegram_bot_key + '/sendMessage'
    data = {
        'chat_id': telegram_chat_id,
        'text': message
    }
    requests.post(url, data=data)


if __name__ == '__main__':
    previous_missed_blocks = load_previous_missed_blocks()
    current_missed_blocks = get_missed_blocks()
    for block in current_missed_blocks:
        if block["username"] in delegates_to_check and str(block["timestamp"]["epoch"]) not in previous_missed_blocks:
            print(block["username"] + " missed a block")
            previous_missed_blocks[str(block["timestamp"]["epoch"])] = block
            send_a_message(block["username"] + " missed a block")
    with open('missed_blocks.json', "w") as outfile:
        json.dump(previous_missed_blocks, outfile, indent=4)
