import flet as ft
from asyncio import sleep
from pytonconnect import TonConnect

async def main(page: ft.Page):
    connector = TonConnect(manifest_url = 'https://raw.githubusercontent.com/artemshten/packetClicker/main/tonconnect-manifest.json')
    is_connected = await connector.restore_connection()
    print('is_connected:', is_connected)
    wallets_list = TonConnect.get_wallets()
    generated_url = await connector.connect(wallets_list[1])
    print('generated_url:', generated_url)
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
    if is_connected == False:
        ton_connect = ft.FilledButton(url=generated_url,
                                      content=ft.Text('Connect Tonkeeper', size=17, color=ft.colors.WHITE),
                                      style=ft.ButtonStyle(bgcolor='#0098ea'))
    else:
        ton_connect = ft.FilledButton(content=ft.Text('Connected', size=50, color=ft.colors.WHITE), style=ft.ButtonStyle(bgcolor='#0098ea'), disabled=True)
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
