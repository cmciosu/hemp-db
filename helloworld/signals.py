from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

# List of groups that will give the user 'is_staff' permission
STAFF_GROUPS = ['Admin', 'SrAdmin']

# Triggers when a user's group is updated.
# e.g. When a SrAdmin gives a user the Admin group, it will automatically give them is_staff
# so the new admin user may access the Django Administration dashboard. 
# If the user is removed from the group, it will also automatically remove is_staff.
@receiver(m2m_changed, sender=User.groups.through)
def update_is_staff_on_group_change(sender, instance, action, reverse, model, pk_set, **kwargs):

    # Check if the action is 'post_add' (user was added to a group)
    # Enabled is_staff
    if action == "post_add":
        for group_id in pk_set:
            group = Group.objects.get(id=group_id)
            if group.name in STAFF_GROUPS:
                instance.is_staff = True
                instance.save()
                break
    
    # Check if the action is 'post_remove' (user was removed from a group)
    # Disables is_staff
    elif action == "post_remove":
        for group_id in pk_set:
            group = Group.objects.get(id=group_id)
            if group.name in STAFF_GROUPS:
                # If the user is no longer in any STAFF_GROUPS, remove is_staff
                if not any(g.name in STAFF_GROUPS for g in instance.groups.all()):
                    instance.is_staff = False
                    instance.save()
                    break
