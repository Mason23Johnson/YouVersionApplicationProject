from app import client

def get_verse_of_the_day( day : int, versionid : int ) -> dict :
	passage_id = client.get_passage_id( day )
	passage = client.get_passage_text( versionid, passage_id )
	return passage 
	# possibly return version, passage_id, etc.