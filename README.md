# hsbot

## How to start

1. generate project using `nb create` .
2. create your plugin using `nb plugin create` .
3. writing your plugins under `src/plugins` folder.
4. run your bot using `nb run` .

## Documentation

See [Docs](https://v2.nonebot.dev/)

```
git update-index --assume-unchanged .env.dev
git update-index --assume-unchanged .env.prod
git update-index --assume-unchanged docker-compose.yml
```

如果需要恢复对文件的版本控制，执行以下操作

```
git update-index --no-assume-unchanged .env.dev
git update-index --no-assume-unchanged .env.prod
git update-index --no-assume-unchanged docker-compose.yml
```
