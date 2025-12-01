import reflex as rx
from app.components.layout import dashboard_layout
from app.states.workflow_state import WorkflowState
from app.models import WorkflowTemplate


def workflow_card(wf: WorkflowTemplate) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(wf.name, class_name="text-lg font-medium text-gray-900"),
            rx.el.p(wf.description, class_name="text-sm text-gray-500 mt-1"),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.h4(
                "Approval Stages:",
                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    wf.stages,
                    lambda stage, i: rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                i + 1, class_name="text-xs font-bold text-white"
                            ),
                            class_name="flex items-center justify-center w-5 h-5 rounded-full bg-blue-500 mr-2",
                        ),
                        rx.el.span(stage, class_name="text-sm text-gray-700"),
                        class_name="flex items-center mb-2",
                    ),
                ),
                class_name="pl-2",
            ),
            class_name="mb-4 bg-gray-50 p-3 rounded-md",
        ),
        rx.el.div(
            rx.el.span(
                f"Created by {wf.created_by} on {wf.created_date}",
                class_name="text-xs text-gray-400",
            ),
            rx.el.button(
                "Delete",
                on_click=lambda: WorkflowState.delete_workflow(wf.id),
                class_name="text-xs text-red-600 hover:text-red-800",
            ),
            class_name="flex justify-between items-center mt-auto pt-4 border-t border-gray-100",
        ),
        class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200 flex flex-col",
    )


def workflow_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Create New Workflow", class_name="text-lg font-semibold text-gray-900 mb-4"
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Workflow Name",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    name="name",
                    required=True,
                    placeholder="e.g., Capital Expenditure",
                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Description", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.textarea(
                    name="description",
                    rows=2,
                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Stages (comma separated roles)",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    name="stages",
                    placeholder="e.g., Manager, Finance, Admin",
                    class_name="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                ),
                rx.el.p(
                    "Define the sequence of approvals required.",
                    class_name="mt-1 text-xs text-gray-500",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    type="button",
                    on_click=WorkflowState.toggle_creating,
                    class_name="mr-3 inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                ),
                rx.el.button(
                    "Create Workflow",
                    type="submit",
                    class_name="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                ),
                class_name="flex justify-end",
            ),
            on_submit=WorkflowState.create_workflow,
        ),
        class_name="bg-gray-50 p-6 rounded-lg border border-gray-200 mb-8",
    )


def workflows_page() -> rx.Component:
    return dashboard_layout(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Workflow Configuration",
                    class_name="text-2xl font-bold text-gray-900",
                ),
                rx.el.button(
                    "+ New Workflow",
                    on_click=WorkflowState.toggle_creating,
                    class_name="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            rx.cond(WorkflowState.is_creating, workflow_form()),
            rx.el.div(
                rx.foreach(WorkflowState.workflows, workflow_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
            ),
        )
    )