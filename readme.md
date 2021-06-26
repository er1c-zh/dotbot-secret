# dotbot-secret

dotbot plugins for encrypt/decrypt private file.

# usage

## dotbot config

dotbot-secret will encrypt file in `src_path` and write to `dst_path`.

```yaml
- decrypt:
    -
        src_path: './encrypt'
        dst_path: './decrypt'
    - ['src_path', 'dst_path']

- encrypt:
    -
        src_path: './decrypt'
        dst_path: './encrypt'
    - ['src_path', 'dst_path']
```

## sample

![dotbot-secret-usage.gif](./doc/dotbot-secret-usage.gif)

## best practice

1. Add dotbot-secret as a submodule in your dotfiles repo and sync it when init dotbot.

   ```shell
   git submodule add https://github.com/er1c-zh/dotbot-secret.git
   ```

1. Modify `install` script with `--except encrypt` action.

    ```shell
   "${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" -c "${CONFIG}" --plugin-dir ./dotbot-secret --except encrypt "${@}"
    ```
   
1. Create [another `install` script named `do_encrypt`](https://github.com/er1c-zh/dotfiles/blob/master/do_encrypt) 
with `--only encrypt` for encrypt only, 
then use `do_encrypt` to encrypt files.
   
   ```shell
   "${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" -c "${CONFIG}" --plugin-dir ./dotbot-secret --only encrypt "${@}"
   ```
