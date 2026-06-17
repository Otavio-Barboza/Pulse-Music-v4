import flet as ft

def main(page : ft.Page):
    page.padding = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    page.add(
        ft.Column(
            expand = True,
            scroll=ft.ScrollMode.ALWAYS,
            controls = [
                ft.ResponsiveRow(
                    spacing=0,
                    controls = [
                        ft.Container(
                            col={'sm' : 6, 'xs' : 12}, 
                            # bgcolor=ft.Colors.YELLOW,
                            height=1080,
                            
                            content=ft.GridView(
                                max_extent=50,
                                controls = [
                                    ft.Container(
                                        width=50,
                                        height=50,
                                        bgcolor = ft.Colors.BLACK,
                                        content = ft.Text(value=i, color=ft.Colors.WHITE)
                                    ) for i in range(1, 201)
                                ]
                            ),
                        ),
                       
                        ft.Container(
                            col={'sm' : 6, 'xs' : 12}, 
                            # bgcolor=ft.Colors.RED,
                            expand = True,
                            height=1080,
                            
                            content=ft.Tabs(
                                tabs=[
                                    ft.Tab(
                                        text='a',
                                        content=ft.GridView(
                                            max_extent=50,
                                            controls = [
                                                ft.Container(
                                                    width=50,
                                                    height=50,
                                                    bgcolor = ft.Colors.ORANGE,
                                                    content = ft.Text(value=i, color=ft.Colors.WHITE)
                                                ) for i in range(1, 201)
                                            ]
                                        ),
                                    ),
                                    ft.Tab(
                                        text='b',
                                        content=ft.GridView(
                                            max_extent=50,
                                            controls = [
                                                ft.Container(
                                                    width=50,
                                                    height=50,
                                                    bgcolor = ft.Colors.BLUE,
                                                    content = ft.Text(value=i, color=ft.Colors.WHITE)
                                                ) for i in range(1, 201)
                                            ]
                                        ),
                                    )
                                ]
                            )
                        )
                    ]
                )
            ]
        )
    )
    
ft.app(
    target=main
)