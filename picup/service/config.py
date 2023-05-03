"""
Time:     2023/4/11 8:30
Author:   忆千峰
Version:  V 0.1
File:     config.py
Email:    yiqf2022@126.com
"""
import base64
import os

import rsa
from PySide2.QtWidgets import QRadioButton
from webdav4.client import Client

from picup import base_path, secret_key_path, config_data, config_path
from picup.exception.param import ParamException
from picup.service.base import Base

import ruamel.yaml


class Config(Base):

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

        
        self._encrypt = ToolEnDe()
        self._cfg_path = f"{config_path}/{config_data['account.filename']}"

        
        self._ui.save_button.clicked.connect(lambda: self._parallel_run(self._save_config))
        self._ui.read_button.clicked.connect(self._get_config)
        self._ui.test_link_button.clicked.connect(lambda: self._parallel_run(self._link_test))

        
        self.username_encrypt = config_data["account.username.encrypt"]
        self.password_encrypt = config_data["account.password.encrypt"]

    def _save_config(self, step, data):
        try:
            yaml_data = {}
            ruamel_yaml = ruamel.yaml.YAML()
            if os.path.exists(self._cfg_path):
                with open(self._cfg_path, "r", encoding="utf-8") as f:
                    yaml_data = ruamel_yaml.load(f)
                    if not yaml_data: yaml_data = {}
            yaml_data.update(data)
            if data.get("username"):
                username = self._encrypt.encrypt(data["username"]) if self.username_encrypt else data["username"]
                yaml_data["username"] = username
            if data.get("password"):
                password = self._encrypt.encrypt(data["password"]) if self.password_encrypt else data["password"]
                yaml_data["password"] = password
            if data.get("compress") is not None:
                button_name, _, _ = self._compress_mapping[data["compress"]]
                yaml_data["compress"] = button_name
            if data.get("rename") is not None:
                yaml_data["rename"] = True if data["rename"] else False
            if self._is_enabled(step):
                with open(self._cfg_path, "w", encoding="utf-8") as f:
                    ruamel_yaml.dump(yaml_data, f)
                self._ui.config_text.setText(self._add_time(
                    "配置已保存!\n路径：{}".format(self._cfg_path.replace(base_path, ".").replace("\\", "/"))))
        except ParamException as e:
            self._ui.config_text.setText(self._add_time(str(e)))
        except Exception as e:
            self._ui.config_text.setText(self._add_time("配置保存失败，请重新配置!"))

    def _get_config(self):
        try:
            if not os.path.exists(self._cfg_path):
                return {}
            with open(self._cfg_path, "r", encoding="utf-8") as f:
                data = ruamel.yaml.safe_load(f)
                if not data: data = {}
            if data.get("username"):
                username = self._encrypt.decrypt(data["username"]) if self.username_encrypt else data["username"]
                self._ui.username_edit.setText(username)
            if data.get("password"):
                password = self._encrypt.decrypt(data["password"]) if self.password_encrypt else data["password"]
                self._ui.password_edit.setText(password)
            if data.get("address"):
                self._ui.address_edit.setText(data["address"])
            if data.get("custom_link"):
                self._ui.custom_link_edit.setText(data["custom_link"])
            if data.get("compress") is not None:
                for button_id, (button_name, compress_image_obj, custom_compress) in self._compress_mapping.items():
                    if data["compress"] == button_name:
                        custom_compress.setChecked(1)
                        break
            if data.get("rename") is not None:
                button: QRadioButton = self._ui.rename_open if data["rename"] else self._ui.rename_close
                if button: button.setChecked(1)
            if data.get("rename_text"):
                self._ui.rename_open_edit.setText(data["rename_text"])
            self._ui.config_text.setText(self._add_time("配置文件读取成功!"))
            return data
        except ParamException as e:
            self._ui.config_text.setText(self._add_time(str(e)))
        except Exception as e:
            self._ui.config_text.setText(self._add_time("配置读取出错，请检查配置!"))

    def _link_test(self, step, data):
        if not self._is_enabled(step): return
        client = Client(data["address"], auth=(data["username"], data["password"]))
        try:
            self._ui.test_text.setText(self._add_time("尝试连接中，请稍候..."))
            client.ls(".")
            self._ui.test_text.setText(self._add_time("连接服务器成功，测试通过!"))
        except Exception as e:
            self._ui.test_text.setText(self._add_time(f"连接服务器失败! {e.__class__.__name__}"))


class ToolEnDe:

    def __init__(self):
        self.public_key_file = f'{secret_key_path}/public_rsa.pem'
        self.private_key_file = f'{secret_key_path}/private_rsa.pem'
        if config_data["account.username.encrypt"] or config_data["account.password.encrypt"]:
            if not os.path.exists(self.public_key_file) or not os.path.exists(self.private_key_file):
                self.create_keys()

    def encrypt(self, s: str) -> str:
        try:
            
            s_encrypted = s.encode('utf-8')
            
            crypto_encrypted = rsa.encrypt(s_encrypted, self.public_key)
            
            crypto_encrypted_base64 = base64.b64encode(crypto_encrypted).decode('utf-8')
            return crypto_encrypted_base64
        except Exception as e:
            raise ParamException(f"加密失败 {e.__class__.__name__}")

    def decrypt(self, crypto_encrypted_base64: str) -> str:
        try:
            
            crypto_encrypted = base64.b64decode(crypto_encrypted_base64.encode('utf-8'))
            
            s_encrypted = rsa.decrypt(crypto_encrypted, self.private_key)
            
            s = s_encrypted.decode("utf-8")
            return s
        except Exception as e:
            raise ParamException(f"解密失败 {e.__class__.__name__}")

    @staticmethod
    def create_keys():
        if not os.path.isdir(secret_key_path): os.makedirs(secret_key_path)
        public_key, private_key = rsa.newkeys(1024)
        public = public_key.save_pkcs1()
        with open(f'{secret_key_path}/public_rsa.pem', 'wb+') as f:
            f.write(public)

        private = private_key.save_pkcs1()
        with open(f'{secret_key_path}/private_rsa.pem', 'wb+') as f:
            f.write(private)

    @property
    def public_key(self):
        if os.path.exists(self.public_key_file):
            with open(f'{secret_key_path}/public_rsa.pem', 'rb') as f:
                public_key = rsa.PublicKey.load_pkcs1(f.read())
            return public_key
        else:
            raise ParamException("public_key获取失败")

    @property
    def private_key(self):
        if os.path.exists(self.private_key_file):
            with open(f'{secret_key_path}/private_rsa.pem', 'rb') as f:
                private_key = rsa.PrivateKey.load_pkcs1(f.read())
            return private_key
        else:
            raise ParamException("private_key获取失败")
