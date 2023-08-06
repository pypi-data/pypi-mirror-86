# env-paths <!-- TODO: badge -->

This package is a modified [sindresorhus/env\-paths from nodejs](https://github.com/sindresorhus/env-paths) for python.

Returns the directory where the cache is located. This is different for each os.



## Install

```
$ pip install env-paths
```


## Usage

```python
from env_paths import env_paths

paths = env_paths('MyApp')
paths.data
# => '/home/atu4403/.local/share/MyApp-python'

paths.config
# => '/home/atu4403/.config/MyApp-python'
```

## Related
- [sindresorhus/env\-paths: Get paths for storing things like data, config, cache, etc](https://github.com/sindresorhus/env-paths)


## License

MIT © [atu4403](https://github.com/atu4403)