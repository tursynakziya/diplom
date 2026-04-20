from .models import UserMessage, Notification, UserProfile


def user_profile(request):
    if request.user.is_authenticated:
        # Админ барлық функцияны көреді
        if request.user.is_superuser or request.user.is_staff:
            return {
                'disability_type': 'all',
                'show_visual_tools': True,
                'show_hearing_tools': True,
            }
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user,
            defaults={'disability_type': 'visual'}
        )
        return {
            'disability_type': profile.disability_type,
            'show_visual_tools': profile.show_visual_tools,
            'show_hearing_tools': profile.show_hearing_tools,
        }
    return {'disability_type': None, 'show_visual_tools': False, 'show_hearing_tools': False}


def chat_messages(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        user_msgs = UserMessage.objects.filter(sender=request.user).order_by('created_at')
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by('created_at')

        # Бір хронологиялық тізім жасаймыз
        timeline = []

        for msg in user_msgs:
            timeline.append({
                'side': 'user',
                'subject': msg.subject,
                'text': msg.message,
                'ts': msg.created_at,
            })
            if msg.reply:
                timeline.append({
                    'side': 'admin',
                    'subject': f'Re: {msg.subject}',
                    'text': msg.reply,
                    'ts': msg.replied_at,
                })

        # Notification-дарды қосамыз (admin → пайдаланушы)
        # "Re: ..." тақырыптылары UserMessage.reply арқылы жасалды — қайталанбас үшін өткізіп жіберемік
        replied_subjects = {f'Re: {m.subject}' for m in user_msgs if m.reply}
        for notif in notifications:
            if notif.subject not in replied_subjects:
                timeline.append({
                    'side': 'admin',
                    'subject': notif.subject,
                    'text': notif.message,
                    'ts': notif.created_at,
                })

        timeline.sort(key=lambda x: x['ts'])

        unread_count = notifications.count()

        return {
            'user_chat_messages': user_msgs,
            'chat_timeline': timeline,
            'chat_unread_count': unread_count,
        }
    return {'user_chat_messages': [], 'chat_timeline': [], 'chat_unread_count': 0}
