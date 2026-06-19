import frappe
import json


def _get_user_permission(doc, user=None):
	"""Return effective permission for user: 'owner', 'edit', 'comment', 'view', or None (no access)."""
	if not user:
		user = frappe.session.user
	if user == "Administrator" or doc.owner == user:
		return "owner"
	shared = json.loads(doc.shared_with or "[]")
	for entry in shared:
		if entry.get("user") == user:
			return entry.get("mode", "view")
	return None


@frappe.whitelist()
def get_all_docs():
	user = frappe.session.user
	all_docs = frappe.get_all(
		"GDoc",
		fields=["name", "title", "permission_mode", "modified", "creation", "owner", "shared_with"],
		order_by="modified desc",
	)
	result = []
	for d in all_docs:
		shared = json.loads(d.get("shared_with") or "[]")
		is_owner = (d.owner == user or user == "Administrator")
		is_shared = any(e.get("user") == user for e in shared)
		if is_owner or is_shared:
			effective = "owner" if is_owner else next(
				(e.get("mode", "view") for e in shared if e.get("user") == user), "view"
			)
			result.append({
				"name": d.name,
				"title": d.title,
				"permission_mode": d.permission_mode,
				"effective_mode": effective,
				"modified": str(d.modified),
				"creation": str(d.creation),
				"owner": d.owner,
			})
	return result


@frappe.whitelist()
def get_doc(name):
	doc = frappe.get_doc("GDoc", name)
	user = frappe.session.user
	effective = _get_user_permission(doc, user)
	if effective is None:
		frappe.throw("You do not have access to this document.", frappe.PermissionError)
	shared = json.loads(doc.shared_with or "[]")
	# Enrich shared list with full names
	enriched = []
	for entry in shared:
		u = frappe.db.get_value("User", entry["user"], ["full_name", "user_image"], as_dict=True) or {}
		enriched.append({**entry, "full_name": u.get("full_name") or entry["user"], "avatar": u.get("user_image") or ""})
	return {
		"name": doc.name,
		"title": doc.title,
		"content": doc.content or "",
		"permission_mode": doc.permission_mode or "edit",
		"effective_mode": effective,
		"is_owner": effective == "owner",
		"shared_with": enriched,
		"comments": json.loads(doc.comments_json or "[]"),
		"modified": str(doc.modified),
		"creation": str(doc.creation),
		"owner": doc.owner,
	}


@frappe.whitelist()
def save_doc(name, title, content, permission_mode="edit"):
	doc = frappe.get_doc("GDoc", name)
	effective = _get_user_permission(doc)
	if effective not in ("owner", "edit"):
		frappe.throw("You do not have edit permission.", frappe.PermissionError)
	doc.title = title
	doc.content = content
	doc.permission_mode = permission_mode
	doc.save(ignore_permissions=True)
	frappe.db.commit()
	return {"name": doc.name, "modified": str(doc.modified)}


@frappe.whitelist()
def save_comments(name, comments):
	doc = frappe.get_doc("GDoc", name)
	effective = _get_user_permission(doc)
	if effective not in ("owner", "edit", "comment"):
		frappe.throw("You do not have comment permission.", frappe.PermissionError)
	doc.comments_json = comments
	doc.save(ignore_permissions=True)
	frappe.db.commit()
	return {"ok": True}


@frappe.whitelist()
def delete_doc(name):
	doc = frappe.get_doc("GDoc", name)
	effective = _get_user_permission(doc)
	if effective != "owner":
		frappe.throw("Only the owner can delete this document.", frappe.PermissionError)
	frappe.delete_doc("GDoc", name, ignore_permissions=True)
	frappe.db.commit()
	return {"ok": True}


@frappe.whitelist()
def create_doc(title="Untitled document"):
	import random, string
	uid = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
	name = f"gdoc-{uid}"
	doc = frappe.get_doc({
		"doctype": "GDoc",
		"name": name,
		"title": title,
		"content": "",
		"permission_mode": "edit",
		"comments_json": "[]",
		"shared_with": "[]",
	})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	return {
		"name": doc.name,
		"title": doc.title,
		"content": "",
		"permission_mode": "edit",
		"effective_mode": "owner",
		"is_owner": True,
		"shared_with": [],
		"comments": [],
		"modified": str(doc.modified),
		"creation": str(doc.creation),
		"owner": doc.owner,
	}


@frappe.whitelist()
def share_doc(name, user, mode):
	"""Add or update a user's access to a document."""
	doc = frappe.get_doc("GDoc", name)
	effective = _get_user_permission(doc)
	if effective != "owner":
		frappe.throw("Only the owner can manage sharing.", frappe.PermissionError)
	if not frappe.db.exists("User", user):
		frappe.throw(f"User '{user}' not found.")
	shared = json.loads(doc.shared_with or "[]")
	for entry in shared:
		if entry["user"] == user:
			entry["mode"] = mode
			break
	else:
		shared.append({"user": user, "mode": mode})
	doc.shared_with = json.dumps(shared)
	doc.save(ignore_permissions=True)
	frappe.db.commit()
	# Return enriched entry
	u = frappe.db.get_value("User", user, ["full_name", "user_image"], as_dict=True) or {}
	return {"user": user, "mode": mode, "full_name": u.get("full_name") or user, "avatar": u.get("user_image") or ""}


@frappe.whitelist()
def unshare_doc(name, user):
	"""Remove a user's access from a document."""
	doc = frappe.get_doc("GDoc", name)
	effective = _get_user_permission(doc)
	if effective != "owner":
		frappe.throw("Only the owner can manage sharing.", frappe.PermissionError)
	shared = json.loads(doc.shared_with or "[]")
	shared = [e for e in shared if e["user"] != user]
	doc.shared_with = json.dumps(shared)
	doc.save(ignore_permissions=True)
	frappe.db.commit()
	return {"ok": True}


@frappe.whitelist()
def search_users(query):
	"""Search Frappe users by name or email for the share dialog."""
	users = frappe.get_all(
		"User",
		filters=[
			["User", "enabled", "=", 1],
			["User", "user_type", "=", "System User"],
			[
				"User", "name", "like", f"%{query}%",
				"or", "full_name", "like", f"%{query}%",
			],
		],
		fields=["name", "full_name", "user_image"],
		limit=8,
	)
	current = frappe.session.user
	return [u for u in users if u["name"] != current]
