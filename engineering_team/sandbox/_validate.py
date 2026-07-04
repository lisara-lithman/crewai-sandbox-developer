from app import library, Member

# Validation script to confirm the Blocks object constructs without error
# Create a new Member
member = Member(member_id='1', name='John Doe')
library.members.append(member)

# Test the setup by checking the catalog
try:
    catalog = library.get_catalog()  # Access method to ensure no errors
    print('Library catalog loaded:', catalog)
except Exception as e:
    print('Failed to load library catalog:', e)
