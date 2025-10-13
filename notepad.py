import TkEasyGUI as eg
from tkinter import filedialog
import os


class Notepad:
    def __init__(self):
        self.current_file = None
        self.modified = False
        
        # レイアウト定義
        menu_def = [
            ['ファイル(&F)', ['新規作成(&N)', '開く(&O)', '保存(&S)', '名前を付けて保存(&A)', '---', '終了(&X)']],
            ['編集(&E)', ['元に戻す(&U)', '切り取り(&T)', 'コピー(&C)', '貼り付け(&P)', '---', 'すべて選択(&A)']],
            ['ヘルプ(&H)', ['バージョン情報(&A)']]
        ]
        
        layout = [
            [eg.Menu(menu_def, key='-MENU-')],
            [eg.Multiline(
                '', 
                size=(80, 25), 
                key='-TEXT-',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                font=('MS Gothic', 11)
            )],
            [eg.Text('行: 1, 列: 1', key='-STATUS-', size=(70, 1)), 
             eg.Push(),
             eg.Text('文字数: 0', key='-CHARCOUNT-')]
        ]
        
        self.window = eg.Window(
            'メモ帳 - 無題',
            layout,
            resizable=True,
            finalize=True,
            size=(800, 600)
        )
        
        # テキストエリアの変更を検知
        self.window['-TEXT-'].bind('<KeyRelease>', self._on_text_change)
        self.window['-TEXT-'].bind('<ButtonRelease>', self._on_cursor_move)
    
    def _on_text_change(self, event=None):
        """テキスト変更時の処理"""
        self.modified = True
        self._update_status()
        self._update_title()
    
    def _on_cursor_move(self, event=None):
        """カーソル移動時の処理"""
        self._update_status()
    
    def _update_status(self):
        """ステータスバーの更新"""
        try:
            text_widget = self.window['-TEXT-'].widget
            cursor_pos = text_widget.index('insert')
            line, col = cursor_pos.split('.')
            self.window['-STATUS-'].update(f'行: {line}, 列: {int(col)+1}')
            
            text_content = self.window['-TEXT-'].get()
            char_count = len(text_content)
            self.window['-CHARCOUNT-'].update(f'文字数: {char_count}')
        except:
            pass
    
    def _update_title(self):
        """ウィンドウタイトルの更新"""
        filename = os.path.basename(self.current_file) if self.current_file else '無題'
        modified_mark = '*' if self.modified else ''
        self.window.set_title(f'メモ帳 - {filename}{modified_mark}')
    
    def new_file(self):
        """新規作成"""
        if self.modified:
            response = eg.popup_yes_no('変更を保存しますか？', title='確認')
            if response == 'Yes':
                self.save_file()
        
        self.window['-TEXT-'].update('')
        self.current_file = None
        self.modified = False
        self._update_title()
        self._update_status()
    
    def open_file(self):
        """ファイルを開く"""
        if self.modified:
            response = eg.popup_yes_no('変更を保存しますか？', title='確認')
            if response == 'Yes':
                self.save_file()
        
        filename = filedialog.askopenfilename(
            title='ファイルを開く',
            filetypes=[('テキストファイル', '*.txt'), ('すべてのファイル', '*.*')]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.window['-TEXT-'].update(content)
                self.current_file = filename
                self.modified = False
                self._update_title()
                self._update_status()
            except Exception as e:
                eg.popup_error(f'ファイルを開けませんでした: {str(e)}')
    
    def save_file(self):
        """ファイルを保存"""
        if self.current_file:
            try:
                content = self.window['-TEXT-'].get()
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.modified = False
                self._update_title()
                return True
            except Exception as e:
                eg.popup_error(f'ファイルを保存できませんでした: {str(e)}')
                return False
        else:
            return self.save_file_as()
    
    def save_file_as(self):
        """名前を付けて保存"""
        filename = filedialog.asksaveasfilename(
            title='名前を付けて保存',
            defaultextension='.txt',
            filetypes=[('テキストファイル', '*.txt'), ('すべてのファイル', '*.*')]
        )
        
        if filename:
            self.current_file = filename
            return self.save_file()
        return False
    
    def undo(self):
        """元に戻す"""
        try:
            self.window['-TEXT-'].widget.edit_undo()
        except:
            pass
    
    def cut(self):
        """切り取り"""
        try:
            self.window['-TEXT-'].widget.event_generate("<<Cut>>")
        except:
            pass
    
    def copy(self):
        """コピー"""
        try:
            self.window['-TEXT-'].widget.event_generate("<<Copy>>")
        except:
            pass
    
    def paste(self):
        """貼り付け"""
        try:
            self.window['-TEXT-'].widget.event_generate("<<Paste>>")
        except:
            pass
    
    def select_all(self):
        """すべて選択"""
        try:
            self.window['-TEXT-'].widget.tag_add('sel', '1.0', 'end')
        except:
            pass
    
    def about(self):
        """バージョン情報"""
        eg.popup('TkEasyGUIメモ帳\nバージョン 1.0\n\nシンプルなテキストエディタ', title='バージョン情報')
    
    def run(self):
        """メインループ"""
        while True:
            event, values = self.window.read()
            
            if event in (eg.WIN_CLOSED, '終了(&X)'):
                if self.modified:
                    response = eg.popup_yes_no('変更を保存しますか？', title='確認')
                    if response == 'Yes':
                        if not self.save_file():
                            continue
                break
            
            # メニューイベント
            if event == '新規作成(&N)':
                self.new_file()
            elif event == '開く(&O)':
                self.open_file()
            elif event == '保存(&S)':
                self.save_file()
            elif event == '名前を付けて保存(&A)':
                self.save_file_as()
            elif event == '元に戻す(&U)':
                self.undo()
            elif event == '切り取り(&T)':
                self.cut()
            elif event == 'コピー(&C)':
                self.copy()
            elif event == '貼り付け(&P)':
                self.paste()
            elif event == 'すべて選択(&A)':
                self.select_all()
            elif event == 'バージョン情報(&A)':
                self.about()
        
        self.window.close()


if __name__ == '__main__':
    app = Notepad()
    app.run()

