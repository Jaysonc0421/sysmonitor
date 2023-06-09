import json
import os


def get_document_ref(db):
    config_file = 'config.json'

    # If the file doesn't exist create it
    if not os.path.isfile(config_file):
        with open(config_file, 'w') as file:
            json.dump({}, file)

    # Load file data
    with open(config_file, 'r') as file:
        config_data = json.load(file)

    # Check if 'doc_id' field exists in the config data
    if 'doc_id' in config_data:
        doc_id = config_data['doc_id']

        # Get snapshot of the document
        doc_ref = db.collection('computers').document(doc_id)
        doc_snapshot = doc_ref.get()

        if doc_snapshot.exists:
            print('Document exists.')
            return doc_ref
        else:
            print("Document doesn't exist")

            # Create a new document, save its ID to config, and update config file
            new_doc_ref = db.collection('computers').document()
            new_doc_id = new_doc_ref.id

            config_data['doc_id'] = new_doc_id
            with open(config_file, 'w') as file:
                json.dump(config_data, file)

            print("New document created with ID:", new_doc_id)
            return new_doc_ref
    else:
        print("'doc_id' field doesn't exist in the config file")

        # Create a new document, save its ID to config, and update config file
        new_doc_ref = db.collection('computers').document()
        new_doc_id = new_doc_ref.id

        config_data['doc_id'] = new_doc_id
        with open(config_file, 'w') as file:
            json.dump(config_data, file)

        print("New document created with ID:", new_doc_id)
        return new_doc_ref

