def create_task(topic, data, description, screenshot=None):
    print(topic)
    print(description)
    print(f'{data} улетает в jira')
    if screenshot is not None:
        print(screenshot)