Apply the config and files to your cluster:

1. Create namespace `test` if not present:

```bash
kubectl create namespace test
```

2. Apply the ConfigMaps and manifests:

```bash
kubectl apply -f k8s/quotes-configmaps.yaml -n test
kubectl apply -f k8s/quotes-app-deploy---service.yaml -n test
```

Notes:
- `quotes-config` contains `PORT` and `QUOTES_FILE` environment keys. Edit it to change runtime values without rebuilding the image.
- `quotes-file-config` holds `quotes.txt` and is mounted into the container at `/etc/quotes/quotes.txt`.
- The app reads `PORT` and `QUOTES_FILE` from environment variables.
