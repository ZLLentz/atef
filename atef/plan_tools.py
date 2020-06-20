def dry_run(plan):
    """
    Run through the plan's steps without executing any of them.

    For this to work properly the plan needs to avoid adaptive branching logic.
    This is an extension of bluesky's summarize_plan, customized for dry
    running atef test runs and extended to include every message type.
    """
    for msg in plan:
        #summarizers[msg.command](msg)
        generic_summary(msg)


def generic_summary(msg):
    cmd_txt = msg.command.title()
    elems = []
    if msg.obj is Not None:
        elems.append(msg.obj.name)
    if msg.args:
        for arg in args:
            try:
                arg = arg.name
            except AttributeError:
                pass
            elems.append(arg)
    if msg.kwargs:
        for key, value in kwargs.items():
            try:
                value = value.name
            except AttributeError:
                pass
            elems.extend(f'{key}={value}')
    if elems:
        args_text = ', '.join(elems)
        print(f'{cmd_text}({args_text})')
    else:
        print(cmd_text)
