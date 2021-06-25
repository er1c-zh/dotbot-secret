# coding=utf-8
import dotbot
import os
from pyDes import des, ECB, PAD_PKCS5
import base64
import getpass


class Brew(dotbot.Plugin):
    _BASE_ENCRYPTED = './encrypt'
    _BASE_DECRYPTED = './decrypt'
    _key = 'default_key'
    _crypto = None
    _action = None

    ACTION_DECRYPT = 'decrypt'
    ACTION_ENCRYPT = 'encrypt'

    def can_handle(self, directive):
        return directive in [self.ACTION_ENCRYPT, self.ACTION_DECRYPT]

    def handle(self, directive, data):
        pwd = self._context.base_directory()
        log = self._log

        log.info(data)

        # 获取加解密的key
        try:
            key = getpass.getpass('[dotbot-secret]Please input key:')
        except BaseException as e:
            log.error(e)
            return True
        self._key = key
        try:
            self.gen_crypto()
        except BaseException as e:
            log.error(e)
            return True

        self._action = directive

        defaults = self._context.defaults().get(self._action, {})
        src_path = defaults.get('src_path',
                                self._BASE_ENCRYPTED if self._action == self.ACTION_DECRYPT else self._BASE_DECRYPTED)
        dst_path = defaults.get('dst_path',
                                self._BASE_DECRYPTED if self._action == self.ACTION_DECRYPT else self._BASE_ENCRYPTED)

        for item in data:
            _src_path = src_path
            _dst_path = dst_path
            if isinstance(item, dict):
                _src_path = item.get('src_path', src_path)
                _dst_path = item.get('dst_path', dst_path)
            elif isinstance(item, list):
                _src_path = item[0] if len(item) > 0 else src_path
                _dst_path = item[1] if len(item) > 1 else dst_path
            src = os.path.join(pwd, _src_path)
            dst = os.path.join(pwd, _dst_path)
            log.info('Load from ' + src + ', write to ' + dst + '.')
            try:
                err = self.work(src, dst)
                if not (err is None):
                    log.error(err)
                    return True
            except BaseException as e:
                log.error(e)
                return True

        return True

    def gen_crypto(self):
        pad_len = 8 - len(self._key) % 8
        key = self._key
        for _ in range(pad_len):
            key += ' '
        self._crypto = des(key, ECB)

    def work(self, src, dest):
        log = self._log

        if not os.access(src, os.F_OK | os.R_OK):
            return ValueError('Access ' + src + ' failed.')

        if os.path.isfile(src):
            if os.access(dest, os.F_OK):
                log.warning('Skip ' + src + ' because ' + dest + ' already existed.')
                return None
            src_file = open(src, mode='r')
            dest_file = open(dest, mode='w')
            origin = ''.join(src_file.readlines())
            if self._action == self.ACTION_DECRYPT:
                dest_file.writelines(self.decrypt(origin))
            else:
                dest_file.writelines(self.encrypt(origin))

            dest_file.flush()
            src_file.close()
            dest_file.close()
            if self._action == self.ACTION_DECRYPT:
                log.info('Decrypt ' + src + ' to ' + dest + ' successfully.')
            else:
                log.info('Encrypt' + src + ' to ' + dest + ' successfully.')

            return None

        if not os.path.isdir(src):
            return ValueError('Unsupported path type: ' + src + '.')

        # recursive check folder
        file_list = os.listdir(src)

        for f in file_list:
            next_src_path = os.path.join(src, f)
            next_dest_path = os.path.join(dest, f)
            if os.path.isdir(next_src_path):
                # check dest folder
                if not os.access(next_dest_path, os.F_OK):
                    # create folder if not exist
                    os.mkdir(next_dest_path)
                if not os.access(next_dest_path, os.R_OK | os.W_OK):
                    # check access
                    log.warning('Skip ' + next_src_path + ' because access ' + next_dest_path + ' failed.')
                    continue
                if not os.path.isdir(next_dest_path):
                    # check isdir
                    log.warning('Skip ' + next_src_path + ' because of existed file ' + next_dest_path + '.')
                    continue

            self.work(next_src_path, next_dest_path)

        return None

    def encrypt(self, src):
        return base64.b64encode(self._crypto.encrypt(src.encode('utf-8'), padmode=PAD_PKCS5))

    def decrypt(self, src):
        return self._crypto.decrypt(base64.b64decode(src), padmode=PAD_PKCS5)
