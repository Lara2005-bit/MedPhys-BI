import streamlit as st
import streamlit_authenticator as stauth
import gspread
from google.oauth2.service_account import Credentials
import time
import bcrypt
import logging

# ─────────────────────────────────────────────
# Escopos necessários para a Service Account
# ─────────────────────────────────────────────
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Nome das colunas na planilha (linha 1 = cabeçalho)
# username | name | email | password | preauthorized
SHEET_NAME = "medphys_users"  # nome da aba na planilha


class UsersManagement:
    def __init__(self):
        self._gc = self._get_gspread_client()
        self._worksheet = self._get_worksheet()
        self.config = self._load_config()
        self.authenticator = self._build_authenticator()
        st.session_state["user_management"] = self

    # ──────────────────────────────────────────
    # Conexão com Google Sheets
    # ──────────────────────────────────────────

    def _get_gspread_client(self) -> gspread.Client:
        """Cria cliente gspread usando credenciais do st.secrets."""
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES,
        )
        return gspread.authorize(creds)

    def _get_worksheet(self) -> gspread.Worksheet:
        """Abre a planilha pelo ID definido em st.secrets."""
        spreadsheet = self._gc.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])
        try:
            ws = spreadsheet.worksheet(medphys-users)
        except gspread.WorksheetNotFound:
            # Cria a aba com cabeçalho se não existir
            ws = spreadsheet.add_worksheet(title=medphys-users, rows=200, cols=5)
            ws.append_row(["username", "name", "email", "password", "preauthorized"])
        return ws

    # ──────────────────────────────────────────
    # Leitura / escrita do config
    # ──────────────────────────────────────────

    def _load_config(self) -> dict:
        """Lê a planilha e monta o dict de config do streamlit-authenticator."""
        records = self._worksheet.get_all_records()
        credentials = {"usernames": {}}
        preauthorized = {"emails": []}

        for row in records:
            uname = row.get("username", "").strip()
            if not uname:
                continue
            credentials["usernames"][uname] = {
                "name": row.get("name", ""),
                "email": row.get("email", ""),
                "password": row.get("password", ""),  # já armazenado como hash bcrypt
            }
            if str(row.get("preauthorized", "")).lower() in ("true", "1", "yes"):
                preauthorized["emails"].append(row.get("email", ""))

        return {
            "credentials": credentials,
            "cookie": {
                "name": st.secrets["cookie"]["name"],
                "key": st.secrets["cookie"]["key"],
                "expiry_days": int(st.secrets["cookie"].get("expiry_days", 30)),
            },
            "preauthorized": preauthorized,
        }

    def _save_config(self) -> bool:
        """Sobrescreve a planilha com o estado atual de self.config."""
        try:
            rows = [["username", "name", "email", "password", "preauthorized"]]
            users = self.config["credentials"]["usernames"]
            pre_emails = set(self.config.get("preauthorized", {}).get("emails", []))
            for uname, info in users.items():
                rows.append([
                    uname,
                    info.get("name", ""),
                    info.get("email", ""),
                    info.get("password", ""),
                    "true" if info.get("email", "") in pre_emails else "false",
                ])
            # Limpa e reescreve a aba inteira
            self._worksheet.clear()
            self._worksheet.update(rows)
            return True
        except Exception as e:
            logging.error(f"Erro ao salvar no Google Sheets: {e}")
            return False

    # ──────────────────────────────────────────
    # Autenticador
    # ──────────────────────────────────────────

    def _build_authenticator(self) -> stauth.Authenticate:
        return stauth.Authenticate(
            self.config["credentials"],
            self.config["cookie"]["name"],
            self.config["cookie"]["key"],
            self.config["cookie"]["expiry_days"],
            self.config["preauthorized"],
        )

    # ──────────────────────────────────────────
    # Widgets públicos (mesma interface de antes)
    # ──────────────────────────────────────────

    def login_widget(self) -> None:
        try:
            self.authenticator.login(
                fields={
                    "Form name": "Log in",
                    "Username": "Usuário",
                    "Password": "Senha",
                }
            )
        except Exception as e:
            st.error(e)

    def logout_widget(self) -> None:
        try:
            self.authenticator.logout("Log out", "sidebar")
        except Exception as e:
            st.error(e)

    def get_user_info(self) -> None:
        with st.container(border=True):
            users = self.config["credentials"]["usernames"]
            st.write("## Usuários cadastrados")
            for user, user_info in users.items():
                st.write(f"### {user}")
                st.write(f"**Nome:** {user_info['name']}")
                st.write(f"**Email:** {user_info['email']}")

    def forgot_password_widget(self) -> None:
        try:
            (
                username_of_forgotten_password,
                _,
                _,
            ) = self.authenticator.forgot_password(
                fields={
                    "Form name": "Esqueci minha senha",
                    "Username": "Usuário",
                    "Submit": "Submeter",
                }
            )
            if username_of_forgotten_password:
                st.session_state["forgot_password_clicked"] = False
                st.success("Nova senha enviada por e-mail com sucesso!")
                time.sleep(1)
                st.rerun()
            elif username_of_forgotten_password == False:
                st.error("Usuário não encontrado")
        except Exception as e:
            st.error(e)

    def forgot_username_widget(self) -> None:
        try:
            username_of_forgotten_username, email_of_forgotten_username = (
                self.authenticator.forgot_username(
                    fields={
                        "Form name": "Esqueci meu usuário",
                        "Email": "Email",
                        "Submit": "Submeter",
                    }
                )
            )
            if username_of_forgotten_username:
                st.session_state["forgot_username_clicked"] = False
                st.success("Usuário enviado por e-mail com sucesso!")
                time.sleep(1)
                st.rerun()
            elif username_of_forgotten_username == False:
                st.error("Email não encontrado")
        except Exception as e:
            st.error(e)

    def reset_password_widget(self) -> None:
        if st.session_state.get("username") is None:
            return
        try:
            if self.authenticator.reset_password(
                st.session_state["username"],
                fields={
                    "Form name": "Redefinir senha",
                    "Current password": "Senha atual",
                    "New password": "Nova senha",
                    "Repeat password": "Repetir senha",
                    "Reset": "Redefinir",
                },
            ):
                if self._save_config():
                    st.success("Senha modificada com sucesso!")
                else:
                    st.error("Erro ao modificar senha")
        except Exception as e:
            error_messages = {
                "Password/repeat password fields cannot be empty": "Senha e repetição de senha não podem estar vazios!",
                "Passwords do not match": "Senhas não coincidem!",
                "Current password is incorrect": "Senha atual incorreta!",
            }
            st.error(error_messages.get(str(e), str(e)))

    def new_user_widget(self) -> None:
        try:
            (
                email_of_registered_user,
                _,
                _,
            ) = self.authenticator.register_user(
                preauthorization=False,
                domains=["@hcpa.edu.br"],
                fields={
                    "Form name": "Registrar usuário",
                    "Email": "Email",
                    "Name": "Nome",
                    "Username": "Usuário",
                    "Password": "Senha",
                    "Repeat password": "Repetir senha",
                    "Register": "Registrar",
                },
            )
            if email_of_registered_user:
                if self._save_config():
                    st.success("Usuário registrado com sucesso!")
                else:
                    st.error("Erro ao registrar usuário")
        except Exception as e:
            error_messages = {
                "Password/repeat password fields cannot be empty": "Senha e repetição de senha não podem estar vazios!",
                "Passwords do not match": "Senhas não coincidem!",
                "Email is not valid": "Email não é válido!",
                "Email already taken": "Email já registrado!",
                "Username is not valid": "Usuário não é válido!",
                "Name is not valid": "Nome não é válido!",
                "Email not allowed to register": "Email não permitido para registro!",
            }
            st.error(error_messages.get(str(e), str(e)))

    def update_user_widget(self) -> None:
        if st.session_state.get("username") is None:
            return
        try:
            if self.authenticator.update_user_details(
                st.session_state["username"],
                fields={
                    "Form name": "Atualizar detalhes do usuário",
                    "Field": "Campo",
                    "Name": "Nome",
                    "Email": "Email",
                    "New value": "Novo valor",
                    "Update": "Atualizar",
                },
            ):
                if self._save_config():
                    st.success("Campos atualizados com sucesso!")
                else:
                    st.error("Erro ao atualizar campos")
        except Exception as e:
            error_messages = {
                "Field cannot be empty": "Campo não pode estar vazio!",
                "New value not provided": "Novo valor não fornecido!",
                "Email is not valid": "Email não é válido!",
                "Email already taken": "Email já registrado!",
                "Name is not valid": "Nome não é válido!",
                "New and current values are the same": "Novo e valor atual são iguais!",
            }
            st.error(error_messages.get(str(e), str(e)))

    def _remove_user_submit(self, username: str) -> None:
        if not username:
            st.error("Usuário não pode estar vazio")
        elif username not in self.config["credentials"]["usernames"]:
            st.error("Usuário não encontrado")
        else:
            del self.config["credentials"]["usernames"][username]
            if self._save_config():
                st.success("Usuário removido com sucesso!")
            else:
                st.error("Erro ao remover usuário")

    def remove_user_widget(self) -> None:
        with st.form("remove_user"):
            st.write("### Remover usuário")
            username = st.text_input("Usuário")
            submit_button = st.form_submit_button("Remover")
            if submit_button:
                self._remove_user_submit(username)
