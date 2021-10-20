import os
from datetime import datetime
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class SpeedTestLauncher(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, _, __):
        stream = os.popen('speedtest')
        response = stream.read()
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        result_str = ''

        if 'Download' in response:
            filtered = filter(
                lambda el: 'Download' in el or 'Upload' in el or 'Loss' in el or 'Result' in el, response.split('\n'))
            trimmed = map(lambda el: el.strip(), list(filtered))
            result_str = '\n'.join([str(elem) for elem in list(trimmed)])

        else:
            result_str = 'Error occured'

        result = f'notify-send "Speedtest {dt_string}" "{result_str}"'
        os.system(result)

        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=f'{result_str}',
                                                           description="SPEEDTEST®",
                                                           on_enter=HideWindowAction())])


if __name__ == '__main__':
    SpeedTestLauncher().run()
