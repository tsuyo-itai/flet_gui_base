import flet as ft
import common as CM
import time

SETTING_PARAMETER_DICT = {
    # "項目名": ["setting.iniのセクション", "setting.iniのキー"]
    "アカウントID": ["ACCOUNT ID", "email"],
    "パスワード1": ["PASS WORD", "password1"],
    "パスワード2": ["PASS WORD", "password2"],
}

SETTING_WARNING_DICT = {
    "アカウントID": "メールアドレス形式で入力してください.",
    "パスワード1": "8文字以上で入力してください.",
    "パスワード2": "",
}

SETTING_FILE_PATH = 'parameter/setting.ini'

class FletSettingParameter(object):
    def __init__(self, page):
        self.page = page

        # 設定ファイルを読み込み
        self.config = CM.set_config(SETTING_FILE_PATH)

    # 設定アイコン・ボタンをクリックした際のハンドラー
    def setting_icon_button_click(self, e):
        self.page.clean()
        self.setting_view_create()

    # 画面描画関数 (再描画も)
    def setting_view_create(self):
        setting_view_title = self.create_setting_parameter_title_view()
        if self.check_exist_inifile():
            setting_view_table = self.create_setting_parameter_table_view()
        else:
            setting_view_table = self.create_setting_parameter_not_exist_view()

        self.page.add(
            setting_view_title,
            setting_view_table
        )


    # 設定情報画面ヘッダービュー作成
    def create_setting_parameter_title_view(self):
        ret_view = ft.ResponsiveRow(
            [
                ft.Container(
                    ft.Text("設定情報", size=20, font_family="Corporate-Logo-Rounded"),
                    # col={"sm": 6, "md": 4, "xl": 2},
                    col={"sm": 12, "md": 12, "xl": 12},
                    alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        return ret_view

    # 設定ファイルチェックNGビュー作成
    def create_setting_parameter_not_exist_view(self):
        ret_view = ft.Text("設定ファイルが存在しません")
        return ret_view

    # 設定情報画面テーブルビュー作成
    def create_setting_parameter_table_view(self):
        ret_view = ft.ResponsiveRow(
            [
                ft.Container(
                    ft.DataTable(
                        column_spacing=20,
                        columns=[
                            ft.DataColumn(ft.Text("設定内容")),
                            ft.DataColumn(ft.Text("設定値")),
                            ft.DataColumn(ft.Text("")),
                        ],
                        rows=[
                            #* わかりにくいがリスト内包表記でリストを展開して返している
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(SETTING_PARAMETER)),
                                    ft.DataCell(ft.Text(self.config[SETTING_PARAMETER_DICT[SETTING_PARAMETER][0]][SETTING_PARAMETER_DICT[SETTING_PARAMETER][1]])) if self.config[SETTING_PARAMETER_DICT[SETTING_PARAMETER][0]][SETTING_PARAMETER_DICT[SETTING_PARAMETER][1]] != "" else ft.DataCell(ft.Text("設定が未入力です", color="red")),
                                    ft.DataCell(ft.TextButton("編集", icon=ft.icons.EDIT, icon_color="blue400", data=[SETTING_PARAMETER, SETTING_PARAMETER_DICT[SETTING_PARAMETER][0], SETTING_PARAMETER_DICT[SETTING_PARAMETER][1]], on_click=self.setting_dlg_modal))
                                ]
                            )
                            for SETTING_PARAMETER in SETTING_PARAMETER_DICT
                        ],
                    ),
                    col={"sm": 12, "md": 8, "xl": 6},
                    # alignment=ft.alignment.center
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        return ret_view
    
    # 設定編集モーダルウィンドウ
    def setting_dlg_modal(self, e):
        # 設定するパラメータ名
        setting_param_name = e.control.data[0]
        # 設定読み込むパラメータセクション
        setting_param_section = e.control.data[1]
        # 設定読み込むパラメータ変数
        setting_param_value = e.control.data[2]

        modal_content_message = SETTING_WARNING_DICT[setting_param_name]

        # 設定値フィールド (モーダルダイアログから値を参照できるようクラス変数にインスタンスを入れる)
        self.setting_value_field = ft.TextField(label=setting_param_name, value=self.config[setting_param_section][setting_param_value])

        # 選択時のモーダルダイアログ
        self.dlg_modal = ft.AlertDialog(
            modal=True, # モーダル外のクリックで閉じない
            title=ft.Text(setting_param_name),
            content=ft.Text(modal_content_message),
            actions=[
                self.setting_value_field,
                ft.Row(
                    [
                        ft.Container(
                            content=ft.ElevatedButton(" 保存 ", icon=ft.icons.SAVE, color="white", bgcolor="blue", on_click=self.setting_save, data=[setting_param_section, setting_param_value]),
                            margin=ft.margin.only(top=25),  # 上方向のみマージンを入れる
                            # padding=10,
                            alignment=ft.alignment.center_left
                        ),

                        ft.Container(
                            content=ft.ElevatedButton(" 戻る ", icon=ft.icons.CANCEL, color="white", bgcolor="red", on_click=self.setting_cancel_button_click),
                            margin=ft.margin.only(top=25),  # 上方向のみマージンを入れる
                            # padding=10,
                            alignment=ft.alignment.center_right
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            on_dismiss=lambda e: print(f'{setting_param_name} edit cancel!!'),
        )

        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

    # モーダルウィンドウ閉じる (閉じる・いいえ押下時)
    def setting_cancel_button_click(self, e):
        self.modal_close()

    # モーダルウィンドウ閉じる (閉じる・いいえ押下時)
    def modal_close(self):
        # モーダルダイアログを閉じる
        self.dlg_modal.open = False
        self.page.update()
        # _Control__attrsのopenが存在しかつ要素が空ではない場合
        if hasattr(self.dlg_modal, '_Control__attrs') and 'open' in self.dlg_modal._Control__attrs and self.dlg_modal._Control__attrs['open']:
            # 最大1秒待ち (キモいけどsleepないとうまくいかない)
            for _ in range(10):
                # ダイアログが閉じられたら文字列の"false"になる
                if self.dlg_modal._Control__attrs['open'][0] == 'false':
                    break
                time.sleep(0.1)
        else:
            # デフォルト0.5秒待ち
            time.sleep(0.5)

    # 設定ファイル保存・画面反映
    def setting_save(self, e):
        # 設定するパラメータセクション
        save_section = e.control.data[0]
        # 設定するパラメータ変数
        save_key = e.control.data[1]

        # バリデーション
        ret = self.parameter_validate(save_section, save_key)

        if ret is False:
            # 赤文字で入力規則を強調
            self.dlg_modal.content.color="red"
            self.page.update()
            return

        self.config[save_section][save_key] = self.setting_value_field.value

        with open(CM.get_resource_path(SETTING_FILE_PATH), 'w') as configfile:
            # 指定したconfigファイルを書き込み
            self.config.write(configfile)
            print(f"{save_section} {save_key} が更新されました。")

        # モーダルウィンドウ閉じる
        self.modal_close()

        # Viewを再作成
        self.page.clean()
        self.setting_view_create()
        self.page.update()

    # 設定バリデーション
    def parameter_validate(self, save_section, save_key) -> bool:
        ret = True
        if save_section == "ACCOUNT ID" and save_key == "email":
            if "@" not in self.setting_value_field.value:
                self.setting_value_field.value = ""
                ret = False
        
        if save_section == "PASS WORD" and save_key == "password1":
            if len(self.setting_value_field.value) < 8:
                self.setting_value_field.value = ""
                ret = False

        return ret

    # iniファイルチェック (起動時にコール)
    def check_exist_inifile(self):
        if self.config is None:
            return False
        else:
            return True

    # iniファイルから設定値を返す
    def get_setting_param(self, sectionction, key):
        return self.config[sectionction][key]