# Deployment

## Tailwind CSS
Before committing code, the Tailwind CSS file needs to be compiled by running the following command:

```bash
make buildtailwind
```

After committing the code to master/main,  run:
    
```bash
export BW_SESSION=$(bw unlock --raw)
make deploy env=stage|prod
```

For a quick deploy,w here only assets and project files have changed, run:

```bash
make quickdeploy env=stage|prod
```

Note: After committing code, delete the build file `static/css/tailwind.css` to pick up CSS changes during development.
