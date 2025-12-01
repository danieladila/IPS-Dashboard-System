import reflex as rx
from app.components.layout import dashboard_layout
from app.states.document_state import DocumentState
from app.states.auth_state import AuthState
from app.models import Document


def status_badge(status: str) -> rx.Component:
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


def document_row(doc: Document) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon("file-text", class_name="h-5 w-5 text-gray-400 mr-3"),
                rx.el.div(
                    rx.el.p(doc.title, class_name="text-sm font-medium text-gray-900"),
                    rx.el.p(doc.file_type, class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(doc.uploaded_by, class_name="text-sm text-gray-900"),
                rx.el.p(doc.upload_date, class_name="text-xs text-gray-500"),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(status_badge(doc.status), class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            rx.cond(
                (AuthState.user_role == "Admin") | (AuthState.user_role == "Manager"),
                rx.cond(
                    doc.status == "Pending",
                    rx.el.div(
                        rx.el.button(
                            rx.icon("check", class_name="h-4 w-4"),
                            on_click=lambda: DocumentState.approve_document(doc.id),
                            class_name="text-green-600 hover:text-green-900 mr-3 p-1 hover:bg-green-50 rounded-full transition-colors",
                            title="Approve",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="h-4 w-4"),
                            on_click=lambda: DocumentState.reject_document(doc.id),
                            class_name="text-red-600 hover:text-red-900 p-1 hover:bg-red-50 rounded-full transition-colors",
                            title="Reject",
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.span(
                        rx.cond(doc.reviewer != "", f"Reviewed by {doc.reviewer}", "-"),
                        class_name="text-xs text-gray-500",
                    ),
                ),
                rx.el.a(
                    rx.icon(
                        "download",
                        class_name="h-4 w-4 text-blue-600 hover:text-blue-800",
                    ),
                    href=rx.get_upload_url(doc.file_path),
                    target="_blank",
                    class_name="inline-flex items-center px-2 py-1 rounded hover:bg-blue-50",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def upload_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.upload.root(
                rx.el.div(
                    rx.icon("cloud-upload", class_name="h-12 w-12 text-blue-500 mb-4"),
                    rx.el.p(
                        "Drag and drop files here or click to select",
                        class_name="text-lg font-medium text-gray-700 mb-1",
                    ),
                    rx.el.p(
                        "Supported formats: PDF, DOC, DOCX, XLS",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-blue-200 rounded-xl bg-blue-50 hover:bg-blue-100 transition-colors cursor-pointer",
                ),
                id="doc_upload",
                multiple=True,
                accept={
                    "application/pdf": [".pdf"],
                    "application/msword": [".doc"],
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
                        ".docx"
                    ],
                    "application/vnd.ms-excel": [".xls"],
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
                        ".xlsx"
                    ],
                },
                class_name="w-full",
            ),
            rx.el.div(
                rx.foreach(
                    rx.selected_files("doc_upload"),
                    lambda file: rx.el.div(
                        rx.icon("file", class_name="h-4 w-4 mr-2 text-blue-600"),
                        rx.el.span(file, class_name="text-sm text-gray-700 truncate"),
                        class_name="flex items-center p-2 bg-white border border-gray-200 rounded-md",
                    ),
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-4",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        DocumentState.is_uploading,
                        rx.el.span("Uploading...", class_name="flex items-center"),
                        rx.el.span("Upload Files", class_name="flex items-center"),
                    ),
                    on_click=DocumentState.handle_upload(
                        rx.upload_files(upload_id="doc_upload")
                    ),
                    disabled=DocumentState.is_uploading,
                    class_name="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                class_name="flex justify-end",
            ),
            class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8",
        ),
        class_name="w-full",
    )


def documents_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Document Management", class_name="text-2xl font-bold text-gray-900"
            ),
            rx.el.p(
                "Upload and manage your documents here.",
                class_name="mt-1 text-sm text-gray-500",
            ),
            class_name="mb-8",
        ),
        upload_section(),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Document List", class_name="text-lg font-semibold text-gray-900"
                ),
                rx.el.div(
                    rx.el.button(
                        "All",
                        on_click=lambda: DocumentState.set_filter("All"),
                        class_name=rx.cond(
                            DocumentState.current_filter == "All",
                            "px-3 py-1 rounded-full text-sm font-medium bg-gray-900 text-white",
                            "px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-600 hover:bg-gray-200",
                        ),
                    ),
                    rx.el.button(
                        "Pending",
                        on_click=lambda: DocumentState.set_filter("Pending"),
                        class_name=rx.cond(
                            DocumentState.current_filter == "Pending",
                            "px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800",
                            "px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-600 hover:bg-gray-200",
                        ),
                    ),
                    rx.el.button(
                        "Approved",
                        on_click=lambda: DocumentState.set_filter("Approved"),
                        class_name=rx.cond(
                            DocumentState.current_filter == "Approved",
                            "px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800",
                            "px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-600 hover:bg-gray-200",
                        ),
                    ),
                    class_name="flex space-x-2",
                ),
                class_name="flex items-center justify-between mb-4",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Document",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Uploaded By",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider",
                            ),
                        ),
                        class_name="bg-gray-50",
                    ),
                    rx.el.tbody(
                        rx.foreach(DocumentState.filtered_documents, document_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="overflow-x-auto border border-gray-200 rounded-lg shadow-sm",
            ),
            class_name="bg-white p-6 rounded-lg shadow-sm border border-gray-200",
        ),
    )


def documents_page() -> rx.Component:
    return dashboard_layout(documents_content())