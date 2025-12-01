import reflex as rx
from app.components.layout import dashboard_layout
from app.states.leave_state import LeaveState
from app.states.auth_state import AuthState
from app.models import LeaveRequest


def leave_status_badge(status: str) -> rx.Component:
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


def leave_request_card(req: LeaveRequest) -> rx.Component:
    is_manager_or_admin = (AuthState.user_role == "Admin") | (
        AuthState.user_role == "Manager"
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        f"{req.leave_type} Leave",
                        class_name="text-lg font-medium text-gray-900",
                    ),
                    rx.el.p(
                        f"{req.days_count} Days", class_name="text-sm text-gray-500"
                    ),
                    class_name="flex justify-between items-start",
                ),
                rx.el.div(
                    rx.el.p(
                        f"From: {req.start_date}", class_name="text-sm text-gray-600"
                    ),
                    rx.el.p(f"To: {req.end_date}", class_name="text-sm text-gray-600"),
                    class_name="mt-2 grid grid-cols-2 gap-4",
                ),
                rx.el.p(
                    req.reason,
                    class_name="mt-3 text-sm text-gray-700 italic bg-gray-50 p-2 rounded",
                ),
                rx.cond(
                    req.manager_comment != "",
                    rx.el.div(
                        rx.el.p(
                            "Manager Comment:",
                            class_name="text-xs font-semibold text-gray-500",
                        ),
                        rx.el.p(
                            req.manager_comment, class_name="text-xs text-gray-600"
                        ),
                        class_name="mt-2 border-t pt-2",
                    ),
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                leave_status_badge(req.status),
                rx.el.p(
                    f"By: {req.employee_username}",
                    class_name="text-xs text-gray-400 mt-2 text-right",
                ),
                rx.cond(
                    is_manager_or_admin & (req.status == "Pending"),
                    rx.el.div(
                        rx.el.input(
                            placeholder="Reason (optional)",
                            on_change=lambda val: LeaveState.set_manager_comment(
                                req.id, val
                            ),
                            class_name="w-full mt-2 text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:border-blue-500",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Approve",
                                on_click=lambda: LeaveState.approve_request(req.id),
                                class_name="bg-green-600 text-white px-3 py-1 rounded text-xs hover:bg-green-700",
                            ),
                            rx.el.button(
                                "Reject",
                                on_click=lambda: LeaveState.reject_request(req.id),
                                class_name="bg-red-600 text-white px-3 py-1 rounded text-xs hover:bg-red-700",
                            ),
                            class_name="flex space-x-2 mt-2 justify-end",
                        ),
                        class_name="mt-4 border-t border-gray-100 pt-2",
                    ),
                ),
                class_name="flex flex-col items-end ml-4 min-w-[120px]",
            ),
            class_name="flex justify-between",
        ),
        class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow",
    )


def leave_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "New Leave Request", class_name="text-lg font-semibold text-gray-900 mb-4"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Leave Type",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.select(
                        rx.el.option("Annual Leave", value="Annual"),
                        rx.el.option("Sick Leave", value="Sick"),
                        rx.el.option("Personal Leave", value="Personal"),
                        rx.el.option("Unpaid Leave", value="Unpaid"),
                        name="leave_type",
                        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md border",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "Start Date",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        type="date",
                        name="start_date",
                        default_value=LeaveState.start_date,
                        class_name="mt-1 block w-full shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border-gray-300 rounded-md border px-3 py-2",
                    ),
                ),
                rx.el.div(
                    rx.el.label(
                        "End Date", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="date",
                        name="end_date",
                        default_value=LeaveState.end_date,
                        class_name="mt-1 block w-full shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border-gray-300 rounded-md border px-3 py-2",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Reason", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.textarea(
                    name="reason",
                    rows=3,
                    required=True,
                    placeholder="Please provide a reason for your leave request...",
                    class_name="mt-1 block w-full shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm border-gray-300 rounded-md border px-3 py-2",
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Submit Request",
                type="submit",
                class_name="w-full inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
            ),
            on_submit=LeaveState.submit_request,
        ),
        class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8",
    )


def leave_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Leave Requests", class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(
                "Submit and manage your leave requests.",
                class_name="mt-1 text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        leave_form(),
        rx.el.div(
            rx.el.h2(
                "Request History", class_name="text-lg font-semibold text-gray-900 mb-4"
            ),
            rx.el.div(
                rx.cond(
                    LeaveState.requests,
                    rx.el.div(
                        rx.foreach(LeaveState.requests, leave_request_card),
                        class_name="space-y-4",
                    ),
                    rx.el.p(
                        "No leave requests found.",
                        class_name="text-gray-500 italic text-center py-8 bg-white rounded-lg border border-dashed border-gray-300",
                    ),
                )
            ),
        ),
    )


def leave_page() -> rx.Component:
    return dashboard_layout(leave_content())