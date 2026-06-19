app_name = "frappe_docs"
app_title = "Frappe Docs"
app_publisher = "makeown"
app_description = "A collaborative document editor built natively inside Frappe. Create, edit, and share rich-text documents with role-based permissions — no external tools required."
app_email = "makeown@example.com"
app_license = "mit"

page_css = {"gdocs": "public/css/gdocs.css"}

add_to_apps_screen = [
	{
		"name": "frappe_docs",
		"logo": "/assets/frappe_docs/images/logo.svg",
		"title": "Docs",
		"route": "/app/gdocs",
	}
]

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "frappe_docs",
# 		"logo": "/assets/frappe_docs/logo.png",
# 		"title": "Frappe Docs",
# 		"route": "/frappe_docs",
# 		"has_permission": "frappe_docs.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/frappe_docs/css/frappe_docs.css"
# app_include_js = "/assets/frappe_docs/js/frappe_docs.js"

# include js, css files in header of web template
# web_include_css = "/assets/frappe_docs/css/frappe_docs.css"
# web_include_js = "/assets/frappe_docs/js/frappe_docs.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "frappe_docs/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "frappe_docs/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "frappe_docs.utils.jinja_methods",
# 	"filters": "frappe_docs.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "frappe_docs.install.before_install"
# after_install = "frappe_docs.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "frappe_docs.uninstall.before_uninstall"
# after_uninstall = "frappe_docs.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "frappe_docs.utils.before_app_install"
# after_app_install = "frappe_docs.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "frappe_docs.utils.before_app_uninstall"
# after_app_uninstall = "frappe_docs.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "frappe_docs.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "frappe_docs.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"frappe_docs.tasks.all"
# 	],
# 	"daily": [
# 		"frappe_docs.tasks.daily"
# 	],
# 	"hourly": [
# 		"frappe_docs.tasks.hourly"
# 	],
# 	"weekly": [
# 		"frappe_docs.tasks.weekly"
# 	],
# 	"monthly": [
# 		"frappe_docs.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "frappe_docs.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "frappe_docs.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "frappe_docs.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "frappe_docs.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["frappe_docs.utils.before_request"]
# after_request = ["frappe_docs.utils.after_request"]

# Job Events
# ----------
# before_job = ["frappe_docs.utils.before_job"]
# after_job = ["frappe_docs.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"frappe_docs.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

