import json
import os

# Initialize Firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Get the document reference for this system
from modules.config_util import get_document_ref

doc_ref = get_document_ref(db)

# Initialize Plugin Manager
from modules.plugin_manager import PluginManager

plugin_manager = PluginManager('plugins', doc_ref)
plugin_manager.load_plugins()

# Listen for snapshots on the document
def on_snapshot(snapshot, changes, read_time):
    for plugin_name, plugin in plugin_manager.plugins.items():
        if hasattr(plugin, 'on_snapshot'):
            plugin.on_snapshot(snapshot, changes, read_time)

doc_ref.on_snapshot(on_snapshot)

# Keep the program running
while True:
    continue
