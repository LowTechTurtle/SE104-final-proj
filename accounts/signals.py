from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group # Import thêm Group
from .models import Profile

# -----------------------------------------------------------------------------
# SIGNAL 1: Tự động tạo Profile khi tạo User (Code cũ của bạn)
# -----------------------------------------------------------------------------
@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a Profile when a User is saved.
    """
    if created:
        Profile.objects.create(user=instance)
        print(f'Profile created for user: {instance.username}')
    else:
        # Kiểm tra xem user có profile chưa để tránh lỗi
        if hasattr(instance, 'profile'):
            instance.profile.save()

# -----------------------------------------------------------------------------
# SIGNAL 2: Tự động phân quyền (Group) khi sửa Role trong Profile (Code mới)
# -----------------------------------------------------------------------------
@receiver(post_save, sender=Profile)
def sync_user_group(sender, instance, created, **kwargs):
    """
    Tự động thêm User vào Group 'Manager' hoặc 'Staff' dựa trên Role của Profile.
    """
    user = instance.user
    role = instance.role

    # Lấy các Group từ Database
    try:
        manager_group = Group.objects.get(name='Manager')
        staff_group = Group.objects.get(name='Staff')
    except Group.DoesNotExist:
        # Nếu chưa tạo Group trong Admin thì bỏ qua để tránh lỗi crash
        print("Warning: Group 'Manager' or 'Staff' does not exist yet.")
        return

    # Logic đồng bộ
    if role == 'Manager':
        user.groups.add(manager_group)
        user.groups.remove(staff_group)
        print(f"Updated permissions: {user.username} -> Manager Group")
        
    elif role == 'Staff':
        user.groups.add(staff_group)
        user.groups.remove(manager_group)
        print(f"Updated permissions: {user.username} -> Staff Group")
        
    elif role == 'Admin':
        # Admin thường là Superuser hoặc quản lý cấp cao, 
        # ta xóa khỏi các nhóm giới hạn quyền này
        user.groups.remove(manager_group)
        user.groups.remove(staff_group)
        print(f"Updated permissions: {user.username} -> Admin (Removed from Staff/Manager groups)")