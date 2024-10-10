import streamlit as st

class Database:
    def __init__(self, url: str):
        self.url = url

    def connect(self):
        return st.connection(
            "postgresql",
            type="sql",
            url=self.url
        )


def get_db_connection(url: str):
    return Database(url)
