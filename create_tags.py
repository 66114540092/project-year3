from tournaments.models import Tag

PRESET_TAGS = [
    'Pets & Animals',
    'Food & Drinks',
    'Gaming',
    'Movies & TV',
    'Music',
    'Travel & Places',
    'Art & Design',
    'Sports',
    'Tech & Gadgets',
    'Fashion',
    'Photography',
    'Memes',
    'Nature',
    'Architecture',
    'Other'
]

print("Creating preset tags...")
for tag_name in PRESET_TAGS:
    tag, created = Tag.objects.get_or_create(name=tag_name)
    if created:
        print(f"✓ Created: {tag_name}")
    else:
        print(f"- Already exists: {tag_name}")

print(f"\nTotal tags: {Tag.objects.count()}")
exit()