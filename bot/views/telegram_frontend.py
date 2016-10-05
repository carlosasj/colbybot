from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .. import tasks

from ..models import Update, Chat

COMMANDS = {
    '/cancel': tasks.cancel,
    '/start': tasks.start,
    '/help': tasks.help_,
    '/docs': tasks.docs,
    '/new': tasks.new,
    '/subscribe': tasks.subscribe,
    '/unsubscribe': tasks.unsubscribe,
    '/info': tasks.info,
    '/revoke': tasks.revoke,
    '/list': tasks.list_,
    '/delete': tasks.delete,
    '/stop': tasks.stop,
}


def error_answer(update, text, parse_mode=None):
    msg = {
        "chat_id": update.json['message']['chat']['id'],
        "text": text
    }
    if parse_mode is not None:
        msg["parse_mode"] = parse_mode
        tasks.send_message.delay(msg)


@csrf_exempt
@require_http_methods(['POST'])
def parse_commands(request):
    update = Update(request.body)

    if update.is_edited:
        # Não responde nada
        print('FRONTEND: Is edited')
        return HttpResponse(status=200)

    if not update.is_valid_request:
        print('FRONTEND: Is invalid')
        error_answer(update, "Sorry, I don't accept "
                             "this kind of requisition")
        return HttpResponse(status=200)

    message = update.message
    Chat.objects.get_or_create(
        id=update.json['message']['chat']['id'],
        defaults=update.json['message']['chat'],
    )

    if not hasattr(message, 'text'):
        print('FRONTEND: Has no text')
        error_answer(update, ("Sorry, I only accept text messages "
                              "(or puppy pics, BUT with a caption)"))
        return HttpResponse(status=200)

    if update.message.chat_model.state == 'root':
        # Começa o fluxo que exige ao menos um comando, já que não houve
        # mensagens anteriores alterando o estado do usuário
        if not message.contains_command:
            print('FRONTEND: Has no command')
            error_answer(update, ("Your message has no commands.\nSend me "
                                  "/help to know everything I can do!"))
            return HttpResponse(status=200)

        if not message.contains_single_command:
            print('FRONTEND: Has multiple commands')
            error_answer(update, ("Your message have multiple commands, "
                                  "and I can't handle this (yet)"))
            return HttpResponse(status=200)

        if not message.startswith_command:
            print('FRONTEND: Does not start with command')
            error_answer(update, ("Please, place the command at "
                                  "the beginning of the message"))
            return HttpResponse(status=200)

        if not message.is_valid_command(COMMANDS):
            print('FRONTEND: Is invalid command')
            error_answer(update, "Sorry, The Master didn't "
                                 "train me to do that")
            return HttpResponse(status=200)

        print('FRONTEND: Command identified as "{}"'
              .format(message.the_command))
        COMMANDS[message.the_command].delay(update.json)
        # Fim do fluxo que espera por um comando na mensagem
    else:
        # Começa o fluxo que NÃO espera nenhum comando, porque a mensagem
        # anterior que definiu o comando, e agora só vem o argumento
        pass

    return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def status(request):
    return JsonResponse({'ok': True, 'method': request.method}, status=200)
