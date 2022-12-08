from mongoengine import *
from cryptography.fernet import Fernet
from APIs.TalpiotAPIs.User.user import User
from APIs.init_APIs import main as set_up_DB
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def login_info_already_exists(user, is_real_data=False):
    return len(LoginInfo.objects.filter(user=user, is_real_data=is_real_data)) > 0


def get_madar_key(password):
    """
    convert the custom key to a hash key ready to be ferneted
    :param password: the madar custom key
    :return: hash key
    """
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(bytes(password, encoding='utf8'))
    return base64.urlsafe_b64encode(digest.finalize())


class LoginInfo(Document):
    user = ReferenceField('User', required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    cse_username = StringField(required=True)
    cse_password = StringField(required=True)
    is_real_data = BooleanField(default=False, required=True)  # boolean if the data is real or not

    meta = {'collection': 'login_info'}

    __XOR_KEY = 1249
    __ACCURACY = 100.0
    __fernet_key = b'FVOwF-23paS9PIFBdmjCrYjhiQ6hyQEOfAcb832gS-0='

    @staticmethod
    def encrypt(password, token):
        return Fernet(get_madar_key(password)).encrypt(token.encode()).decode()

    @staticmethod
    def decrypt(password, token):
        return Fernet(get_madar_key(password)).decrypt(token.encode()).decode()


def insert(user_name, mahzor, email, password, cse_username, cse_password, madar_password, is_real_data=False):
    """
    insert the data as LoginInfo object to the collection
    :param user_name: fitting hebrew name to talpix
    :param mahzor: user's mahzor number
    :param email: user's university email
    :param password: user's university password
    :param cse_username: user's cse username (moodle)
    :param cse_password: user's cse password (moodle)
    :param madar_password: the madar custom key
    :param is_real_data: indicates if the data is real or not
    :return:
    """
    user = User.objects.filter(name=user_name, mahzor=mahzor).first()
    if user is None:
        return
    # encrypt the given data
    encrypted_huji_email = LoginInfo.encrypt(madar_password, email)
    encrypted_password = LoginInfo.encrypt(madar_password, password)
    encrypted_cse_username = LoginInfo.encrypt(madar_password, cse_username)
    encrypted_cse_password = LoginInfo.encrypt(madar_password, cse_password)
    if not login_info_already_exists(user):
        new_login_info = LoginInfo(user=user, email=encrypted_huji_email, password=encrypted_password,
                                   cse_username=encrypted_cse_username, cse_password=encrypted_cse_password,
                                   is_real_data=is_real_data)
        new_login_info.save()
        print("saved")
    else:
        # the case newer data is given - so need to update
        exist_login_info = LoginInfo.objects.filter(user=user).first()
        exist_login_info.email = encrypted_huji_email
        exist_login_info.password = encrypted_password
        exist_login_info.cse_username = encrypted_cse_username
        exist_login_info.cse_password = encrypted_cse_password
        exist_login_info.save()
        print("updated")


def delete(user_name, mahzor, is_real_data=False):
    """
    deletes the fitting object in the collection to the given data
    :param user_name: fitting hebrew name to talpix
    :param mahzor: user's mahzor number
    :param is_real_data: indicates if the data is real or not
    :return:
    """
    user = User.objects.filter(name=user_name, mahzor=mahzor).first()
    if login_info_already_exists(user, is_real_data):
        Lgn_info_obj = LoginInfo.objects.filter(user=user)
        Lgn_info_obj[0].delete()
        print("deleted")
    else:
        print("this user don't have login info")


set_up_DB()
