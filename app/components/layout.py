import reflex as rx
from app.components.sidebar import sidebar
from app.components.navbar import navbar


def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.div(
            navbar(),
            rx.el.main(
                content,
                class_name="flex-1 overflow-auto p-6 bg-slate-50 bg-pattern-grid min-h-[calc(100vh-4rem)]",
            ),
            class_name="flex flex-col flex-1 min-w-0 h-screen overflow-hidden",
        ),
        class_name="flex h-screen w-full bg-slate-50",
    )