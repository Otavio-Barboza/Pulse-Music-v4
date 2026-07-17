from core.services.auth.google_login_auth import login_google
from ui.others.colors import color
import asyncio
import flet as ft

async def main(page: ft.Page):
    async def login(click):
        # await login_google()
        print('logando')
        
        await asyncio.sleep(2.5)

        overlay_login.opacity = 0
        overlay_login.update()
        await asyncio.sleep(2.5)

    page.overlay.append(
        overlay_login := ft.Container(
            expand = True,
            bgcolor = color.preto3,
            opacity = 1,
            animate_opacity = ft.Animation(
                duration = 1000,
                curve = ft.AnimationCurve.EASE_OUT
            ),

            content = ft.Column(
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Row(expand_loose = True, height = 0),
                    ft.Text(
                        value = 'Fazer login com o google',
                        size = 30,
                        weight = ft.FontWeight.BOLD
                    ),
                    ft.TextButton(
                        text = 'Fazer Login',
                        icon = ft.Icons.LOGIN_ROUNDED,
                        on_click = login,
                        width = 200,
                        height = 50,
                        style = ft.ButtonStyle(
                            padding = ft.padding.all(20),
                            icon_size = 18,
                            alignment = ft.alignment.center,
                            animation_duration = 1000,
                            
                            color = {
                                ft.ControlState.DEFAULT : ft.Colors.WHITE,
                                ft.ControlState.HOVERED : ft.Colors.BLACK
                            },
                            overlay_color = {
                                ft.ControlState.HOVERED : ft.Colors.GREY_100
                            },
                            text_style = ft.TextStyle(
                                size = 20,
                                weight = ft.FontWeight.W_500
                            )
                        ) 
                    )
                ]
            )
        )
    )

    page.add(ft.Container(expand=True))

asyncio.run(
    ft.app_async(target = main)
)