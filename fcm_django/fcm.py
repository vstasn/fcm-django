from firebase_admin import exceptions
from firebase_admin import messaging


def fcm_send_message(
    registration_id,
    title=None,
    body=None,
    icon=None,
    data=None,
    sound=None,
    badge=None,
    low_priority=False,
    condition=None,
    time_to_live=None,
    click_action=None,
    collapse_key=None,
    delay_while_idle=False,
    restricted_package_name=None,
    dry_run=False,
    color=None,
    tag=None,
    body_loc_key=None,
    body_loc_args=None,
    title_loc_key=None,
    title_loc_args=None,
    content_available=None,
    extra_kwargs={},
    api_key=None,
    json_encoder=None,
    extra_notification_kwargs=None,
    **kwargs
):

    apns_sound = sound
    if kwargs.get("critical", False):
        apns_sound = messaging.CriticalSound("default", critical=True)

    notification = None
    if title and body:
        notification = messaging.Notification(
            title=title,
            body=body,
            image=icon,
        )

    message = messaging.Message(
        notification=notification,
        data=data,
        token=registration_id,
        android=messaging.AndroidConfig(
            collapse_key=collapse_key,
            ttl=time_to_live,
            restricted_package_name=restricted_package_name,
            notification=messaging.AndroidNotification(
                color=color,
                sound=sound,
                tag=tag,
                click_action=click_action,
                body_loc_key=body_loc_key,
                body_loc_args=body_loc_args,
                title_loc_key=title_loc_key,
                title_loc_args=title_loc_args,
            ),
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        loc_key=body_loc_key,
                        loc_args=body_loc_args,
                        title_loc_key=title_loc_key,
                        title_loc_args=title_loc_args,
                    ),
                    sound=apns_sound,
                    content_available=content_available,
                    badge=badge,
                )
            )
        ),
    )

    res = {}
    try:
        res["data"] = messaging.send(message, dry_run)
    except (exceptions.FirebaseError, ValueError) as error:
        res["error"] = error

    return {"results": [res]}


def fcm_send_single_device_data_message(registration_id, *args, **kwargs):
    data = kwargs.pop("data_message", None)
    kwargs.update({"data": data})

    return fcm_send_message(registration_id=registration_id, **kwargs)


def fcm_send_bulk_message(
    registration_ids,
    title=None,
    body=None,
    icon=None,
    data=None,
    sound=None,
    badge=None,
    low_priority=False,
    condition=None,
    time_to_live=None,
    click_action=None,
    collapse_key=None,
    delay_while_idle=False,
    restricted_package_name=None,
    dry_run=False,
    color=None,
    tag=None,
    body_loc_key=None,
    body_loc_args=None,
    title_loc_key=None,
    title_loc_args=None,
    content_available=None,
    extra_kwargs={},
    api_key=None,
    json_encoder=None,
    extra_notification_kwargs=None,
    **kwargs
):
    apns_sound = sound
    if kwargs.get("critical", False):
        apns_sound = messaging.CriticalSound("default", critical=True)

    notification = None
    if title and body:
        notification = messaging.Notification(
            title=title,
            body=body,
            image=icon,
        )

    multicast = messaging.MulticastMessage(
        notification=notification,
        data=data,
        tokens=registration_ids,
        android=messaging.AndroidConfig(
            collapse_key=collapse_key,
            ttl=time_to_live,
            restricted_package_name=restricted_package_name,
            notification=messaging.AndroidNotification(
                color=color,
                sound=sound,
                tag=tag,
                click_action=click_action,
                body_loc_key=body_loc_key,
                body_loc_args=body_loc_args,
                title_loc_key=title_loc_key,
                title_loc_args=title_loc_args,
            ),
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        loc_key=body_loc_key,
                        loc_args=body_loc_args,
                        title_loc_key=title_loc_key,
                        title_loc_args=title_loc_args,
                    ),
                    sound=apns_sound,
                    content_available=content_available,
                    badge=badge,
                )
            )
        ),
    )

    response = messaging.send_multicast(multicast)
    responses = [
        {"error": response.exception, "success": response.success}
        for response in response.responses
    ]

    return responses


def fcm_send_bulk_data_messages(*args, **kwargs):
    data = kwargs.pop("data_message", None)
    kwargs.update({"data": data})

    return fcm_send_bulk_message(**kwargs)


class FCMError(Exception):
    pass
