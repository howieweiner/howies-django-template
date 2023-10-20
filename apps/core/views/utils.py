def add_page_context_data(
    context,
    section: str,
    heading: str,
    model_name: str = None,
    delete_action: str = None,
):
    context.update(
        {
            "heading": heading,
            "section": section,
            "model_name": model_name,
            "delete_action": delete_action,
        }
    )
    return context
