import logging
import requests

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

logger = logging.getLogger(__name__)


class LinguatoolsConjugationsService:
    def __init__(self):
        self.base_url = "https://linguatools-conjugations.p.rapidapi.com/conjugate/"
        self.api_key = None

    def request_conjugations(self, verb):
        try:
            logger.info(self.api_key)
            querystring = {"verb": verb}
            headers = {
                'x-rapidapi-key': self.api_key,
                'x-rapidapi-host': "linguatools-conjugations.p.rapidapi.com"
            }
            response = requests.request("GET", self.base_url, headers=headers, params=querystring)
            response = response.json()

            if response["result"] != "OK":
                raise ValueError

            return response
        except KeyError or ValueError as err:
            raise err


class VerbFormsCheckerExtension(Extension):

    def __init__(self):
        super(VerbFormsCheckerExtension, self).__init__()
        self.service = LinguatoolsConjugationsService()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())

    def get_conjugations(self, verb):
        result_items = []

        try:
            conjugations = self.service.request_conjugations(verb)

            for conjugated_form in conjugations['conjugated_forms']:
                result_items.append(ExtensionResultItem(icon='images/icon.png',
                                                        name=conjugated_form[1],
                                                        description=conjugated_form[0],
                                                        highlightable=False,
                                                        on_enter=CopyToClipboardAction(conjugated_form[1])
                                                        ))

            # addition, progressive/continuous form
            random_progressive_phrase = conjugations["conjugation_tables"]["conditional"][1]["forms"][0][1]
            progressive_form = random_progressive_phrase.split()[-1]

            result_items.append(ExtensionResultItem(icon='images/icon.png',
                                                    name=progressive_form,
                                                    description="Progressive",
                                                    highlightable=False,
                                                    on_enter=CopyToClipboardAction(progressive_form)
                                                    ))
        except ValueError or KeyError:
            result_items.append(ExtensionResultItem(icon='images/icon.png',
                                                    name="Invalid response from Linguatools",
                                                    description='Word is not a verb/wrong API key',
                                                    highlightable=False
                                                    ))

        return result_items

    def error(self, title: str, msg: str):
        return [
            ExtensionResultItem(
                icon='images/icon.png',
                name=title,
                highlightable=False,
                description=msg
            )
        ]

    def get_argument_error(self):
        return self.error("😔", "Can only process a single (verb) word")

    def get_empty_argument_error(self):
        return self.error("😔", "Please input a word")

    def get_api_key_error(self):
        return self.error("😔", "Please specify the API key in the config")


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        argument = event.get_argument() or ""
        if argument == "":
            return RenderResultListAction(extension.get_empty_argument_error())

        extension.service.api_key = extension.preferences.get("verbforms_apikey")
        if extension.service.api_key is None:
            return RenderResultListAction(extension.get_api_key_error())

        total_words = len(argument.split())
        if total_words > 1:
            return RenderResultListAction(extension.get_argument_error())
        else:
            return RenderResultListAction(extension.get_conjugations(argument))


if __name__ == '__main__':
    VerbFormsCheckerExtension().run()
