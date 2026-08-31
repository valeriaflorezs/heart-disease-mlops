# Etapa 4 — Kubernetes local (Minikube)

La API contenerizada en la Etapa 3 se despliega en un clúster de Kubernetes local con
[Minikube](https://minikube.sigs.k8s.io/), usando dos manifiestos en `k8s/`.

## `k8s/deployment.yaml`

- Despliega **2 réplicas** de `heart-disease-api:latest` (`imagePullPolicy: Never`, para usar la
  imagen construida localmente en vez de buscarla en un registro remoto).
- Define `readinessProbe` y `livenessProbe` apuntando a `GET /health`, para que Kubernetes
  verifique automáticamente que cada pod esté sirviendo antes de recibir tráfico.
- Límites de CPU/memoria razonables para un entorno local (`requests`/`limits`).

## `k8s/service.yaml`

Expone el deployment como `NodePort` en el puerto `30080`, accesible desde fuera del clúster.

## Despliegue

```bash
minikube start --driver=docker
docker build -t heart-disease-api:latest -f docker/Dockerfile .
minikube image load heart-disease-api:latest
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
```

## Verificación en vivo

```{code} text
$ kubectl get pods,svc
NAME                                    READY   STATUS    RESTARTS   AGE
pod/heart-disease-api-58449d8c9-cvql2   1/1     Running   0          15s
pod/heart-disease-api-58449d8c9-xv2rp   1/1     Running   0          15s

NAME                                TYPE       PORT(S)          AGE
service/heart-disease-api-service  NodePort   8000:30080/TCP   15s

$ curl http://$(minikube ip):30080/health
{"status":"ok","model_loaded":true}

$ curl -X POST http://$(minikube ip):30080/predict -d '{"Age":54,"Sex":"M", ...}'
{"prediction":0,"label":"Sin enfermedad cardíaca","probability_heart_disease":0.0785}
```

Ambos pods quedaron `Running` (1/1) y la API respondió una predicción real a través del
`Service` expuesto — confirmando que el despliegue funciona de extremo a extremo.
