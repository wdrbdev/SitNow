import os


# Alter the path and name of the user profile picture from uploading
def user_directory_path(instance, filename):
    upload_dir = 'profile_images'
    filename = "profile_img." + filename.split(".")[-1]
    filename = 'user_{0}/{1}'.format(instance.user.id, filename)
    return os.path.join(upload_dir, filename)
