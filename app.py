import flet as ft
from asyncio import sleep
from pytonconnect import TonConnect
from pytonconnect.exceptions import TonConnectError
from tonsdk.utils import Address

async def main(page: ft.Page):
    def status_changed(wallet):
        result = connector.wait_for_connection()
        if isinstance(result, TonConnectError):
            print('error:', result)
        else:
            if connector.connected and connector.account.address:
                global adress
                adress = Address(connector.account.address).to_string(True, True)
                print('Connected with address:', adress)
                unsubscribe()

    async def disconnect_wallet(e):
        cupertino_alert_dialog.open = False
        await connector.disconnect()
        await e.control.page.update_async()

    async def dismiss_dialog(e):
        cupertino_alert_dialog.open = False
        await e.control.page.update_async()

    async def open_dlg(e):
        e.control.page.dialog = cupertino_alert_dialog
        cupertino_alert_dialog.open = True
        await e.control.page.update_async()

    connector = TonConnect(manifest_url='https://raw.githubusercontent.com/artemshten/packetClicker/main/tonconnect-manifest.json')
    is_connected = await connector.restore_connection()
    page.title = 'Packet Cliker'
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = '#000000'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {"Calibri" : "fonts/calibribold.ttf"}
    page.theme = ft.Theme(font_family="Calibri")

    async def score_up(event: ft.ContainerTapEvent):
        score.data += 1
        score.value = str(score.data)

        image.scale = 0.95

        score_counter.opacity = 0
        score_counter.value = '+1'
        score_counter.right = 0
        score_counter.left = 150
        score_counter.top = 0
        score_counter.bottom = 0

        progress_bar.value += (1/100)

        if score.data % 100 == 0:
            page.snack_bar = ft.SnackBar(content=ft.Text(value='+100',
                                                         size=20,
                                                         color='#ffffff',
                                                         text_align=ft.TextAlign.CENTER), bgcolor='#cccccc')
            page.snack_bar.open = True
            progress_bar.value = 0

        await page.update_async()
        await sleep(0.1)
        image.scale = 1
        score_counter.opacity = 0
        await page.update_async()

    score = ft.Text(value='0', size=70, data=0)
    score_counter = ft.Text(size=50, animate_opacity=ft.Animation(duration=200, curve=ft.AnimationCurve.BOUNCE_IN))
    is_connected = await connector.restore_connection()
    if is_connected == False:
        connector = TonConnect(manifest_url = 'https://raw.githubusercontent.com/artemshten/packetClicker/main/tonconnect-manifest.json')
        wallets_list = TonConnect.get_wallets()
        generated_url = await connector.connect(wallets_list[1])
        unsubscribe = connector.on_status_change(status_changed)
        ton_connect = ft.FilledButton(url=generated_url,
                                      content=ft.Text('Connect Tonkeeper', size=17, color=ft.colors.WHITE),
                                      style=ft.ButtonStyle(bgcolor='#0098ea'))
        ton_connect = ft.Container(content=ton_connect, margin=ft.Margin(180, 0, 0, 100))
    else:
        global adress
        lst = [i for i in adress if adress]
        count = len(lst)
        formatted_adress = lst[0] + lst[1] + lst[2] + lst[3] + '...' + lst[count-4] + lst[count-3] + lst[count-2] + lst[count-1]
        cupertino_alert_dialog = ft.CupertinoAlertDialog(
            title=ft.Text("Сonfirmation"),
            content=ft.Text("Do you want to disconnect wallet?"),
            actions=[
                ft.CupertinoDialogAction(
                    "Yes", is_destructive_action=True, on_click=disconnect_wallet
                ),
                ft.CupertinoDialogAction(text="No", on_click=dismiss_dialog),
            ],
        )
        ton_connect_butt = ft.FilledButton(content=ft.Text(formatted_adress, size=17, color=ft.colors.WHITE), style=ft.ButtonStyle(bgcolor='#0098ea'), on_click=open_dlg)
        ton_connect = ft.Container(content=ton_connect_butt, margin=ft.Margin(230,0,0,100))

    image = ft.Image(src='packet.png',
                     fit=ft.ImageFit.CONTAIN,
                     animate_scale=ft.Animation(duration=200, curve=ft.AnimationCurve.EASE))

    progress_bar = ft.ProgressBar(value=0,
                                  width=page.width-100,
                                  height=20,
                                  color='#ffffff',
                                  bgcolor='#cccccc'
                                  )

    await page.add_async(ton_connect,
                         score,
                         ft.Container(content=ft.Stack(controls=[image, score_counter]), on_click=score_up, margin=ft.Margin(0,0,0,20)),
                         ft.Container(content=progress_bar, border_radius=ft.BorderRadius(10,10,10,10)),
                         )

if __name__ == '__main__':
    ft.app(target=main, view=None, port=8000)
