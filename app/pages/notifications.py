import reflex as rx
from app.components.layout import dashboard_layout
from app.states.notification_state import NotificationState
from app.models import Notification


def notification_item(notif: Notification) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                rx.match(
                    notif.type,
                    ("Success", "check-circle"),
                    ("Error", "alert-circle"),
                    ("Warning", "alert-triangle"),
                    "info",
                ),
                class_name=rx.match(
                    notif.type,
                    ("Success", "h-6 w-6 text-green-500"),
                    ("Error", "h-6 w-6 text-red-500"),
                    ("Warning", "h-6 w-6 text-yellow-500"),
                    "h-6 w-6 text-blue-500",
                ),
            ),
            class_name="mr-4 flex-shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h4(notif.title, class_name="text-sm font-medium text-gray-900"),
                rx.el.span(notif.created_at, class_name="text-xs text-gray-500"),
                class_name="flex justify-between items-start",
            ),
            rx.el.p(notif.message, class_name="mt-1 text-sm text-gray-600"),
            rx.cond(
                ~notif.is_read,
                rx.el.button(
                    "Mark as read",
                    on_click=lambda: NotificationState.mark_as_read(notif.id),
                    class_name="mt-2 text-xs text-blue-600 hover:text-blue-800 font-medium",
                ),
            ),
            class_name="flex-1",
        ),
        class_name=rx.cond(
            notif.is_read,
            "flex p-4 bg-white border-b border-gray-200 opacity-75",
            "flex p-4 bg-blue-50 border-b border-blue-100",
        ),
    )


def notifications_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Notifications", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.div(
                    rx.el.button(
                        "Mark all as read",
                        on_click=NotificationState.mark_all_as_read,
                        class_name="text-sm text-blue-600 hover:text-blue-800 mr-4",
                    ),
                    rx.el.button(
                        "Clear all",
                        on_click=NotificationState.clear_notifications,
                        class_name="text-sm text-gray-600 hover:text-gray-800",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            rx.el.div(
                rx.cond(
                    NotificationState.current_user_notifications_list,
                    rx.el.div(
                        rx.foreach(
                            NotificationState.current_user_notifications_list,
                            notification_item,
                        ),
                        class_name="bg-white shadow overflow-hidden sm:rounded-md",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "bell-off", class_name="h-12 w-12 text-gray-300 mb-4"
                            ),
                            rx.el.p(
                                "No notifications",
                                class_name="text-lg font-medium text-gray-900",
                            ),
                            rx.el.p(
                                "You're all caught up!", class_name="text-gray-500"
                            ),
                            class_name="flex flex-col items-center justify-center py-12",
                        ),
                        class_name="bg-white shadow sm:rounded-lg",
                    ),
                )
            ),
        )
    )