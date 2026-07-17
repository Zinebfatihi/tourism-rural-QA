"""
Test de RÉGRESSION (opération réelle) — CRUD d'un compte bancaire par l'admin.

Le test effectue de vraies opérations : il AJOUTE un compte bancaire, vérifie
qu'il apparaît dans la liste, puis le SUPPRIME et vérifie sa disparition. Le RIB
est horodaté (unique) pour rendre le test rejouable, et le compte de test est
retiré à la fin (aucune pollution des données).

Lien métier : cette opération est précisément celle qui lève l'anomalie ANO-05
(« sans compte bancaire configuré, aucune réservation n'est possible »).

Couvre TC-ADM-09 : gestion des comptes bancaires (création + suppression).
"""

import time

import pytest

from pages.admin_bank_accounts_page import AdminBankAccountsPage


@pytest.mark.regression
def test_admin_create_and_delete_bank_account(admin_session):
    page = AdminBankAccountsPage(admin_session).load()
    assert page.is_loaded(), "La page des comptes bancaires ne s'est pas chargée."

    rib = f"QA-RIB-{int(time.time())}"

    # 1) CRÉATION
    page.create_account(rib=rib, beneficiary="Bénéficiaire QA", bank="Banque QA")
    assert page.has_account(rib), (
        "Le compte bancaire créé n'apparaît pas dans la liste."
    )

    # 2) SUPPRESSION (nettoyage)
    page.delete_account(rib)
    assert page.is_account_absent(rib), (
        "Le compte bancaire n'a pas été supprimé de la liste."
    )
