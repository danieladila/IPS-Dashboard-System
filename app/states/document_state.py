import reflex as rx
import datetime
import uuid
from app.models import Document
from app.states.auth_state import AuthState
from app.services.telegram_service import TelegramService

MOCK_DOCUMENTS: list[Document] = []


class DocumentState(rx.State):
    documents: list[Document] = MOCK_DOCUMENTS
    is_uploading: bool = False
    current_filter: str = "All"

    @rx.var
    def filtered_documents(self) -> list[Document]:
        if self.current_filter == "All":
            return self.documents
        return [d for d in self.documents if d.status == self.current_filter]

    @rx.event
    def set_filter(self, status: str):
        self.current_filter = status

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the file upload."""
        if not files:
            return rx.toast.error("No files selected")
        user = await self.get_state(AuthState)
        if not user.user:
            return rx.toast.error("You must be logged in to upload files")
        self.is_uploading = True
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        for file in files:
            upload_data = await file.read()
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{unique_id}_{file.name}"
            file_path = upload_dir / filename
            with file_path.open("wb") as f:
                f.write(upload_data)
            file_ext = filename.split(".")[-1].upper()
            new_doc = Document(
                id=str(uuid.uuid4()),
                title=file.name,
                file_path=filename,
                file_type=file_ext,
                uploaded_by=user.user.username,
                upload_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                status="Pending",
            )
            self.documents.insert(0, new_doc)
            msg = f"📄 New Document Uploaded\nUser: {user.user.username}\nFile: {file.name}"
            if await TelegramService.send_message(msg):
                from app.states.notification_state import NotificationState

                notif_state = await self.get_state(NotificationState)
                notif_state.log_telegram_message(msg)
        self.is_uploading = False
        return rx.toast.success(f"Uploaded {len(files)} file(s)")

    @rx.event
    async def approve_document(self, doc_id: str):
        user = await self.get_state(AuthState)
        if user.user_role not in ["Admin", "Manager"]:
            return rx.toast.error("Unauthorized")
        for doc in self.documents:
            if doc.id == doc_id:
                doc.status = "Approved"
                doc.reviewer = user.user.username
                doc.review_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                msg = f"✅ Document Approved\nDocument: {doc.title}\nReviewed by: {user.user.username}"
                if await TelegramService.send_message(msg):
                    from app.states.notification_state import NotificationState

                    notif_state = await self.get_state(NotificationState)
                    notif_state.log_telegram_message(msg)
                return rx.toast.success("Document approved")

    @rx.event
    async def reject_document(self, doc_id: str):
        user = await self.get_state(AuthState)
        if user.user_role not in ["Admin", "Manager"]:
            return rx.toast.error("Unauthorized")
        for doc in self.documents:
            if doc.id == doc_id:
                doc.status = "Rejected"
                doc.reviewer = user.user.username
                doc.review_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                msg = f"❌ Document Rejected\nDocument: {doc.title}\nReviewed by: {user.user.username}"
                if await TelegramService.send_message(msg):
                    from app.states.notification_state import NotificationState

                    notif_state = await self.get_state(NotificationState)
                    notif_state.log_telegram_message(msg)
                return rx.toast.success("Document rejected")

    @rx.event
    async def delete_document(self, doc_id: str):
        self.documents = [d for d in self.documents if d.id != doc_id]
        return rx.toast.success("Document deleted")