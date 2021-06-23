import dotbot, os


class Brew(dotbot.Plugin):
    _baseEncrypted = '/encrypt'
    _baseDecrypted = '/decrypt'
    _key = 'default_key'

    def can_handle(self, directive):
        return "decrypt" == directive

    def handle(self, directive, data):
        pwd = self._context.base_directory()
        log = self._log

        src = pwd + self._baseEncrypted
        dest = pwd + self._baseDecrypted

        log.info('Load from ' + src + ', write to ' + dest + '.')

        # key = raw_input('decrypt key:')

        # log.debug('Use key [' + key + '].')

        # self._key = key

        try:
            err = self.work(src, dest)
            if not (err is None):
                log.error(err)
                return err
        except BaseException as e:
            log.error(e)

        return True

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

            for line in src_file:
                # todo decrypt
                dest_file.writelines(line)

            dest_file.flush()
            src_file.close()
            dest_file.close()
            log.info('Decrypt ' + src + ' to ' + dest + ' successfully.')
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
