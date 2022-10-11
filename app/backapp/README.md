# BackApp - workshop backend app


## Build info for Apple M processors

```
docker buildx build --platform linux/arm64,linux/amd64 -t public.ecr.aws/e9n4z9i6/workshop:latest --push . 
```