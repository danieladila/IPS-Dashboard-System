import reflex as rx
from app.components.layout import dashboard_layout
from app.states.request_state import RequestState
from app.states.auth_state import AuthState
from app.models import GeneralRequest


def request_status_badge(status: str) -> rx.Component:
    return rx.match(
        status,
        (
            "Approved",
            rx.el.span(
                "Approved",
                class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
            ),
        ),
        (
            "Rejected",
            rx.el.span(
                "Rejected",
                class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800",
            ),
        ),
        rx.el.span(
            "Pending",
            class_name="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800",
        ),
    )


def request_card(req: GeneralRequest) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(req.title, class_name="text-lg font-medium text-gray-900"),
                    rx.el.span(
                        req.type,
                        class_name="ml-2 px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.p(
                    f"Amount: ${req.amount}",
                    class_name="text-sm font-semibold text-gray-700 mt-1",
                ),
                rx.el.p(req.description, class_name="mt-2 text-sm text-gray-600"),
                rx.el.div(
                    rx.el.p(
                        f"Submitted by: {req.submitted_by}",
                        class_name="text-xs text-gray-500",
                    ),
                    rx.el.p(
                        f"Date: {req.submitted_date}",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="mt-3 flex justify-between items-center",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                request_status_badge(req.status),
                rx.cond(
                    req.status == "Pending",
                    rx.cond(
                        (AuthState.user_role == "Admin")
                        | (AuthState.user_role == "Manager"),
                        rx.el.div(
                            rx.el.button(
                                "Approve",
                                on_click=lambda: RequestState.approve_request(req.id),
                                class_name="bg-green-600 text-white px-3 py-1 rounded text-xs hover:bg-green-700 mr-2",
                            ),
                            rx.el.button(
                                "Reject",
                                on_click=lambda: RequestState.reject_request(req.id),
                                class_name="bg-red-600 text-white px-3 py-1 rounded text-xs hover:bg-red-700",
                            ),
                            class_name="mt-4 flex justify-end",
                        ),
                    ),
                ),
                rx.cond(
                    req.approver != "",
                    rx.el.p(
                        f"Action by: {req.approver}",
                        class_name="text-xs text-gray-500 mt-2 text-right",
                    ),
                ),
                class_name="ml-4 flex flex-col items-end justify-between",
            ),
            class_name="flex justify-between",
        ),
        class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-all",
    )


def new_request_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2("New Request", class_name="text-lg font-semibold text-gray-900 mb-4"),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Title", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        name="title",
                        required=True,
                        placeholder="e.g., New Laptop Monitor",
                        class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    ),
                    class_name="col-span-6 sm:col-span-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Type", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.select(
                        rx.el.option("Expense", value="Expense"),
                        rx.el.option("Purchase", value="Purchase"),
                        rx.el.option("Resource", value="Resource"),
                        rx.el.option("Other", value="Other"),
                        name="type",
                        class_name="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    ),
                    class_name="col-span-6 sm:col-span-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "Amount ($)",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        type="number",
                        name="amount",
                        placeholder="0.00",
                        step="0.01",
                        class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    ),
                    class_name="col-span-6 sm:col-span-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "Priority", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.select(
                        rx.el.option("Low", value="Low"),
                        rx.el.option("Medium", value="Medium"),
                        rx.el.option("High", value="High"),
                        name="priority",
                        class_name="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    ),
                    class_name="col-span-6 sm:col-span-3",
                ),
                class_name="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6 mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Description", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.textarea(
                    name="description",
                    rows=3,
                    required=True,
                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                class_name="mb-6",
            ),
            rx.el.button(
                "Submit Request",
                type="submit",
                class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
            ),
            on_submit=RequestState.submit_request,
        ),
        class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8",
    )


def requests_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "General Requests", class_name="text-2xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Manage expense, purchase, and resource requests.",
                    class_name="mt-1 text-sm text-gray-500",
                ),
                class_name="mb-8",
            ),
            new_request_form(),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Request History",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option("All Status", value="All"),
                            rx.el.option("Pending", value="Pending"),
                            rx.el.option("Approved", value="Approved"),
                            rx.el.option("Rejected", value="Rejected"),
                            on_change=RequestState.set_status_filter,
                            class_name="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md border mr-4",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.div(
                    rx.cond(
                        RequestState.filtered_requests,
                        rx.el.div(
                            rx.foreach(RequestState.filtered_requests, request_card),
                            class_name="space-y-4",
                        ),
                        rx.el.div(
                            "No requests found matching filters.",
                            class_name="text-center py-12 text-gray-500 bg-white rounded-lg border border-dashed border-gray-300",
                        ),
                    )
                ),
            ),
        )
    )