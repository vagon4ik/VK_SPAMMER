import vk_api
from vk_api import VkUpload
import time


def main():

    print()
    print('Welcome to vk_spammer.py')
    print('Write <help> to get command list')

    # Цикл-интерфейс
    while True:

        print()
        print('vk_spammer: ', end='')
        cmd = input()
        print()

        if cmd.split()[0] == 'help':
            print(' <help> - get help')
            print(" <spam> [personsFile] [id] [textFile] [times] [reload] [mediaFile]- spam person, where personsFile is file with spammer's name (login:password\\n), id - prey's id, times - spam times, textFile - file with spam text, reload - spam times reload, mediaRel - way to image ([] are not important properties)")
            print(' <quit> - exit program')
            print(' <hey> - greet program')
        elif cmd.split()[0] == 'spam':
            print('Process have been started...')
            try:
                print(*(cmd.split()[1:]))
                spam(*(cmd.split()[1:]))
            except Exception as e:
                print('Error:', e)
            print('Process have been ended')
        elif cmd.split()[0] == 'quit':
            break
        elif cmd.split()[0] == 'hey':
            print('hey')
        else:
            print('Command not found')
            print('Write <help> to get command list')

def spam(personsFile='persons.txt', id=None, textFile='message.txt', times=1, reload=1, mediaRel=None):

    with open(personsFile, 'r', encoding='utf-8') as file:
        arr = file.read().split('\n')

    with open(textFile, 'r', encoding='utf-8') as file:
        text = file.read()

    id = int(id)
    times = int(times)
    reload = int(reload)

    session_dic = {}
    isMediaUpload = False

    if mediaRel != None:
        isMedia = True
    else:
        isMedia = False

    for item in arr:
        session_dic[item.split(':')[0]] = item.split(':')[1]

    print('Loop have been started')
    for cnt in range(times):
        for key in session_dic.keys():
            try:
                print('Connect to person with login: ', key) # Вывод информации о текущей сессии
                vk_session = vk_api.VkApi(key, session_dic[key])
                try:
                    vk_session.auth()
                except Exception as e:
                    print('Error:', e)
                    continue
                print('Connected')
                vk = vk_session.get_api()

                # Проверка на наличие медиа в сообщении
                print('Send message...')
                if isMedia:
                    if not isMediaUpload:
                        # Загрузка медиа только на страницу первого
                        # успешно авторизированного пользователя
                        print('Upload media...')
                        mediaUrl = mediaResponse(vk_session, mediaRel)
                        print('Media have been uploaded with name: {}'.format(mediaUrl))
                        isMediaUpload = True
                    # Отправка сообщения с медиа
                    vk.messages.send(
                    user_id = id,
                    attachment = mediaUrl,
                    message = text
                    )
                else:
                    # Отправка сообщения без медиа
                    vk.messages.send(
                    user_id = id,
                    message = text
                    )
                print('Message have been sended')
            # Любое исключение
            except Exception as e:
                print('Error', e)
        time.sleep(reload)
        print('Loop have been iterated {} time(s)'.format(cnt+1))
    print('Loop have been ended')

# Загрузка медиа на страницу пользователя
def mediaResponse(vk_session, mediaRel):

    upload = VkUpload(vk_session)

    media = upload.photo_messages(photos=mediaRel)[0]

    return 'photo{}_{}'.format(media['owner_id'], media['id'])

if __name__ == '__main__':
    main()
