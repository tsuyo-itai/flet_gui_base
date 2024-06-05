import flet as ft
from setting_parameter import FletSettingParameter

class FletApp(object):
    def __init__(self, page):
        self.page = page
        self.page.fonts = {
            "Corporate-Logo-Rounded": "/fonts/Corporate-Logo-Rounded-Bold-ver3.otf"
        }
        self.page.title = "Flet app title bar"
        ## 縦中央揃え
        # self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        ## 横中央揃え
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # スクロールを設定
        self.page.scroll = ft.ScrollMode.AUTO

        # 設定編集機能追加
        self.SettingParameterClass = FletSettingParameter(page)


    def page_header_create(self):
        # appbarの作成
        self.page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.COMPUTER_OUTLINED, color="white"),
            leading_width=40,
            title=ft.Text("Flet app", size=25, color=ft.colors.WHITE, font_family="Corporate-Logo-Rounded"),
            center_title=False,
            bgcolor=ft.colors.INDIGO_600,
            actions=[
                ft.IconButton(ft.icons.HOME, icon_color="white", on_click=self.home_icon_button_click),
                ft.IconButton(ft.icons.SETTINGS_OUTLINED, icon_color="white", on_click=self.SettingParameterClass.setting_icon_button_click),
            ],
        )

    # HOME画面描画関数 (再描画も)
    def home_window_create(self):
        # appbarの作成
        self.home_view_create()

    # 画面描画関数 (再描画も)
    def home_view_create(self):
        self.page_header_create()
        self.page.add(
            ft.Text("Welcome to Home View!!"),
        )

    # HOMEアイコン・ボタンをクリックした際のハンドラー
    def home_icon_button_click(self, e):
        self.page.clean()
        self.home_view_create()

def main(page: ft.Page):
    flet_app = FletApp(page)

    flet_app.home_window_create()


if __name__ == "__main__":

    if True:
        # GUIアプリとして起動
        ft.app(
            target=main,
            assets_dir="assets"
        )
    else:
        # WEBブラウザで起動
        ft.app(
            target=main,
            view=ft.WEB_BROWSER,
            port=8552,
            assets_dir="assets"
        )