# Copyright (c) 2026, Athif and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LibraryTransaction(Document):

    def validate(self):

        if self.type == "Issue":
            self.validate_article_status()
            self.validate_membership()
            self.validate_borrow_limit()

    def on_submit(self):
        self.update_article_status()

    def validate_article_status(self):

        article = frappe.get_doc("Library Article", self.article)

        if article.status != "Available":
            frappe.throw("Article is already issued")

    def validate_membership(self):

        memberships = frappe.get_all(
            "Library Membership",
            filters={
                "library_member": self.library_member,
                "paid": 1
            },
            fields=["name", "from_date", "to_date"]
        )

        if not memberships:
            frappe.throw("No active membership found")

        active_membership = False

        for membership in memberships:
            transaction_date = frappe.utils.getdate(self.date)

            if membership.from_date <= transaction_date <= membership.to_date:
                active_membership = True
                break

        if not active_membership:
            frappe.throw("Membership is expired")

    def validate_borrow_limit(self):

        settings = frappe.get_single("Library Settings")

        max_allowed = settings.max_articles

        issued_articles = frappe.db.count(
            "Library Transaction",
            filters={
                "library_member": self.library_member,
                "type": "Issue",
                "docstatus": 1
            }
        )

        returned_articles = frappe.db.count(
            "Library Transaction",
            filters={
                "library_member": self.library_member,
                "type": "Return",
                "docstatus": 1
            }
        )

        currently_issued = issued_articles - returned_articles

        if currently_issued >= max_allowed:
            frappe.throw("Maximum issued articles limit reached")

    def update_article_status(self):

        article = frappe.get_doc("Library Article", self.article)

        if self.type == "Issue":
            article.status = "Issued"

        elif self.type == "Return":
            article.status = "Available"

        article.save()