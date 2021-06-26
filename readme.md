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

![dotbot-secret-usage.gif](https://dsm01pap001files.storage.live.com/y4m2dz3sOKQtRYANK7pI48E0wvdUo3GSWf7EyO-R53wvoJakaEdvGLp4evSEToPBhdkXLzXJ6_0-h0d0reEkxyvwRQYkEGL5iIWF5qiar4v6HuA-IaQ1z0edHTi0eVIh54NZDtQ9fQOzHXigAvxpDkxKD_qKajSmYkwaTy00hmJM43hsZm8lkVe0Mdj3veKdOWm?width=1162&height=609&cropmode=none)

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
