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
    body = request.body.decode("utf-8")
    update = Update(body)
    body = update.json
    body['validations'] = {
        "is_edited": None,
        "is_valid_request": None,
        "has_text": None,
        "contains_command": None,
        "contains_single_command": None,
        "startswith_command": None,
        "is_valid_command": None,
        "the_command": None,
        "the_argument": None,
        "is_flow": None,
    }

    if update.is_edited:
        # Não responde nada
        # body['validations']['is_edited'] = True
        return HttpResponse(status=200)

    body['validations']['is_edited'] = False

    if not update.is_valid_request:
        # body['validations']['is_valid_request'] = False
        error_answer(update, "Sorry, I don't accept "
                             "this kind of requisition")
        return HttpResponse(status=200)

    body['validations']['is_valid_request'] = True

    message = update.message
    Chat.objects.get_or_create(
        id=body['message']['chat']['id'],
        defaults=body['message']['chat'],
    )

    if not hasattr(message, 'text'):
        # body['validations']['has_text'] = False
        error_answer(update, ("Sorry, I only accept text messages "
                              "(or puppy pics, BUT with a caption)"))
        return HttpResponse(status=200)

    body['validations']['has_text'] = True

    if message.contains_command:
        body['validations']['contains_command'] = True

        if not message.contains_single_command:
            # body['validations']['contains_single_command'] = False
            error_answer(update, ("Your message have multiple commands, "
                                  "and I can't handle this (yet)"))
            return HttpResponse(status=200)

        body['validations']['contains_single_command'] = True

        if not message.startswith_command:
            # body['validations']['startswith_command'] = False
            error_answer(update, ("Please, place the command at "
                                  "the beginning of the message"))
            return HttpResponse(status=200)

        body['validations']['startswith_command'] = True

        if not message.is_valid_command(COMMANDS):
            # body['validations']['is_valid_command'] = False
            error_answer(update, "Sorry, The Master didn't "
                                 "train me to do that")
            return HttpResponse(status=200)

        body['validations']['is_valid_command'] = True
        body['validations']['the_command'] = message.the_command
        body['validations']['the_argument'] = message.the_argument

        COMMANDS[message.the_command].delay(body)
        return HttpResponse(status=200)

    else:
        body['validations']['contains_command'] = False

        if update.message.chat_model.state == 'root':
            # body['validations']['is_flow'] = False
            error_answer(update, ("Your message has no commands.\nSend me "
                                  "/help to know everything I can do!"))
            return HttpResponse(status=200)

        else:
            body['validations']['is_flow'] = True

            last_cmd = update.message.chat_model.get_state_json()['last_cmd']

            body['validations']['the_command'] = last_cmd
            body['validations']['the_argument'] = message.the_argument

            COMMANDS[last_cmd].delay(body)

            return HttpResponse(status=200)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def status(request):
    return JsonResponse({'ok': True, 'method': request.method}, status=200)
